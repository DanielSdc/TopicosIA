# 🚦 Sistema Integral de Gestión de Incidencias Vehiculares

Este repositorio contiene una solución completa para la gestión, control y reporte de incidencias de estacionamiento. El sistema integra una aplicación móvil para la captura de evidencias, un servicio de Inteligencia Artificial para el reconocimiento automático de matrículas (ANPR) y un backend robusto para la administración de datos y reglas de negocio.

## 📂 Estructura del Proyecto

El sistema se divide en tres módulos principales, cada uno en su propia carpeta:

### 1. 📱 Aplicación Móvil (`transito-app`)

Aplicación desarrollada en **React Native con Expo**.

- **Función:** Permite a los usuarios/oficiales iniciar sesión, capturar fotografías de vehículos, obtener la ubicación GPS automática y registrar incidencias.
- **Características:** Integración con cámara, geolocalización y autenticación con Firebase.

### 2. 🧠 Servicio de IA (`License_plate_detector`)

API REST construida con **FastAPI** y **Python**.

- **Función:** Procesa las imágenes enviadas por la app para detectar y leer la matrícula del vehículo.
- **Tecnologías:** Utiliza **YOLOv11** para la detección de objetos y **PaddleOCR** para el reconocimiento de caracteres.

### 3. 🛡️ Backend (`IncidenciasEstacionamiento`)

API REST desarrollada con **Spring Boot (Java)**.

- **Función:** Gestiona usuarios, propietarios, automóviles e incidencias.
- **Lógica de Negocio:** Implementa reglas automáticas, como el bloqueo de la "Tarjeta de Pase" de un propietario si acumula **3 o más incidencias**.
- **Seguridad:** Autenticación mediante Tokens JWT y Firebase.

### 4. 🏋️ Entrenamiento del Modelo (`model_train`)

Recursos utilizados para el entrenamiento y ajuste del modelo de Inteligencia Artificial.

- **Función:** Documentar y ejecutar el proceso de entrenamiento del modelo de detección de objetos.
- **Contenido:** Jupyter Notebook (`license_plate_detector.ipynb`) para entrenar **YOLOv11**.
- **Resultados:** Contiene los pesos resultantes (`best.pt`) y las métricas de rendimiento en la carpeta `train3/`.

---

## 🚀 Flujo de Trabajo General

1.  **Captura:** El usuario toma una foto de un vehículo usando la **App Móvil**.
2.  **Procesamiento:** La imagen se envía al **Servicio de IA**, que devuelve el número de matrícula detectado.
3.  **Confirmación:** El usuario valida los datos (matrícula y ubicación).
4.  **Registro:** La incidencia se envía al **Backend**, donde se guarda y se verifica si el propietario debe ser sancionado (bloqueo de acceso).

---

## 🛠️ Tecnologías Principales

| Módulo      | Tecnologías Clave                                               |
| :---------- | :-------------------------------------------------------------- |
| **Móvil**   | React Native, Expo, Axios, Firebase Auth                        |
| **IA**      | Python, FastAPI, YOLOv11, PaddleOCR, PyTorch                    |
| **Backend** | Java 21, Spring Boot 3, Spring Security, Spring Data JPA, Maven |
| **Train**   | Jupyter Notebook, Python, YOLOv11                               |

---

## 🏁 Cómo Iniciar el Proyecto

Para ejecutar el sistema completo, se recomienda levantar los servicios en el siguiente orden:

1.  **Backend (Spring Boot):**
    ```bash
    cd IncidenciasEstacionamiento
    ./mvnw spring-boot:run
    ```
2.  **Servicio de IA (Python):**
    ```bash
    cd License_plate_detector
    # Activar entorno virtual si es necesario
    uvicorn app:app --reload
    ```
3.  **Aplicación Móvil (Expo):**
    ```bash
    cd transito-app
    npm start
    ```

> **Nota:** Asegúrate de configurar las variables de entorno y las credenciales de Firebase en cada proyecto individualmente según sus propios archivos `README.md`.
