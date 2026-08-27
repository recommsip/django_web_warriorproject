from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get("http://127.0.0.1:8000/")

print(driver.title)

driver.quit()