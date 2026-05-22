import os
import shutil
import tempfile
import time
import unittest
import subprocess
import sys
from datetime import datetime, timedelta
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class TestSistemaReservas(unittest.TestCase):

    server_process = None

    @classmethod
    def setUpClass(cls):
        """Inicia el servidor Express y configura el navegador"""
        print("\n🚀 Iniciando servidor Express...")
        cls.server_process = subprocess.Popen(
            ['node', 'server.js'],
            cwd='/Users/hyrumpaz/Documents/Ing-De-Software/Sistema-de-reservas-academicas-automatizado',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)  # Esperar a que el servidor inicie

        # Crear un espacio en la base de datos
        print("📍 Creando espacios en la base de datos...")
        import sqlite3
        try:
            conn = sqlite3.connect('/Users/hyrumpaz/Documents/Ing-De-Software/Sistema-de-reservas-academicas-automatizado/academico.sqlite')
            cursor = conn.cursor()
            # Crear espacios
            espacios = [
                (1, 'Aula A', 'Aula', 30),
                (2, 'Aula B', 'Aula', 30),
                (3, 'Laboratorio 1', 'Laboratorio', 20),
            ]
            for espacio_id, nombre, tipo, capacidad in espacios:
                cursor.execute(
                    'INSERT OR IGNORE INTO espacios (id, nombre, tipo, capacidad) VALUES (?, ?, ?, ?)',
                    (espacio_id, nombre, tipo, capacidad)
                )
            conn.commit()
            conn.close()
            print("✅ Espacios creados")
        except Exception as e:
            print(f"⚠️  No se pudieron crear espacios: {e}")

        # Configurar opciones del navegador Chrome
        options = Options()
        cls.profile_dir = tempfile.mkdtemp()
        options.add_argument(f'--user-data-dir={cls.profile_dir}')
        options.add_argument('--remote-debugging-port=0')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Usar webdriver-manager para gestionar ChromeDriver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.implicitly_wait(10)
        print("✅ Servidor iniciado y navegador configurado")

    def test_01_crear_usuario(self):
        """Test 1: Crear un nuevo usuario en el sistema"""
        driver = self.driver
        driver.get('http://localhost:3000')
        
        print("\n👤 Test 1: Creando usuario...")
        
        # Rellenar formulario de usuario
        nombre_input = driver.find_element(By.ID, 'nombreUsuario')
        nombre_input.clear()
        nombre_input.send_keys('Hyrum Paz')
        
        email_input = driver.find_element(By.ID, 'emailUsuario')
        email_input.clear()
        email_input.send_keys(f'hpaz{int(time.time())}@miumg.edu')
        
        rol_select = Select(driver.find_element(By.ID, 'rolUsuario'))
        rol_select.select_by_value('estudiante')
        
        # Hacer clic en el botón de envío
        submit_button = driver.find_element(By.XPATH, '//*[@id="formUsuario"]//button[@type="submit"]')
        submit_button.click()
        
        # Esperar a la respuesta
        time.sleep(2)
        
        # Verificar que se creó el usuario
        respuesta = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'respuestaUsuario'))
        )
        
        resultado = respuesta.text
        self.assertIn('Usuario creado', resultado, "El usuario no fue creado correctamente")
        print(f"✅ Usuario creado exitosamente: {resultado}")

    def test_02_consultar_disponibilidad(self):
        """Test 2: Consultar disponibilidad de espacios"""
        driver = self.driver
        
        print("\n📅 Test 2: Consultando disponibilidad...")
        
        # Calcular fecha para mañana
        tomorrow = datetime.now() + timedelta(days=1)
        fecha_formato = tomorrow.strftime('%Y-%m-%d')
        
        # Scroll down para ver el formulario de disponibilidad
        disponibilidad_section = driver.find_element(By.XPATH, "//h2[contains(text(), '📅')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", disponibilidad_section)
        time.sleep(0.5)
        
        # Rellenar formulario de disponibilidad
        fecha_input = driver.find_element(By.ID, 'fechaDisponibilidad')
        # Usar JavaScript para establecer el valor directamente
        driver.execute_script(f"arguments[0].value = '{fecha_formato}';", fecha_input)
        driver.execute_script(f"arguments[0].dispatchEvent(new Event('change', {{ bubbles: true }}));", fecha_input)
        time.sleep(0.5)
        
        espacio_input = driver.find_element(By.ID, 'espacioIdDisponibilidad')
        espacio_input.clear()
        espacio_input.send_keys('1')
        
        # Hacer clic en el botón de consulta
        consultar_button = driver.find_element(By.XPATH, '//button[@class="btn btn-secondary"]')
        consultar_button.click()
        
        # Esperar a la respuesta
        time.sleep(2)
        
        # Verificar que se consultó la disponibilidad
        respuesta = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'respuestaDisponibilidad'))
        )
        
        resultado = respuesta.text
        self.assertIn('disponible', resultado.lower(), "No se pudo consultar la disponibilidad")
        print(f"✅ Disponibilidad consultada: {resultado}")

    def test_03_crear_reserva(self):
        """Test 3: Crear una nueva reserva"""
        driver = self.driver
        
        print("\n🎫 Test 3: Creando reserva...")
        
        # Calcular fecha para mañana
        tomorrow = datetime.now() + timedelta(days=1)
        fecha_formato = tomorrow.strftime('%Y-%m-%d')
        
        print(f"   Fecha a usar: {fecha_formato}")
        
        # Usar JavaScript para hacer la petición POST directamente al servidor
        print("   Enviando petición POST al servidor...")
        
        resultado_js = driver.execute_script(f"""
        let respuesta_creada = false;
        let respuesta_texto = '';
        
        fetch('/reservar', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{
                usuario_id: 1,
                espacio_id: 1,
                fecha: '{fecha_formato}',
                hora_inicio: '09:00',
                hora_fin: '11:00'
            }})
        }})
        .then(response => response.json())
        .then(data => {{
            respuesta_texto = JSON.stringify(data);
            respuesta_creada = true;
            console.log('Respuesta:', data);
        }})
        .catch(error => {{
            respuesta_texto = 'Error: ' + error.message;
            console.error('Error:', error);
        }});
        
        // Esperar a que se complete la petición (máx 10 segundos)
        let inicio = Date.now();
        while (!respuesta_creada && Date.now() - inicio < 10000) {{
            // Esperar un poco
        }}
        
        return respuesta_texto;
        """)
        
        print(f"   Respuesta del servidor: {resultado_js}")
        
        # Esperar un poco más para que se actualice la BD
        time.sleep(2)
        
        # Verificar que se creó la reserva consultando la base de datos
        print("   Verificando en la base de datos...")
        import sqlite3
        try:
            conn = sqlite3.connect('/Users/hyrumpaz/Documents/Ing-De-Software/Sistema-de-reservas-academicas-automatizado/academico.sqlite')
            cursor = conn.cursor()
            
            # Contar reservas para el usuario y espacio especificado
            cursor.execute(
                'SELECT COUNT(*) FROM reservas WHERE usuario_id = 1 AND espacio_id = 1 AND fecha = ?',
                (fecha_formato,)
            )
            count = cursor.fetchone()[0]
            
            # También obtener los detalles de la reserva si existe
            cursor.execute(
                'SELECT id, usuario_id, espacio_id, fecha, hora_inicio, hora_fin FROM reservas WHERE usuario_id = 1 AND espacio_id = 1 AND fecha = ?',
                (fecha_formato,)
            )
            reserva = cursor.fetchone()
            conn.close()
            
            if count > 0:
                print(f"   ✅ Reserva encontrada en la base de datos")
                print(f"   ID Reserva: {reserva[0]}, Usuario: {reserva[1]}, Espacio: {reserva[2]}")
                print(f"   Fecha: {reserva[3]}, Horario: {reserva[4]} - {reserva[5]}")
                print(f"✅ Reserva creada exitosamente")
            else:
                # Si no está en BD, intentar ver la respuesta del servidor
                self.assertIn('exitosa', resultado_js.lower() or 'error', 
                    f"La reserva no fue creada. Estado BD: {count} reservas. Respuesta: {resultado_js}")
        except Exception as e:
            print(f"   Error verificando BD: {str(e)}")
            raise

    @classmethod
    def tearDownClass(cls):
        """Cierra el navegador y detiene el servidor"""
        print("\n🛑 Finalizando tests...")
        cls.driver.quit()
        shutil.rmtree(cls.profile_dir, ignore_errors=True)
        
        # Detener el servidor Express
        if cls.server_process:
            cls.server_process.terminate()
            cls.server_process.wait(timeout=5)
        
        print("✅ Servidor detenido")


if __name__ == "__main__":
    # Crear directorio de reportes si no existe
    os.makedirs('reportes', exist_ok=True)
    
    print("=" * 60)
    print("🎓 SISTEMA DE RESERVAS ACADÉMICAS - PRUEBAS AUTOMATIZADAS")
    print("=" * 60)
    
    # Ejecutar tests con reporte HTML
    unittest.main(
        verbosity=2,
        testRunner=HTMLTestRunner(
            output='reportes',
            report_name='reporte-reservas'
        ),
        exit=False
    )
