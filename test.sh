#!/bin/bash

echo "=========================================="
echo "🎓 SISTEMA DE RESERVAS ACADÉMICAS"
echo "Instalando dependencias..."
echo "=========================================="

# Instalar dependencias de Python
pip3 install -r requirements.txt > /dev/null 2>&1

# Limpiar la base de datos anterior
rm -f academico.sqlite

echo ""
echo "=========================================="
echo "🚀 Ejecutando pruebas..."
echo "=========================================="

# Ejecutar las pruebas
python3 test_reservas.py

echo ""
echo "=========================================="
echo "✅ Pruebas completadas"
echo "Los reportes se encuentran en: ./reportes/"
echo "=========================================="
