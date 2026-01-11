"""Script para automatizar el login en facebook mediante email y password.Se le puede pasar cookies.
Mas adelante se le agregara la parte de loguearse en gmail para verificar correo."""

from datetime import datetime as dt
import json,time,random,os
while 1:
    try:
        from seleniumbase import Driver
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as ec
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import TimeoutException
        break
    except:
        os.system('pip install selenium')
        os.system('pip install seleniumbase')


def errors_screenshoter(driver):
	"""Para guardar un screenshot del punto donde dio un error."""
	#si no existe la carpeta de errores la crea
	if not os.path.isdir('Errors'):
		os.mkdir('Errors')
	curr_time = dt.now()
	stringuinized = curr_time.strftime('%Y-%m-%d_%H-%M-%S') #formato year-month-days-hour-minute-secs
	driver.save_screenshot('Errors' + os.sep + 'Error_' + stringuinized + '.png')

def keys_sender(element,key):
    """Para simular humanidad a la hora de enviar texto"""
    for letter in key:
        time.sleep(random.randint(1,5)/10)
        element.send_keys(letter)

def manual_login(email,password,driver,wait):
    """Para loguearse manual en el face con correo y password."""
    driver.get('https://www.facebook.com')
    
    #correo
    try:
        correo_element = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@id="email"]')))
    except TimeoutException:
        errors_screenshoter(driver)
        print('Algo fue mal al cargar el correo')
        return 'bad'
    keys_sender(correo_element,email)
    #password
    pass_element = driver.find_element(By.XPATH,'//input[@id="pass"]')
    keys_sender(pass_element,password)

    #Boton de siguiente
    try:
        wait.until(ec.element_to_be_clickable((By.XPATH,"//button[@name='login']"))).click()
    except TimeoutException:
        errors_screenshoter(driver)
        print('Algo fue mal al clickear el boton se siguiente.')
        return 'bad'
    
    #entrando a perfil
    try:    
        wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@aria-label="Tu perfil"]')))
    except TimeoutException:
        errors_screenshoter(driver)
        print('Algo fue mal al cargar el perfil.')
        return 'bad'
    #salvando cookies
    with open('face_cookies.json','w') as file:
        json.dump(driver.get_cookies(),file)
    
    return driver

def login_face(email,password):
    """Funcion inicial que intenta loguearse con cookies, si falla llama al manual."""
    #starting chrome
    driver = Driver(uc=True)
    wait = WebDriverWait(driver,10)
    driver.maximize_window()
    #buscando cookies primero
    try:
        driver.get('https://facebook.com/robots.txt')
        time.sleep(1)
        with open('face_cookies.json','r') as file:
            cookies = json.load(file)
        for cookie in cookies: driver.add_cookie(cookie)
        driver.get('https://facebook.com')
        wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@aria-label="Tu perfil"]')))
    except OSError:
        driver = manual_login(email,password,driver,wait)
    except TimeoutException:
        driver = manual_login(email, password,driver,wait)
    
    return driver

if __name__ == '__main__':
    driver = login_face('nelly550ruiz@gmail.com','Leon.990423')
    driver.quit()

    

