from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import joblib,time,random

def start_chrome(headless=False):
    #opciones del navegador
    options = Options()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0')
    options.add_argument('--headless') if headless else options.add_argument('--start-maximized')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--no-proxy-server')
    options.add_argument('--disable-blink-features=AutomationContolled')
    options.add_experimental_option('excludeSwitches',['enable-automation','ignore-certificate-errors','enable-logging'])
    options.add_experimental_option('prefs',{'profile.default_content_settings_values.notifications':2,'intl.accept_languages':['es-ES','es'],'credentials_enable_service':False})
    driver = Chrome(options=options)

    return driver

def quit_driver(driver):
    driver.close()
    driver.quit()

def keys_sender(element,key):
    #para simular humanidad a la hora de enviar texto
    for letter in key:
        time.sleep(random.choice(range(1,5))/10)
        element.send_keys(letter)

def manual_login(driver,wait):
    driver.get('https://www.facebook.com')
    
    #correo
    try:
        correo_element = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@id="email"]')))
    except TimeoutException:
        quit_driver(driver)
        exit()
    keys_sender(correo_element,'nelly550ruiz@gmail.com')
    print('Correo: OK.')

    #password
    pass_element = driver.find_element(By.XPATH,'//input[@id="pass"]')
    keys_sender(pass_element,'Leon.990423')
    print('Password: OK.')

    #Boton de siguiente
    try:
        next_button = wait.until(ec.element_to_be_clickable((By.XPATH,"//button[@name='login']")))
    except TimeoutException:
        quit_driver(driver)
        exit()
    next_button.click()
    print('Enviando claves...')
    #por si tengo que poner el 2FA o algo:
    #time.sleep(30)

    #entrando a perfil
    breakpoint()
    try:    
        wait.until(ec.visibility_of_element_located((By.XPATH,'//a[@aria-label="Biografía de Paulo Leon"]')))
    except TimeoutException:
        quit_driver(driver)
        exit()

    print('Perfil: OK.\n\nLogiado manual.')
    #salvando cookies
    with open('face_cookies.joblib','wb') as file:
        joblib.dump(driver.get_cookies(),file)
    
    time.sleep(5)
    return driver

def login_face(headless=False,manual=False):
    #starting chrome
    driver = start_chrome()
    wait = WebDriverWait(driver,10)
    #para tests
    if manual: 
        return manual_login(driver,wait)
        
    driver.get('https://facebook.com/robots.txt')
    #checkando si hay cookies
    try:
        with open('face_cookies.joblib','rb') as file:
            cookies = joblib.load(file)
        for cookie in cookies: driver.add_cookie(cookie)
        driver.get('https://facebook.com')
        wait.until(ec.visibility_of_element_located((By.XPATH,'//a[@aria-label="Biografía de Paulo Leon"]')))
        print('Loguiado por cookies.')
        time.sleep(3)
    except OSError:
        driver = manual_login(driver,wait)
    except TimeoutException:
        driver = manual_login(driver,wait)
    
    return driver

if __name__ == '__main__':
    driver = login_face()
    input('Hablate ')
    quit_driver(driver)
    exit()

    

