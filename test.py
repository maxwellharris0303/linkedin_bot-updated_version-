from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument('--profile-directory=Default')  # Replace with the actual Chrome profile directory

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://mail.google.com/mail/u/0/#inbox")

