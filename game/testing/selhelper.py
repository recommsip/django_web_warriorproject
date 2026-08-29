# helpers.py
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

def login(driver, username="ron", password="ynot1230"):
    driver.get("http://127.0.0.1:8000/login/")

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert "/login/" not in driver.current_url
    print("Login successful")

