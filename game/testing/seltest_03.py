from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
import json
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)


def run_test():
    try:
        driver.get("http://127.0.0.1:8000/")
        tavern = driver.find_element(By.NAME, "characterSelect")
        tavern.click()
        # character_select = driver.find_element(By.LINK_TEXT, "Continue")
        # character_select.click()
        result = {
                    "test": "Create Warrior successful",
                    "success": False
                }
        print(json.dumps(result))
        
        assert "/tavern/" in driver.current_url

        print("TEST PASSED")
        return result

    finally:
        driver.quit()