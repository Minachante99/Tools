"""Un script para logearse en gmail, directamente en el correo y devuelve el driver para continuar."""

import os,time,random
from datetime import datetime as dt
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
	"""Para simular humanidad.Envia un chr cada un tiempo random."""
	for k in str(key):
		element.send_keys(k)
		time.sleep(random.randint(1,5)/10)


def gmail_login(gmail,password):
	"""Para loguearse en gmail."""
	#creando driver y wait, accediendo a la web de logeo
	driver = Driver(uc=True)
	driver.maximize_window()
	wait = WebDriverWait(driver,15)
	driver.get(r'https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&emr=1&flowEntry=ServiceLogin&flowName=GlifWebSignIn&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AS5LTARRlWmVYagolRbMTU85GPNIbetL3Z1N1YyzjLEWwqhmCzn3UnpsJNL_wt8szcjn2EaS0Nh1Gw&osid=1&passive=1209600&service=mail&dsh=S739510538%3A1717551485902084')
	
	#gmail user
	try:
		gmail_user = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@type="email"]')))
		keys_sender(gmail_user,gmail)
		wait.until(ec.element_to_be_clickable((By.XPATH,'//div[@id="identifierNext"]/div/button'))).click()
	except TimeoutException:
		print('Algo fue mal con el user.')
		errors_screenshoter(driver)
		return 'bad'

	#pass
	try:
		gmail_pass = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@type="password"]')))
		keys_sender(gmail_pass,password)
		wait.until(ec.element_to_be_clickable((By.XPATH,'//div[@id="passwordNext"]/div/button'))).click()
	except TimeoutException:
		print('Algo fue mal con la pass.')
		errors_screenshoter(driver)
		return 'bad'
	
	#esperar a que entre completo al gmail
	try:
		wait.until(ec.visibility_of_element_located((By.XPATH,'//a[contains(@aria-label,"Cuenta de Google")]')))
	except:
		print('Algo fue mal al terminar de entrar.')
		errors_screenshoter(driver)
		return 'bad'

	return driver


if __name__ == '__main__':
	driver = gmail_login('jessi550ruiz@gmail.com','jessi.9904')
	driver.quit()