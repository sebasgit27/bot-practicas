
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import smtplib
from email.mime.text import MIMEText
import os
#sebaslondotabor@gmail.com
# ✉️ Función para enviar el correo
def enviar_mail(disponibles):
    msg = MIMEText(f"Hay {disponibles} prácticas disponibles en PracticaVial")
    msg["Subject"] = "🚘 Prácticas disponibles"
    msg["From"] = os.getenv("GMAIL_USER")
    msg["To"] = os.getenv("GMAIL_USER")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
        server.send_message(msg)


# Configura el WebDriver
driver = webdriver.Chrome()  # Asegúrate de que chromedriver esté en tu PATH
driver.get("https://app.practicavial.com/")

# Espera a que la página cargue completamente
time.sleep(2)

# Encuentra los campos de correo electrónico y contraseña e ingresa tus credenciales
email_input = driver.find_element(By.ID, "username_input")  # Ajusta según el atributo 'name' real
password_input = driver.find_element(By.NAME, "password")  # Ajusta según el atributo 'name' real

email_input.send_keys("sebaslondotabor@gmail.com")
password_input.send_keys("7ikrL")
password_input.send_keys(Keys.RETURN)

# Espera a que la sesión se inicie y la página redirija
time.sleep(2)

# Ahora estás autenticado y puedes navegar a la página de prácticas
driver.get("https://app.practicavial.com/mi-calendario")
time.sleep(2)

# Aquí puedes agregar el código para verificar la disponibilidad de prácticas
disponibles = driver.find_element(By.CLASS_NAME, "available-example").text
disponibles = int(disponibles.strip())  

if disponibles >= 0:
    enviar_mail(disponibles)
    # Aquí más adelante agregaremos lógica para reservar automáticamente

time.sleep(2)
# No olvides cerrar el navegador al finalizar
driver.quit()
