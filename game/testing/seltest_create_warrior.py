from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from getpass import getpass
import json

driver = webdriver.Chrome()

def run_test():
    date = datetime.now().date().strftime("%Y-%m-%d")
    username = input("Username: ")
    password = getpass("Password: ")
    
    try:
        # -------------------------
        # LOGIN
        # -------------------------
        driver.get("http://127.0.0.1:8000/login/")
        
        driver.find_element(
            By.NAME, "username"
        ).send_keys(username)

        driver.find_element(
            By.NAME, "password"
        ).send_keys(password)

        driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        ).click()
        
        WebDriverWait(driver, 10).until(
                    lambda d: "/login/" not in d.current_url
                )
            
        assert "/login/" not in driver.current_url

        print("Login successful")


        # -------------------------
        # CREATE WARRIOR
        # -------------------------

        driver.get("http://127.0.0.1:8000/")

        driver.find_element(
            By.NAME, "name"
        ).send_keys("Test Warrior")

        driver.find_element(By.ID, "begin_journey")
        
        element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'The Tavern')]"))
            )
        if(element):
            print("Found Tavern Button")
            print("Found Begin Journey Button")
        
        driver.find_element(By.ID, "begin_journey").click()
        print("Found Begin Journey Button Clicked.")
        
        WebDriverWait(driver, 10).until(
                    lambda d: "/character/" in d.current_url
                )
        
        print("Made it to the character sheeet url.")
        print("Warrior creation submitted")
        
        # # Click login
        # driver.find_element(
        #      By.CSS_SELECTOR,
        #      "button[type='submit']"
        #  ).click()

        # Wait up to 10 seconds for the element containing the exact text to appear on screen
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Test Warrior')]"))
        )

        # -------------------------
        # VERIFY
        # -------------------------
        assert "Test Warrior" in element.text
          
        if(not "Test Warrior" in element.text):
            result = {
                        "test": "Create Warrior Failed.",
                        "success": False,
                        "date": date
                    }
            print(json.dumps(result))
            return result
        print("WARRIOR TEST PASSED")
        
        driver.find_element(By.XPATH, "//*[contains(text(), 'Continue Journey')]").click()
        print("Clicked Continue Journey.")
        
       
        
        result = {
                "test": "Create Warrior successful",
                "success": True,
                "date": date
            }
            
        print(json.dumps(result))
        return result
            
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()