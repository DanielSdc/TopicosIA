import os
import re
from typing import Optional, List, Dict, Any
import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR


class ANPRService:
    def __init__(self, model_path: Optional[str] = None, ocr_lang: str = 'en'):
        root = os.path.dirname(__file__)
        if model_path is None:
            model_path = os.path.join(root, 'model', 'best.pt')

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo no encontrado en: {model_path}")

        self.model = YOLO(model_path)
        self.ocr = PaddleOCR(use_textline_orientation=True, lang=ocr_lang)

    def _clean_text(self, t: str) -> str:
        if t is None:
            return ''
        return re.sub(r'[^A-Z0-9]', '', t.upper())

    def read_plate_from_image(self, image: np.ndarray, limite_confianza: float = 0.6) -> Dict[str, Any]:
        """Detector de placas y OCR.

        Recibe:
          - image: imagen como numpy array

        Regresa:
          - plate_text: placa seleccionada (o None)
          - plate_score: puntuación usada para la selección (puntuación OCR o confianza de detección)
          - bbox: [x1,y1,x2,y2] de la detección usada (o None)
          - candidates: lista de diccionarios candidatos para depuración
        """
        results = self.model(image)

        candidates: List[Dict[str, Any]] = []

        for result in results:
            # Filtrar solo clase 0 (correspondiente a placas)
            try:
                idxs = (result.boxes.cls == 0).nonzero(as_tuple=True)[0]
                if len(idxs) == 0:
                    idxs = range(len(result.boxes))
            except Exception:
                idxs = range(len(result.boxes))

            # Iterar sobre las detecciones de placas y validar que superen el umbral de confianza
            for idx in idxs:
                try:
                    conf = float(result.boxes.conf[idx].item())
                except Exception:
                    conf = 0.0
                if conf < limite_confianza:
                    continue

                # Obtener coordenadas de la caja (x1,y1,x2,y2) donde se detectó la placa
                xyxy = result.boxes.xyxy[idx].squeeze().tolist()
                x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])

                # Recortar con padding (10 píxeles) y verificar limites
                h, w = image.shape[:2]
                pad = 10

                # Aplicar padding y asegurar que no se salga de los limites de la imagen
                x1p = max(0, x1 - pad)
                y1p = max(0, y1 - pad)
                x2p = min(w - 1, x2 + pad)
                y2p = min(h - 1, y2 + pad)

                plate_img = image[y1p:y2p, x1p:x2p]

                # Realizar OCR en la imagen recortada 
                try:
                    ocr_res = self.ocr.predict(cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB))
                except Exception:
                    ocr_res = []

                # Extraer resultados de OCR
                ocr_out = ocr_res[0] if ocr_res else {}
                texts = ocr_out.get('rec_texts', [])
                scores = ocr_out.get('rec_scores', [])

                # Almacenar candidatos
                for i, txt in enumerate(texts):
                    txt_clean = self._clean_text(txt)
                    if not txt_clean:
                        continue
                    ocr_score = scores[i] if i < len(scores) else None
                    candidates.append({
                        'orig': txt,
                        'clean': txt_clean,
                        'ocr_score': float(ocr_score) if ocr_score is not None else None,
                        'det_conf': conf,
                        'bbox': [x1, y1, x2, y2],
                    })

        """
        Heurística para seleccionar la mejor placa entre los candidatos:
        1. Filtrar candidatos con longitud válida (4-10 caracteres).
        2. Priorizar candidatos que contengan al menos una letra y un dígito.
        3. Si no hay candidatos con letras y dígitos, considerar aquellos con solo dígitos.
        4. Si no hay candidatos con solo dígitos, considerar todos los alfanuméricos.
        5. Dentro de cada grupo, seleccionar el candidato con la puntuación OCR más alta.
        """
        def valid_len(s: str) -> bool:
            return 4 <= len(s) <= 10

        has_letter_digit = [c for c in candidates if valid_len(c['clean']) and re.search(r'[A-Z]', c['clean']) and re.search(r'[0-9]', c['clean'])]
        has_digit = [c for c in candidates if valid_len(c['clean']) and re.search(r'[0-9]', c['clean'])]
        alnum = [c for c in candidates if valid_len(c['clean']) and re.fullmatch(r'[A-Z0-9]+', c['clean'])]


        # Función para obtener el score OCR
        def obtener_score_ocr(candidato):
            return candidato['ocr_score']

        # Función de respaldo en caso de que no haya puntuaciones OCR
        def obtener_criterios_respaldo(candidato):
            # Devuelve una tupla: primero compara confianza, si hay empate, compara longitud
            return (candidato.get('det_conf', 0.0), len(candidato['clean']))
        

        chosen = None
        for pool in (has_letter_digit, has_digit, alnum):
            if pool:
                with_scores = [p for p in pool if p['ocr_score'] is not None]
                if with_scores:
                    # Usamos la función definida para obtener el score OCR
                    chosen = max(with_scores, key=obtener_score_ocr)
                else:
                    # Si no hay scores OCR, usamos criterios de respaldo
                    chosen = max(pool, key=obtener_criterios_respaldo)
                break

        # Resultado final en caso de no encontrar ninguna placa     
        result_out: Dict[str, Any] = {
            'plate_text': None,
            'plate_score': None,
            'bbox': None,
            'candidates': candidates,
        }

        # Si se encontró una placa valida cargar el resultado
        if chosen:
            result_out['plate_text'] = chosen['clean']
            result_out['plate_score'] = chosen.get('ocr_score') if chosen.get('ocr_score') is not None else chosen.get('det_conf')
            result_out['bbox'] = chosen['bbox']

        return result_out
