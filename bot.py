from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
import os

def enviar_mail(disponibles):
    msg = MIMEText(f"Hay {disponibles} prácticas disponibles en PracticaVial")
    msg["Subject"] = "🚘 Prácticas disponibles"
    msg["From"] = os.getenv("GMAIL_USER")
    msg["To"] = os.getenv("GMAIL_USER")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
        server.send_message(msg)

# Configuración del navegador
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acceso a la web
    driver.get("https://app.practicavial.com/")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username_input")))

    # Login
    email_input = driver.find_element(By.ID, "username_input")
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys(os.getenv("PV_USER"))
    password_input.send_keys(os.getenv("PV_PASS"))
    password_input.send_keys(Keys.RETURN)

    # Ir al calendario
    WebDriverWait(driver, 15).until(EC.url_contains("mi-calendario"))
    
    # Revisar disponibilidad
    try:
        disponibles_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "available-example"))
        )
        disponibles = int(disponibles_element.text.strip())
        print(f"Prácticas disponibles: {disponibles}")
        
        if disponibles > 0:
            enviar_mail(disponibles)
    except:
        disponibles = 0
        print("No se encontraron prácticas disponibles")

except Exception as e:
    print("Error durante la ejecución:", e)
finally:
    driver.quit()
