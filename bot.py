from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from email.mime.text import MIMEText
import os

# ✉️ Función para enviar el correo
def enviar_mail(disponibles):
    msg = MIMEText(f"Hay {disponibles} prácticas disponibles en PracticaVial")
    msg["Subject"] = "🚘 Prácticas disponibles"
    msg["From"] = os.getenv("GMAIL_USER")
    msg["To"] = os.getenv("GMAIL_USER")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
        server.send_message(msg)

# Configuración del navegador sin interfaz
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# Accede a la web
driver.get("https://app.practicavial.com/")
time.sleep(2)

# Login
email_input = driver.find_element(By.ID, "username_input")
password_input = driver.find_element(By.NAME, "password")

email_input.send_keys(os.getenv("PV_USER"))       # Usa variable de entorno
password_input.send_keys(os.getenv("PV_PASS"))    # Usa variable de entorno
password_input.send_keys(Keys.RETURN)

time.sleep(2)

# Ir a calendario
driver.get("https://app.practicavial.com/mi-calendario")
time.sleep(2)

# Revisar prácticas disponibles
try:
    disponibles = driver.find_element(By.CLASS_NAME, "available-example").text
    disponibles = int(disponibles.strip())
    print(f"Hay {disponibles} prácticas disponibles")

    if disponibles >=0:
        enviar_mail(disponibles)

except Exception as e:
    print("Error al revisar disponibilidad:", e)

driver.quit()
