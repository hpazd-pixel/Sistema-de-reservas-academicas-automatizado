# Sistema de Reservas Académicas

Un sistema de reservas académicas construido con Node.js y Express para gestionar la disponibilidad de espacios, usuarios y reservas en ambientes educativos.

---

## 📋 Requisitos Previos

Asegurar de tener instalados en la máquina:

- **Node.js** (versión 12 o superior) - [Descargar aquí](https://nodejs.org/)
- **npm** (viene incluido con Node.js)

Para verificar que están instalados, ejecute en la terminal:

```bash
node --version
npm --version
```

---

## 🛠️ Instalación

### 1. Clonar o descargar el proyecto

```bash
cd ruta/al/proyecto
```

### 2. Instalar las dependencias

Ejecutar el siguiente comando en la carpeta del proyecto:

```bash
npm install
```

Luego, aplica los arreglos de seguridad:

```bash
npm audit fix
```

Esto instalará las siguientes dependencias:

- **express**: Framework web para Node.js
- **sqlite3**: Base de datos SQLite para almacenar usuarios, espacios y reservas

---

## 🚀 Ejecución del Proyecto

Para iniciar el servidor, ejecutar:

```bash
npm start
```

O si prefieres:

```bash
node server.js
```

Si todo va bien, se debe mostrar:

```
Conectado a la base de datos SQLite.
Servidor corriendo en http://localhost:3000
```

Luego abrir el navegador y acceder a: **http://localhost:3000**

Se mostrará una interfaz gráfica amigable para usar el sistema.

---

## 🧪 Pruebas Automatizadas (Con Selenium)

El proyecto incluye una **suite completa de pruebas automatizadas** que valida automáticamente todo el sistema.

### Requisitos para Tests
- Python 3.9+
- Google Chrome instalado

### Instalación de Dependencias de Tests

```bash
pip3 install -r requirements.txt
```

### Ejecutar las Pruebas

**Opción 1: Con npm**
```bash
npm start
```

**Opción 2: Script ejecutable**
```bash
./test.sh
```

**Opción 3: Directamente con Python**
```bash
python3 test_reservas.py
```

### Pruebas Incluidas

✅ **Test 1: Crear Usuario** - Registra un usuario en el sistema
✅ **Test 2: Consultar Disponibilidad** - Verifica horarios disponibles
✅ **Test 3: Crear Reserva** - Crea una reserva de espacio académico

### Características de Tests

- 🤖 Automatización completa con Selenium WebDriver
- 📊 Reportes HTML automáticos en `/reportes/`
- ✔️ Validación contra base de datos SQLite
- 🌐 Navegador real (no headless) para visualizar
- ⏱️ Tiempos de ejecución por cada prueba
- 📋 Detalles completos de errores si ocurren

### Archivos de Tests

- `test_reservas.py` - Suite de pruebas Selenium
- `requirements.txt` - Dependencias Python (Selenium, pyunitreport)
- `test.sh` / `run_tests.sh` - Scripts ejecutables
- `README_TESTS.md` - Documentación detallada de tests

---

## 📂 Estructura del Proyecto

```
Sistema-de-reservas-academicas/
├── server.js                    # Servidor principal (Express)
├── database.js                  # Configuración de la base de datos (SQLite)
├── package.json                 # Dependencias y configuración del proyecto
├── public/                      # Archivos estáticos (Frontend)
│   ├── index.html              # Interfaz gráfica principal
│   └── style.css               # Estilos CSS
├── node_modules/                # Dependencias instaladas (generado por npm)
└── README.md                    # Este archivo
```

---

## 🎨 Interfaz Gráfica

El proyecto incluye una interfaz web moderna y responsiva (en `public/index.html`) con tres secciones principales:

### 1. **Crear Usuario** 👤
Permite registrar nuevos usuarios en el sistema con:
- Nombre completo
- Email único
- Rol (Estudiante, Docente)

### 2. **Consultar Disponibilidad** 📅
Verifica qué horarios están ocupados en un espacio específico:
- Seleccione la fecha
- Ingrese el ID del espacio
- El sistema muestra los horarios ocupados

### 3. **Crear Reserva** 🎫
Realiza nuevas reservas de espacios académicos:
- ID del usuario
- ID del espacio
- Fecha de la reserva
- Hora de inicio y fin
- El sistema valida automáticamente conflictos de horarios

**La interfaz es completamente interactiva y muestra mensajes de éxito o error** ✅

---

## 📡 Endpoints Disponibles

Si prefieres usar la API directamente (con Postman, curl, etc.):

### 1. Crear Usuario
**POST** `/usuarios`

```json
{
  "nombre": "Hyrum paz",
  "email": "hpazd@miumg.edu",
  "rol": "estudiante"
}
```

### 2. Consultar Disponibilidad
**GET** `/disponibilidad?fecha=2026-05-17&espacio_id=1`

Responde con los horarios ocupados para un espacio en una fecha específica.

### 3. Realizar Reserva
**POST** `/reservar`

```json
{
  "usuario_id": 1,
  "espacio_id": 1,
  "fecha": "2026-05-17",
  "hora_inicio": "14:00",
  "hora_fin": "16:00"
}
```

El sistema valida automáticamente que no haya conflictos de horarios.

---

## 💡 Notas Importantes

- La base de datos se crea automáticamente al iniciar el servidor
- El servidor corre en el **puerto 3000** por defecto
- Usa **SQLite3**, una base de datos embebida (no requiere servidor separado)
- La interfaz gráfica se sirve automáticamente desde la carpeta `public/`
- Todos los cambios en HTML/CSS se reflejan inmediatamente sin reiniciar (sirve archivos estáticos)
- La API responde en formato JSON y valida todos los datos automáticamente

---

## 📝 Cambios Recientes

✨ **v2.0.0** - Suite de Pruebas Automatizadas con Selenium
- Implementado framework de pruebas automatizadas con Selenium WebDriver
- Crear 3 tests automatizados (usuario, disponibilidad, reserva)
- Generación automática de reportes HTML
- Integración de webdriver-manager para gestión de ChromeDriver
- Documentación completa en README_TESTS.md
- Scripts ejecutables (test.sh, run_tests.sh)
- Validación contra base de datos SQLite

✨ **v1.1.0** - Interfaz Gráfica Mejorada
- Creada carpeta `public/` con interfaz web moderna
- Actualizado `index.html` con formularios interactivos
- Actualizado `style.css` con estilos responsivos
- Configurado Express para servir archivos estáticos
- Actualizado `package.json` con Express y scripts de inicio
- Implementado validación de formularios en el frontend

---

## 🐛 Solución de Problemas

**Error: "Cannot find module 'express'"**
- Solución: Ejecutar `npm install` de nuevo

**Error: "npm audit fix" falla**
- Solución: Ejecutar `npm install` primero, luego `npm audit fix`

**Puerto 3000 ya está en uso**
- Solución: Cambiar el puerto en `server.js` (busca `const PORT = 3000`) o cerrar la aplicación que usa ese puerto

**Error de base de datos**
- Solución: Elimina el archivo `academico.sqlite` si existe y reinicia el servidor para recrearlo

**La interfaz no carga (error 404)**
- Solución: Verificar que la carpeta `public/` existe con los archivos `index.html` y `style.css`
- Asegurarse de que en `server.js` está la línea: `app.use(express.static('public'));`

**Cambios en HTML/CSS no se reflejan**
- Solución: Recarga la página con F5 o Ctrl+Shift+R (limpia caché)

### Tests Automatizados

**Error: "ChromeDriver no encontrado"**
- Solución: `pip3 install --upgrade webdriver-manager`

**Error: "No module named 'selenium'"**
- Solución: `pip3 install -r requirements.txt`

**Los tests fallan o se cuelgan**
- Solución: Verificar que no hay otra instancia del servidor corriendo
- Ejecutar: `lsof -ti:3000 | xargs kill -9`

**Base de datos bloqueada en tests**
- Solución: `rm -f academico.sqlite` y ejecutar los tests nuevamente

---

## 👨‍💻 Autor

Hyrum Paz
