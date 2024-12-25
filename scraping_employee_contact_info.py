from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep



def get_contact_info(url):
    if url == "":
        return "", ""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")
    chrome_options.add_argument('--profile-directory=Default')  # Replace with the actual Chrome profile directory

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get(url)

    apollo_extension_icon = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-cy=\"apollo-opener-icon-new\"]")))
    apollo_extension_icon.click()

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"x_WRo0w\"]")))
    try:
        contact_info_elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x_WRo0w\"]")
        # print(len(contact_info_elements))
        contact_info_elements[0].click()
        sleep(3)
        mobile_element_for = driver.find_elements(By.TAG_NAME, "div[class=\"x_pRbdE\"]")
        for element in mobile_element_for:
            if element.text == "Mobile":
                element.click()
                break
    except:
        pass
    email_addresses = []
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"x_GxQlI\"]")))
        email_address_elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x_GxQlI\"]")
        for email in email_address_elements:
            email_addresses.append(email.text)
    except:
        email_addresses = ""
    print(email_addresses)
    phone_numbers = []
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"x_XitPs\"]")))
        phone_numbers_elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x_XitPs\"]")
        for phone_number in phone_numbers_elements:
            number = phone_number.text
            if not "*" in number:
                phone_numbers.append(number[1:])
    except:
        phone_numbers = ""
    print(phone_numbers)
    driver.quit()
    return email_addresses, phone_numbers

# print(get_contact_info("https://www.linkedin.com/in/ksass/"))

# email_addresses, phone_numbers = get_contact_info("https://www.linkedin.com/in/ksass/")

# print(email_addresses)
# print(phone_numbers)