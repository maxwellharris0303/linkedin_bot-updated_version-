from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import keyboard


firefox_profile_directory = 'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/dir1ccqy.default-release'
firefox_options = webdriver.FirefoxOptions()
firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_directory)

url = "https://www.linkedin.com/sales/search/company?viewAllFilters=true"

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()

driver.get(url)
USERNAME = "admin@safetylabs.org"
PASSWORD = "!Admin@234"
sleep(5)
keyboard.press('tab')
keyboard.release('tab')
keyboard.press('tab')
keyboard.release('tab')
sleep(1)
keyboard.write(USERNAME)
sleep(1)
keyboard.press('tab')
keyboard.release('tab')
sleep(1)
keyboard.write(PASSWORD)
keyboard.press('enter')
keyboard.release('enter')

sleep(1000)
