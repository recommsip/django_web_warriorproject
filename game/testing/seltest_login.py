from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json

options = Options()
options.add_argument("--headless")


def run_test():
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("http://127.0.0.1:8000/login/")
        username = "ron"
        password = "ynot1230"
        # Find username field
        driver.find_element(By.NAME, "username").send_keys(username)

        # Find password field
        driver.find_element(By.NAME, "password").send_keys(password)

        # Click login
        driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        ).click()
        
        WebDriverWait(driver, 2).until(
                lambda d: "/login/" not in d.current_url
            )
        
        print("Login successful")
        
        # Verify login succeeded
        assert "/login/" not in driver.current_url

        print("LOGIN TEST PASSED")
        date = datetime.now().date().strftime("%Y-%m-%d")
        
        result = {
            "test": "Login successful",
            "success": True,
            "date": date
        }
        
        print(json.dumps(result))
        return result

    finally:
        driver.quit()
        
def loginfunc(driver, username, password):
    driver.get("http://127.0.0.1:8000/login/")
    # Find username field
    driver.find_element(By.NAME, "username").send_keys(username)
    
    # Find password field
    driver.find_element(By.NAME, "password").send_keys(password)

if __name__ == "__main__":
    run_test()
        