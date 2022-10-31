import pytest 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

@pytest.fixture()
def browser():
	print ('Starting the browser...')
	# --uncomment when running in Azure DevOps.
	options = ChromeOptions()	
	options.add_argument("--headless") 
	driver = webdriver.Chrome(options=options)
	print ('Browser started successfully. Navigating to the demo page to login.')
	return driver

def test_login_with_standard_user(browser):
	browser.get('https://www.saucedemo.com/')
	browser.find_element(By.ID, 'user-name').send_keys('standard_user')
	browser.find_element(By.ID, 'password').send_keys('secret_sauce')
	browser.find_element(By.ID, 'login-button').click()
	assert browser.current_url == 'https://www.saucedemo.com/inventory.html'

	browser.get('https://www.saucedemo.com/inventory.html')
	products = browser.find_elements(By.CLASS_NAME, 'inventory_item')
	for product in products:
		product.find_element(By.CLASS_NAME, 'btn_inventory').click()
	browser.get('https://www.saucedemo.com/cart.html')
	assert len(browser.find_elements(By.CLASS_NAME, 'cart_item')) == len(products)

	browser.get('https://www.saucedemo.com/cart.html')
	products = browser.find_elements(By.CLASS_NAME, 'cart_item')
	for product in products:
		product.find_element(By.CLASS_NAME, 'btn_secondary').click()
	browser.get('https://www.saucedemo.com/cart.html')
	assert len(browser.find_elements(By.CLASS_NAME, 'cart_item')) == 0

def test_login_with_locked_out_user(browser):
	browser.get('https://www.saucedemo.com/')
	browser.find_element(By.ID, 'user-name').send_keys('locked_out_user')
	browser.find_element(By.ID, 'password').send_keys('secret_sauce')
	browser.find_element(By.ID, 'login-button').click()
	assert browser.current_url == 'https://www.saucedemo.com/'

def test_login_with_problem_user(browser):
	browser.get('https://www.saucedemo.com/')
	browser.find_element(By.ID, 'user-name').send_keys('problem_user')
	browser.find_element(By.ID, 'password').send_keys('secret_sauce')
	browser.find_element(By.ID, 'login-button').click()
	assert browser.current_url == 'https://www.saucedemo.com/inventory.html'

	browser.get('https://www.saucedemo.com/inventory.html')
	products = browser.find_elements(By.CLASS_NAME, 'inventory_item')
	for product in products:
		product.find_element(By.CLASS_NAME, 'btn_inventory').click()
	browser.get('https://www.saucedemo.com/cart.html')
	assert len(browser.find_elements(By.CLASS_NAME, 'cart_item')) <= len(products)

	browser.get('https://www.saucedemo.com/cart.html')
	products = browser.find_elements(By.CLASS_NAME, 'cart_item')
	for product in products:
		product.find_element(By.CLASS_NAME, 'btn_secondary').click()
	browser.get('https://www.saucedemo.com/cart.html')
	assert len(browser.find_elements(By.CLASS_NAME, 'cart_item')) == 0

def test_login_with_performance_glitch_user(browser):
	browser.get('https://www.saucedemo.com/')
	browser.find_element(By.ID, 'user-name').send_keys('performance_glitch_user')
	browser.find_element(By.ID, 'password').send_keys('secret_sauce')
	browser.find_element(By.ID, 'login-button').click()
	assert browser.current_url == 'https://www.saucedemo.com/inventory.html'

	browser.get('https://www.saucedemo.com/inventory.html')
	products = browser.find_elements(By.CLASS_NAME, 'inventory_item')
	for product in products:
		product.find_element(By.CLASS_NAME, 'btn_inventory').click()
	browser.get('https://www.saucedemo.com/cart.html')
	assert len(browser.find_elements(By.CLASS_NAME, 'cart_item')) <= len(products)

	browser.get('https://www.saucedemo.com/cart.html')
	products = browser.find_elements(By.CLASS_NAME, 'cart_item')
	for product in products:
		product.find_element(By.CLASS_NAME, 'btn_secondary').click()
	browser.get('https://www.saucedemo.com/cart.html')
	assert len(browser.find_elements(By.CLASS_NAME, 'cart_item')) == 0