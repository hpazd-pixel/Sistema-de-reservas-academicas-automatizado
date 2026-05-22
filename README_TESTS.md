# 🎓 Sistema de Reservas Académicas - Pruebas Automatizadas

## Descripción del Proyecto

Sistema automatizado de pruebas para un sistema de reservas académicas universitario, construido con:
- **Backend**: Node.js + Express.js
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Base de Datos**: SQLite
- **Testing**: Selenium + Python (unittest + HTMLTestRunner)

## Características Principales

✅ **Test 1**: Crear usuario automáticamente
✅ **Test 2**: Consultar disponibilidad de espacios
✅ **Test 3**: Crear reserva de espacios (en desarrollo)

Genera reportes HTML automáticos con los resultados de las pruebas.

## Instalación

### 1. Instalar dependencias de Node.js
```bash
npm install
```

### 2. Instalar dependencias de Python
```bash
pip3 install -r requirements.txt
```

## Uso

### Ejecutar todas las pruebas:
```bash
npm start
```
o
```bash
./test.sh
```

### Ejecutar solo el servidor (sin pruebas):
```bash
npm run server
```

## Estructura de Archivos

```
.
├── server.js                 # Servidor Express
├── database.js              # Configuración SQLite
├── test_reservas.py         # Suite de pruebas Selenium
├── requirements.txt         # Dependencias Python
├── package.json            # Dependencias Node.js
├── public/
│   ├── index.html          # Interfaz web
│   └── style.css           # Estilos
└── reportes/               # Reportes HTML generados
```

## Endpoints del API

### 1. Crear Usuario
```bash
POST /usuarios
Body: { "nombre": "string", "email": "string", "rol": "estudiante|docente" }
```

### 2. Consultar Disponibilidad
```bash
GET /disponibilidad?fecha=YYYY-MM-DD&espacio_id=1
```

### 3. Crear Reserva
```bash
POST /reservar
Body: { 
  "usuario_id": 1, 
  "espacio_id": 1, 
  "fecha": "YYYY-MM-DD",
  "hora_inicio": "HH:MM",
  "hora_fin": "HH:MM"
}
```

## Estructura de Pruebas

### setUpClass
- Inicia el servidor Express en puerto 3000
- Configura el navegador Chrome con opciones de seguridad
- Crea espacios iniciales en la base de datos

### test_01_crear_usuario
Verifica la creación de usuarios a través de la interfaz

### test_02_consultar_disponibilidad
Verifica la consulta de horarios disponibles para espacios

### test_03_crear_reserva
Verifica la creación de reservas (con validación de conflictos de horarios)

### tearDownClass
- Cierra el navegador
- Detiene el servidor
- Limpia directorios temporales

## Resultados de Pruebas

Los reportes HTML se generan automáticamente en `/reportes/`

Incluyen:
- Estado de cada prueba (✅ OK / ❌ FAILED)
- Tiempos de ejecución
- Mensajes de error detallados
- Captura de pantalla (si corresponde)

## Configuración del Navegador

El script utiliza ChromeDriver gestionado automáticamente por `webdriver-manager`:
- Modo no headless (para visualizar la ejecución)
- Sandbox deshabilitado
- Debugging remoto activado
- GPU deshabilitada para mejor rendimiento

## Notas Importantes

1. **Base de Datos**: Se crea automáticamente con esquema SQLite
2. **Espacios**: Se crean automáticamente en cada ejecución de pruebas
3. **Usuarios**: Cada prueba crea usuarios con IDs únicos mediante timestamps
4. **Fechas**: Se usan fechas futuras para evitar conflictos

## Requisitos del Sistema

- Python 3.9+
- Node.js 14+
- Google Chrome instalado
- macOS (con ligeros cambios funciona en Linux/Windows)

## Archivos Generados

- `academico.sqlite`: Base de datos SQLite
- `reportes/`: Carpeta con reportes HTML
- `node_modules/`: Dependencias de Node.js
- `chromedriver`: Descargado automáticamente por webdriver-manager

## Troubleshooting

### "ChromeDriver no encontrado"
```bash
pip3 install --upgrade webdriver-manager
```

### "Puerto 3000 ya está en uso"
Matar el proceso:
```bash
lsof -ti:3000 | xargs kill -9
```

### "Base de datos bloqueada"
Eliminar la base de datos:
```bash
rm -f academico.sqlite
```

## Desarrollo Futuro

- [ ] Integración con CI/CD (GitHub Actions)
- [ ] Pruebas de rendimiento
- [ ] Pruebas de seguridad
- [ ] Parallelización de pruebas
- [ ] Capturas de pantalla en fallos
- [ ] Métricas de cobertura

## Licencia

ISC

## Autor

Hyrum Paz

---

**Última actualización**: 18 de mayo de 2026
