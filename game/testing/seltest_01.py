from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

try:
    # Open your Django website
    driver.get("http://127.0.0.1:8000/")

    # Check that the page loaded
    assert driver.title != ""

    print("TEST PASSED")
    print("Page title:", driver.title)

finally:
    
    # Always close the browser
    driver.quit()