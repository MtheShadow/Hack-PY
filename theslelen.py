from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

s = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=s)

website = "http://127.0.0.1:5000/login"

driver.get(website)

titles = ""

passwords = ["adjaödlja", "lakdhalkjhda", "akshdakjd", "pass"]

i = 0

for password in passwords:
    print (f"Trying password: {password}")

    res = driver.find_elements(By.CLASS_NAME, "form-control")
    assert len(res) == 2

    res[0].clear()
    res[0].send_keys("Derk")
    res[1].clear()
    res[1].send_keys(password)

    but = driver.find_elements(By.CLASS_NAME, "btn")

    assert len(but) == 1
    but[0].click()
    time.sleep(0.05)

    print(driver.title)


    if driver.title != "This is my Login Page":
        print(f"The Correct Password is '{password}'")



driver.quit()