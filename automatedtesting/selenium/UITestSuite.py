from ast import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import argparse

URL= 'https://www.saucedemo.com/'

# login with standard_user
def login (user, password):
    driver.find_element(By.ID, 'user-name').send_keys(user)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()
    try:
        if driver.find_element(By.ID, 'inventory_container').is_displayed():
            return True
    except:
        return False

# adds all products to a cart
def add_all_products_to_cart():
    products = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    for product in products:
        product.find_element(By.CLASS_NAME, 'btn_inventory').click()
    if len(products) == int(driver.find_element(By.CLASS_NAME, 'shopping_cart_badge').text):
        return True
    else:
        return False

# removes all products from a cart
def remove_all_products_from_cart():
    products = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    for product in products:
        product.find_element(By.CLASS_NAME, 'btn_secondary').click()
    if driver.find_element(By.CLASS_NAME, 'shopping_cart_link').text:
        return False
    else:
        return True

if __name__ == "__main__":
    print ('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    # options = ChromeOptions()
    # options.add_argument("--headless") 
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get(URL)
    
    # Get user and password from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help='Username to login with', required=True)
    parser.add_argument('--password', help='Password to login with', required=True)
    user_name, password = parser.parse_args().user, parser.parse_args().password
    
    # Test UI login
    print ('Testing login with user: ' + user_name + ' and password: ' + password)
    if login(user_name, password):
        print ('Login successful')
        if add_all_products_to_cart():
            print ('All products added to cart')
            if remove_all_products_from_cart():
                print ('All products removed from cart')
                print ('Test passed')
            else:
                print ('Test failed')
    
