from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from time import sleep
import quickstart_industries

firefox_profile_directory = 'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/dir1ccqy.default-release'
firefox_options = webdriver.FirefoxOptions()
firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_directory)

url = "https://www.linkedin.com/sales/search/company?viewAllFilters=true"

KEYWORD = "Building Materials"

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()
driver.get(url)
sleep(3)

filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class=\"artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary search-filter__focus-target--button mlA button--fill-click-area artdeco-button--0 flex-shrink-zero\"]")
filter_buttons[7].click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"mh1 t-14 color-inherit nowrap-ellipsis\"]")))
industry_elements = driver.find_elements(By.CSS_SELECTOR, "span[class=\"mh1 t-14 color-inherit nowrap-ellipsis\"]")
print(len(industry_elements))
industry_array = []
for industry in industry_elements:
    industry_array.append(industry.text)

    quickstart_industries.main()
    columnCount = quickstart_industries.getColumnCount()
    RANGE_DATA = f'industries!A{columnCount + 2}:A'

    quickstart_industries.insert_data(RANGE_DATA, industry.text)
print(industry_array)

