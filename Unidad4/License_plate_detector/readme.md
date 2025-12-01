# License Plate Detector API

Esta aplicación es una API REST construida con **FastAPI** que permite la detección y reconocimiento automático de matrículas vehiculares (ANPR) a partir de imágenes. Utiliza **YOLOv11** para la detección de la ubicación de la placa y **PaddleOCR** para la lectura de los caracteres.

## Estructura del Proyecto

- **`app.py`**: Archivo principal que contiene la definición de la API y los endpoints.
- **`anpr_service.py`**: Contiene la clase `ANPRService` con la lógica de negocio: carga de modelos, preprocesamiento de imagen, inferencia y heurísticas de selección de texto.
- **`model/`**: Carpeta que almacena los recursos del modelo de IA.
  - `best.pt`: Archivo de pesos del modelo YOLOv11 entrenado específicamente para detectar matrículas.

* **`requirements.txt`**: Lista de dependencias de Python necesarias para ejecutar el proyecto.

## Requisitos Previos

- Python 3.12+.
- (Opcional) GPU con soporte CUDA para un entrenamiento más rápido, aunque funciona perfectamente en CPU o se puede optar por utilizar Google Colab.

## Instalación

1.  **Clonar o descargar el proyecto** en tu máquina local.

2.  **Instalar dependencias**:
    Se recomienda hacer el proceso en un entorno virtual.
    Ejecuta el siguiente comando en tu terminal para instalar todas las librerías necesarias:

    ```
    pip install -r requirements.txt
    ```

## Ejecución

Para iniciar el servidor de desarrollo, ejecuta el siguiente comando desde la raíz del proyecto:

```
python app.py
```

Alternativamente, puedes usar `uvicorn` directamente:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Importante**: Al iniciar la aplicación por primera vez, es normal que tarde unos segundos (aprox. 1m) en arrancar. Esto se debe a que está cargando los modelos `YOLO` y `PaddleOCR` en la memoria RAM para asegurar que las peticiones posteriores sean rápidas.

## Uso de la API

La API expone documentación interactiva automática (Swagger UI) que se puede consultar en:

- **URL**: `http://localhost:8000/docs`

### Endpoint: `/read_plate`

- **Método**: `POST`
- **Descripción**: Recibe un archivo de imagen y devuelve la matrícula detectada.

#### Ejemplo de petición con cURL:

```bash
curl -X POST "http://127.0.0.1:8000/read_plate" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@media/license_plate_01.jpg"
```

#### Ejemplo de Respuesta JSON:

```json
{
  "plate_text": "HA9354A"
}
```

Si no se detecta ninguna matrícula, la respuesta será:

```json
{
  "plate_text": null,
  "message": "No plate detected",
  "candidates": []
}
```

## Sobre el Modelo (`model/`)

En la carpeta `model` encontrarás:

1.  **`best.pt`**: Es un modelo YOLOv11n que ha sido entrenado para identificar la región rectangular donde se encuentra una matrícula en una foto.
