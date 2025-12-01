# Detector de Matrículas (License Plate Detector)

Este proyecto consiste en el entrenamiento de un modelo de detección de objetos para identificar matrículas de vehículos utilizando la arquitectura **YOLOv11** (You Only Look Once). El entrenamiento se realizó utilizando Google Colab y un dataset público de Roboflow.

## 📊 Dataset

El dataset utilizado para este proyecto fue obtenido de Roboflow Universe:

- **Fuente:** [License Plate Recognition - Roboflow](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e)
- **Cantidad de imágenes:** 10,125
- **División de datos:**
  - 70% Entrenamiento
  - 20% Test
  - 10% Validación

## 🧠 Modelo y Entrenamiento

Se utilizó el modelo **YOLOv11 nano (`yolo11n.pt`)** de la librería `ultralytics`.

**Parámetros de entrenamiento:**

- **Épocas:** 50
- **Batch size:** 16
- **Tamaño de imagen:** 640px
- **Optimizador:** Auto
- **Dispositivo:** GPU (T4 en Google Colab)

## 📂 Estructura del Proyecto

```
model_train/
├── license_plate_detector.ipynb  # Notebook con el código de entrenamiento
├── readme.md                     # Este archivo
└── train3/                       # Resultados del entrenamiento
    ├── args.yaml                 # Configuración utilizada para entrenar
    ├── results.csv               # Métricas de entrenamiento por época
    └── weights/                  # Pesos del modelo entrenado
        ├── best.pt               # Mejores pesos obtenidos
        └── last.pt               # Pesos de la última época
```

## 🚀 Instalación y Uso

### Requisitos

Para ejecutar el código o utilizar el modelo, necesitas instalar la librería `ultralytics`:

```bash
pip install ultralytics
```

### Entrenamiento

El archivo `license_plate_detector.ipynb` contiene todos los pasos necesarios para reproducir el entrenamiento en Google Colab:

1. Montar Google Drive.
2. Copiar el dataset al entorno local de Colab.
3. Instalar dependencias.
4. Entrenar el modelo.
5. Guardar los resultados.

### Inferencia (Uso del modelo)

Para utilizar el modelo entrenado (`best.pt`) en nuevas imágenes o videos:

```python
from ultralytics import YOLO

# Cargar el modelo entrenado
model = YOLO('train3/weights/best.pt')

# Realizar predicción
results = model('ruta/a/tu/imagen.jpg')

# Mostrar resultados
results[0].show()
```
