from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

def login(username, password):
	driver.get('https://www.saucedemo.com/')
	driver.find_element(By.ID, 'user-name').send_keys(username)
	driver.find_element(By.ID, 'password').send_keys(password)
	driver.find_element(By.ID, 'login-button').click()
	if driver.current_url == 'https://www.saucedemo.com/inventory.html':
		return True
	else:
		return False

def add_to_cart():
	driver.get("https://www.saucedemo.com/inventory.html")
	products = driver.find_elements(By.CLASS_NAME, "inventory_item")
	products_name = []
	for product in products:
		product.find_element(By.CLASS_NAME, 'btn_inventory').click()
		products_name.append(product.find_element(By.CLASS_NAME, "inventory_item_name").text)
	driver.get("https://www.saucedemo.com/cart.html")
	added_products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
	added_products = [product.text for product in added_products]
	for product in products_name:
		if product in added_products:
			print(f"[INFO]: Added {product}")
		else:
			print(f"[INFO]: Can't add {product}")
	return len(products)

def remove_from_cart():
	driver.get("https://www.saucedemo.com/cart.html")
	products = driver.find_elements(By.CLASS_NAME, "cart_item")
	for product in products:
		product_name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
		product.find_element(By.CLASS_NAME, "cart_button").click()
		print(f"[INFO]: Removed {product_name} from cart")
	return len(products)


print ('[INFO]: Starting the browser...')
# --uncomment when running in Azure DevOps.
options = ChromeOptions()	
options.add_argument("--headless") 
driver = webdriver.Chrome(options=options)
print ('[INFO]: Browser started successfully. Navigating to the demo page to login.')

# Testing with standard user
if login("standard_user", "secret_sauce"):
	print("[INFO]: Login success with standard_user user")
	product_added = add_to_cart()
	if product_added == remove_from_cart():
		print("[PASSED]: Testing with standard_user user")
	else:
		print("[FAILED]: Testing with standard_user user")
else:
	print("[FAILED]: Login fail with staned_user user")

# Testing with locked out user
if login("locked_out_user", "secret_sauce"):
	print("[FAILED]: Login success with locked_out_user user")
	print("[FAILED]: Testing with locker_out_user user")
else:
	print("[INFO]: Login fail with locked_out_user user")
	print("[PASSED]: Testing with locker_out_user user")

# Testing with problem user
if login("problem_user", "secret_sauce"):
	print("[INFO]: Login success with problem_user user")
	product_added = add_to_cart()
	if product_added > remove_from_cart():
		print("[PASSED]: Testing with problem_user user")
	else:
		print("[FAILED]: Testing with problem_user user")
else:
	print("[FAILED]: Login fail with problem_user user")

# Testing with performance glitch user
if login("performance_glitch_user", "secret_sauce"):
	print("[INFO]: Login success with performance_glitch_user user")
	product_added = add_to_cart()
	if product_added == remove_from_cart():
		print("[PASSED]: Testing with performance_glitch_user user")
	else:
		print("[FAILED]: Testing with performance_glitch_user user")
else:
	print("[FAILED]: Login fail with performance_glitch_user user")