const sqlite3 = require('sqlite3').verbose();

// Creamos o abrimos el archivo de la base de datos
const db = new sqlite3.Database('./academico.sqlite', (err) => {
    if (err) {
        console.error("Error al abrir la base de datos:", err.message);
    } else {
        console.log("Conectado a la base de datos SQLite.");
        crearTablas();
    }
});

function crearTablas() {
    db.serialize(() => {
        // 1. Tabla de Usuarios
        db.run(`CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            rol TEXT CHECK(rol IN ('estudiante', 'docente', 'admin'))
        )`);

        // 2. Tabla de Espacios
        db.run(`CREATE TABLE IF NOT EXISTS espacios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT,
            capacidad INTEGER
        )`);

        // 3. Tabla de Reservas (La que amarra todo)
        db.run(`CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            espacio_id INTEGER,
            fecha TEXT,
            hora_inicio TEXT,
            hora_fin TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (espacio_id) REFERENCES espacios(id)
        )`);
        
        console.log("Tablas verificadas/creadas con éxito.");
    });
}

module.exports = db;