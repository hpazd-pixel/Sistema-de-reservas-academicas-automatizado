const express = require('express');
const db = require('./database'); // Importamos tu conexión
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static('public')); // Servir archivos estáticos (HTML, CSS, JS)

// --- RUTA PRINCIPAL ---
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// --- 1. ENDPOINT: REGISTRO DE USUARIOS (Para tener con quién reservar) ---
app.post('/usuarios', (req, res) => {
    const { nombre, email, rol } = req.body;
    const sql = `INSERT INTO usuarios (nombre, email, rol) VALUES (?, ?, ?)`;
    
    db.run(sql, [nombre, email, rol], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ mensaje: "Usuario creado", id: this.lastID });
    });
});

// --- 2. ENDPOINT: CONSULTAR DISPONIBILIDAD (GET) ---
app.get('/disponibilidad', (req, res) => {
    const { fecha, espacio_id } = req.query;
    const sql = `SELECT hora_inicio, hora_fin FROM reservas WHERE fecha = ? AND espacio_id = ?`;

    db.all(sql, [fecha, espacio_id], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ 
            mensaje: `Horarios ocupados para el espacio ${espacio_id} el ${fecha}`,
            ocupado: rows 
        });
    });
});

// --- 3. ENDPOINT: CREAR RESERVA (POST) CON VALIDACIÓN ---
app.post('/reservar', (req, res) => {
    const { usuario_id, espacio_id, fecha, hora_inicio, hora_fin } = req.body;

    // VALIDACIÓN CRÍTICA: ¿Se cruza con otra reserva?
    const sqlCheck = `
        SELECT * FROM reservas 
        WHERE espacio_id = ? AND fecha = ? 
        AND (
            (hora_inicio < ? AND hora_fin > ?)
        )`;

    db.get(sqlCheck, [espacio_id, fecha, hora_fin, hora_inicio], (err, row) => {
        if (row) {
            return res.status(400).json({ error: "Choque de horarios. El espacio ya está ocupado." });
        }

        // Si no hay choque, insertamos
        const sqlInsert = `INSERT INTO reservas (usuario_id, espacio_id, fecha, hora_inicio, hora_fin) VALUES (?, ?, ?, ?, ?)`;
        db.run(sqlInsert, [usuario_id, espacio_id, fecha, hora_inicio, hora_fin], function(err) {
            if (err) return res.status(500).json({ error: err.message });
            res.json({ mensaje: "Reserva exitosa", id: this.lastID });
        });
    });
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});