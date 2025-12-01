# 🚗 Sistema de Gestión de Incidencias de Estacionamiento

API REST desarrollada con **Spring Boot** para la gestión de control de acceso vehicular, registro de propietarios y reporte de incidencias (multas) dentro de un estacionamiento.

El sistema integra seguridad mediante **Firebase Authentication** y cuenta con lógica de negocio automatizada para el bloqueo de tarjetas de acceso.

## 📋 Características Principales

- **Gestión de Usuarios:** Registro y autenticación segura mediante Tokens JWT de Firebase.
- **Vinculación Inteligente:** Relación entre Usuarios, Propietarios y Automóviles.
- **Reporte de Incidencias:** Registro de faltas con geolocalización (latitud/longitud) y fecha.
- **Regla de Negocio Automatizada:**
  - El sistema monitorea el historial de incidencias de cada propietario.
  - 🛑 **Bloqueo Automático:** Si un propietario acumula **3 o más incidencias**, su "Tarjeta de Pase" se deshabilita automáticamente.
- **Consulta de Historial:** Endpoints para ver incidencias recibidas (mis multas) y enviadas (reportes hechos por mí).

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Java 21+
- **Framework:** Spring Boot 3.x
- **Seguridad:** Spring Security + Firebase Admin SDK
- **Base de Datos:** MySQL (JPA/Hibernate)
- **Construcción:** Maven

## ⚙️ Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

1.  **Java JDK 21** o superior.
2.  **Maven** .
3.  Una cuenta de **Firebase** con un proyecto activo.

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

### 2. Configurar Firebase

Para que la autenticación funcione, necesitas las credenciales de tu proyecto Firebase:

1.  Ve a la consola de Firebase > Configuración del Proyecto > Cuentas de servicio.
2.  Genera una nueva clave privada (archivo `.json`).
3.  Renombra el archivo a `firebase_service.json`.
4.  Colócalo en la carpeta: `src/main/resources/`.

### 3. Configurar Base de Datos

El proyecto utiliza variables de entorno para la conexión a la base de datos. Puedes configurarlas en tu sistema operativo o IDE, o dejar los valores por defecto para desarrollo local.

**Variables de Entorno:**

| Variable      | Descripción          | Valor por Defecto (Local)                 |
| :------------ | :------------------- | :---------------------------------------- |
| `DB_URL`      | URL de conexión JDBC | `jdbc:mysql://127.0.0.1:3306/incidencias` |
| `DB_USERNAME` | Usuario de la BD     | `root`                                    |
| `DB_PASSWORD` | Contraseña de la BD  | `12345`                                   |

**Ejemplo de configuración en IntelliJ / Eclipse:**
Agrega estas variables en la configuración de "Run/Debug Configurations" -> "Environment variables".

**Ejemplo en terminal (Linux/Mac):**

```bash
export DB_USERNAME=mi_usuario
export DB_PASSWORD=mi_password
./mvnw spring-boot:run
```

### 4. Ejecutar la Aplicación

Usa el wrapper de Maven para correr el proyecto:

```powershell
./mvnw spring-boot:run
```

## 📖 Documentación de la API (Swagger)

Una vez que la aplicación esté corriendo, puedes acceder a la documentación interactiva y probar los endpoints directamente desde el navegador:

🔗 **URL:** `http://localhost:8080/swagger-ui/index.html`

> **Nota:** Para probar los endpoints protegidos en Swagger, necesitarás obtener un Token JWT válido de tu cliente Firebase y usar el botón "Authorize".

## 🧩 Estructura del Proyecto

- `controller`: Controladores REST (Endpoints).
- `service`: Lógica de negocio (Reglas de bloqueo, validaciones).
- `repository`: Acceso a datos (JPA).
- `model`: Entidades de la base de datos.
- `dto`: Objetos de transferencia de datos (Request/Response).
- `security`: Configuración de filtros JWT y Firebase.
- `config`: Configuraciones globales (Swagger, Firebase).

## 🛡️ Seguridad

El proyecto utiliza un filtro personalizado `JwtAuthenticationFilter` que intercepta las peticiones HTTP, extrae el token `Bearer` y lo valida contra los servidores de Google Firebase antes de permitir el acceso a los recursos protegidos.
