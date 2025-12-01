# App de Incidencias de Tránsito

Aplicación móvil desarrollada en React Native con Expo para el registro y gestión de incidencias de tránsito y multas. La aplicación permite a los usuarios capturar matrículas mediante la cámara, obtener la ubicación GPS y registrar incidencias que se envían a un backend centralizado.

## Características

- **Autenticación**: Inicio de sesión seguro utilizando Firebase Authentication.
- **Reconocimiento de Matrículas**: Integración con cámara para capturar evidencias.
- **Geolocalización**: Obtención automática de coordenadas GPS para la incidencia.
- **Gestión de Incidencias**: Enviar datos de multas.
- **Historial**: Visualización de vehículos e incidencias (si aplica).

## Tecnologías Utilizadas

- **Frontend**: React Native, Expo
- **Navegación**: React Navigation
- **Servicios**: Firebase (Auth), Expo Location, Expo Camera, Expo Secure Store
- **HTTP Client**: Axios

## Requisitos Previos

- Node.js (versión LTS recomendada)
- npm o yarn
- Dispositivo físico con Expo Go o emulador (Android/iOS)
- Backend Spring Boot (para gestión de incidencias)
- Microservicio Python (para procesamiento de imágenes/OCR)

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd transito-app
   ```

2. Instalar dependencias:
   ```bash
   npm install
   ```

## Configuración

### Variables de Entorno

Este proyecto utiliza variables de entorno para manejar la configuración sensible y las direcciones de los servidores.

1. Copia el archivo de ejemplo:

   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` con tus propios valores:

   ```ini
   # Configuración de Firebase
   EXPO_PUBLIC_FIREBASE_API_KEY=tu_api_key
   EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=tu_proyecto.firebaseapp.com
   ...

   # Configuración de APIs (Backend)
   # IMPORTANTE: Reemplaza TU_IP_LOCAL con la IP de tu máquina en la red local (ej. 192.168.1.5)
   EXPO_PUBLIC_API_URL=http://TU_IP_LOCAL:8080/api
   EXPO_PUBLIC_PYTHON_URL=http://TU_IP_LOCAL:8000
   ```

### Firebase

La configuración de Firebase se carga automáticamente desde las variables de entorno. Asegúrate de crear un proyecto en Firebase y obtener las credenciales web.

## Ejecución

Para iniciar la aplicación en modo de desarrollo:

```bash
npx expo start
```

Escanea el código QR con la aplicación Expo Go en tu dispositivo móvil.

## Estructura del Proyecto

```
src/
  components/    # Componentes reutilizables
  config/        # Configuraciones (API, Firebase)
  context/       # Contextos de React (Estado global)
  screens/       # Pantallas de la aplicación
    CameraScreen.js
    ConfirmScreen.js
    HomeScreen.js
    LoginScreen.js
    MisVehiculosScreen.js
```
