# helpers.py
from selenium.webdriver.common.by import By

def login(driver, username="ron", password="ynot1230"):
    driver.get("http://127.0.0.1:8000/login/")

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert "/login/" not in driver.current_url
    print("Login successful")