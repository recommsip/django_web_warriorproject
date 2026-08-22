from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore

driver = webdriver.Chrome()

driver.get("http://127.0.0.1:8000/")

print(driver.title)

driver.quit()