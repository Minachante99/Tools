"""Script con la idea de crear cuentas en gmail. Se inicializa con un nombre y correo.
A futuro se anadira la opcion de proxies para escalar el programa."""

import time,random,os
from string import ascii_lowercase,ascii_uppercase
from datetime import datetime as dt

while 1:
	try:
		from seleniumbase import Driver
		from selenium.webdriver.support.ui import WebDriverWait
		from selenium.webdriver.support import expected_conditions as ec
		from selenium.webdriver.common.by import By
		from selenium.common.exceptions import TimeoutException 
		from selenium.webdriver.common.keys import Keys
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

def password_spawner():
	"""Funcion que creas las passwords.Una mayuscula,3 minusculas,un punto y 4 numeros."""
	uppers = ascii_uppercase
	lowers = ascii_lowercase
	return random.choice(uppers) + ''.join([random.choice(lowers) for x in range(3)]) + '.' + ''.join([str(random.randint(0,9)) for x in range(4)])

def keys_sender(element,string):
	"""Para simular humanidad al introducir datos."""
	for letter in str(string):
		element.send_keys(letter)
		time.sleep(random.randint(1,4)/10)

def gmail_account_creator(first_name,last_name,driver,wait):
	"""Crea cuentas en gmail.Anadir proxies luego."""
	#setenado variables y testeando la pagina
	try:
		driver.get(r'https://accounts.google.com/signup')#direccion
	except TimeoutException:
		#si se demora mucho debe ser algun problema de internet
		print('Algo fue mal al cargar el signup, revisa tu internet.')
		errors_screenshoter(driver)
		driver.quit()
		return 'bad'
	#seteando lenguaje e introduciendo nombres
	try:
		language_e = wait.until(ec.visibility_of_element_located((By.XPATH,'//span[@id="i3"]')))
		if language_e.text != 'English (United States)':
			driver.find_element(By.XPATH,'//span[@role="listbox"]/..').click()
			time.sleep(1)
			wait.until(ec.element_to_be_clickable((By.XPATH,'//li[@data-value="en-US"]'))).click()
	except TimeoutException:
		print('Algo fue mal al cargar los nombres')
		errors_screenshoter(driver)
		driver.quit()
		return 'bad'
	#nombres
	name_e = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@id="firstName"]')))
	keys_sender(name_e,first_name)
	name_e.send_keys(Keys.TAB)
	#apellido
	last_name_e = driver.find_element(By.XPATH,'//input[@id="lastName"]')
	keys_sender(last_name_e,last_name)
	#boton de next
	wait.until(ec.element_to_be_clickable((By.XPATH,'//div/button/span[contains(text(),"Next")]'))).click()
	
	#cumple
	#month
	try:
		day_e = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@id="day"]')))
	except TimeoutException:
		print('Algo fue mal al cargar el cumple')
		errors_screenshoter(driver)
		driver.quit()
		return 'bad'
	driver.find_element(By.XPATH,'//div[@id="month"]//div[@role="combobox"]').send_keys(Keys.SPACE)
	time.sleep(1)
	wait.until(ec.element_to_be_clickable((By.XPATH,f'//ul[@aria-label="Month"]/li[@data-value={random.randint(1,12)}]'))).click()
	#day
	keys_sender(day_e,random.randint(1,28))
	#year 
	year_e = driver.find_element(By.XPATH,'//input[@id="year"]')
	keys_sender(year_e,random.randint(1975,2005))
	#genre
	driver.find_element(By.XPATH,'//div[@id="gender"]//div[@role="combobox"]').send_keys(Keys.SPACE)
	time.sleep(1)
	wait.until(ec.element_to_be_clickable((By.XPATH,f'//ul[@aria-label="Gender"]/li[@data-value={random.randint(1,3)}]'))).click()
	
	#boton next
	wait.until(ec.element_to_be_clickable((By.XPATH,'//span[text()="Next"]/..'))).click()
	
	#seleccion de gmail
	#esto hay que mejorarlo si a futuro da errores de no sugerir correo, hacerlo uno mismo
	try:
		wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@type="radio"]/..')))
	except TimeoutException:
		print('Algo fue mal al cargar la seleccion del gmail')
		errors_screenshoter(driver)
		driver.quit()
		return 'bad'
	radio_e = driver.find_elements(By.XPATH,'//input[@type="radio"]')[0]
	time.sleep(0.5)
	radio_e.send_keys(Keys.SPACE)
	gmail= radio_e.get_attribute('value') + '@gmail.com'
	print(gmail)
	#next button
	wait.until(ec.element_to_be_clickable((By.XPATH,'//button/span[text()="Next"]'))).click()
	
	#password
	password = password_spawner()
	try:
		pass_e = wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@name="Passwd"]')))
	except TimeoutException:		
		print('Algo fue mal al cargar la seleccion de pass')
		errors_screenshoter(driver)
		driver.quit()
		return 'bad'
	keys_sender(pass_e,password)
	pass_e.send_keys(Keys.TAB)
	#confirmation pass
	re_pass_e = driver.find_element(By.XPATH,'//input[@name="PasswdAgain"]')
	keys_sender(re_pass_e,password)
	#botton
	wait.until(ec.element_to_be_clickable((By.XPATH,'//span[text()="Next"]/..'))).click()
	# partes finales de aceptar terminos y pinga
	time.sleep(2)
	breakpoint()
	#driver.quit()
	#return gmail,password
	

if __name__ == '__main__':
	#testing
	driver = Driver(uc=True)
	wait = WebDriverWait(driver,15)
	driver.maximize_window()
	gmail_account_creator('Federico de la Concepcion','Garcia Jimenez',driver,wait)