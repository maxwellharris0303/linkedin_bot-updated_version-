from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from time import sleep
import time
import quickstart_industries
import company_info_scraping
# import employee_info_scraping
import quickstart_company_size
import quickstart_location

quickstart_industries.main()
interested_industries = quickstart_industries.getInterestIndustries()
print(interested_industries)

quickstart_company_size.main()
company_sizes = quickstart_company_size.getCompanySizes()
print(company_sizes)

quickstart_location.main()
locations = quickstart_location.getLocations()
print(locations)

firefox_profile_directory = 'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/dir1ccqy.default-release'
firefox_options = webdriver.FirefoxOptions()
firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_directory)

url = "https://www.linkedin.com/sales/search/company?viewAllFilters=true"

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()
try:
    driver.get(url)
except:
    driver.quit()
    sleep(5)
    driver = webdriver.Firefox(options=firefox_options)
    driver.maximize_window()
    driver.get(url)
sleep(3)
for interested_industry in interested_industries:
    for company_size in company_sizes:
        # loop_count = 0
        for location in locations:
            try:
                filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class=\"artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary search-filter__focus-target--button mlA button--fill-click-area artdeco-button--0 flex-shrink-zero\"]")
                filter_buttons[7].click()

                input_add_industry = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder=\"Add industries\"]")))
                input_add_industry.send_keys(interested_industry)
                sleep(3)
                industry_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class=\"artdeco-typeahead__result ember-view  pv1 ph4 relative\"]")))
                industry_element.click()
                sleep(3)

                filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class=\"artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary search-filter__focus-target--button mlA button--fill-click-area artdeco-button--0 flex-shrink-zero\"]")
                filter_buttons[6].click()

                input_add_location = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder=\"Add locations\"]")))
                input_add_location.send_keys(location)
                sleep(3)
                try:
                    location_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class=\"artdeco-typeahead__result ember-view  pv1 ph4 relative\"]")))
                    location_element.click()
                except:
                    break
                sleep(3)

                filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class=\"artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary search-filter__focus-target--button mlA button--fill-click-area artdeco-button--0 flex-shrink-zero\"]")
                filter_buttons[1].click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class=\"artdeco-typeahead__result ember-view  pv1 ph4 relative\"]")))
                headcount_elements = driver.find_elements(By.CSS_SELECTOR, "li[class=\"artdeco-typeahead__result ember-view  pv1 ph4 relative\"]")
                # headcount_elements = headcount_elements[2:-2]
                # reversed_array = headcount_elements[::-1]
                for headcount_element in headcount_elements:
                    if company_size in headcount_element.text:
                        headcount_element.click()
                        break
                # headcount_elements[loop_count].click()
            except:
                pass
            sleep(2)

            while(True):
                start_time = time.time()
                try:
                    while time.time() - start_time < 20:
                        div_element = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-space-between full-width\"]")
                        if len(div_element) == 0:
                            div_element = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-space-between full-width \"]")

                        if len(div_element) == 25:
                            break
                        scroll_origin = div_element[len(div_element) - 1].location_once_scrolled_into_view
                        ActionChains(driver)\
                            .move_to_element(div_element[len(div_element) - 1])\
                            .move_by_offset(0, 200)\
                            .perform()
                except:
                    pass
                sleep(3)
                ################################################## scraping company name #################################################
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-space-between full-width\"]")
                    if len(elements) == 0:
                        elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-space-between full-width \"]")
                except:
                    pass
                for element in elements:
                    try:
                        sleep(3)
                        company_name_text = element.find_element(By.CSS_SELECTOR, "a[data-anonymize=\"company-name\"]").text
                        company_industry_text = element.find_element(By.CSS_SELECTOR, "span[data-anonymize=\"industry\"]").text
                        employee_link = element.find_element(By.CSS_SELECTOR, "a[data-anonymize=\"company-size\"]").get_attribute('href')
                        employee_number_text = element.find_element(By.CSS_SELECTOR, "a[data-anonymize=\"company-size\"]").text
                        more_option_button = element.find_element(By.CSS_SELECTOR, "button[aria-label=\"Open dropdown menu for more account actions\"]")
                        more_option_button.click()
                        # sleep(2)
                        list_element = WebDriverWait(element, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"artdeco-dropdown__content-inner\"]")))

                        view_company_link = list_element.find_element(By.TAG_NAME, "a").get_attribute('href')
                        print(employee_link, view_company_link)
                        company_info_scraping.get_company_info(company_name_text, company_industry_text, view_company_link, employee_number_text, employee_link)
                        # employee_info_scraping.get_employee_info(employee_link, company_name_text)
                    except:
                        pass
                ##########################################################################################################################
                sleep(3)
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label=\"Next\"]")
                    if next_button.get_attribute('class') != "artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view":
                        break
                    driver.execute_script("arguments[0].scrollIntoView();", next_button)
                    next_button.click()
                except:
                    break
                sleep(5)
            try:
                clear_filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label=\"Clear all filter values\"]")))
                clear_filter_button.click()
            except:
                pass
            sleep(2)
            # loop_count += 1
        
print("Done!")