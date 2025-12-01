import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
import cv2
from anpr_service import ANPRService

app = FastAPI(title='ANPR API')

svc = ANPRService()

"""
Endpoint para leer la placa de una imagen subida.
Recibe:
- file: imagen subida como archivo
Regresa:
- plate_text: texto de la placa detectada (o None)
"""
@app.post('/read_plate')
async def read_plate(file: UploadFile = File(...)):
    contents = await file.read()
    # Verificar que el archivo no esté vacío
    if not contents:
        raise HTTPException(status_code=400, detail='Empty file')

    # Decodificar la imagen para OpenCV
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail='Invalid image')

    
    result = svc.read_plate_from_image(img)             # Usar el servicio ANPR para leer la placa

    
    if result.get('plate_text') is None:                # Si no se detectó ninguna placa se devuelve un mensaje 
        return JSONResponse(status_code=200, content={
            'plate_text': None,
            'message': 'No plate detected',
            'candidates': result.get('candidates', [])
        })
    
    
    return {                                            # Solo devolver el texto del mejor resultado
        'plate_text': result['plate_text'],             # Se pueden descomentar las líneas siguientes para devolver más información
       # 'plate_score': result.get('plate_score'),
       # 'bbox': result.get('bbox'),
       # 'candidates': result.get('candidates', [])
    }

# dirección ip y puerto para correr el servicio
if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
