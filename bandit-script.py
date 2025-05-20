import os
import time 


gitURLS =["https://github.com/MtheShadow/Hack-PY.git", "https://github.com/fubsi/hackpy_library.git", "https://github.com/MrSlidingTackle/Passwortmanager_HmP.git"]

if os.path.exists("bandit"):
    os.system("rmdir /s /q bandit")

os.mkdir("bandit")
os.chdir("bandit")
try:
    for url in gitURLS:
        os.system(f"git clone {url}")
        time.sleep(2)

    os.chdir("..")
    for folder in os.listdir("bandit"):
        os.system(f"python -m bandit -r bandit\\{folder} --output {folder}.txt -f txt")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    os.system("rmdir /s /q bandit")