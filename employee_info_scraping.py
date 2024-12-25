from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import time
import quickstart_employee
import quickstart_type_of_employee
import re
import scraping_employee_contact_info


def get_employee_info(url, companyName):
    quickstart_type_of_employee.main()
    type_of_employees = quickstart_type_of_employee.getInterestTypeOFEmployee()
    print(type_of_employees)

    firefox_profile_directory = 'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/dir1ccqy.default-release'
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_directory)

    driver = webdriver.Firefox(options=firefox_options)
    driver.maximize_window()
    try:
        driver.get(url)
    except:
        driver.quit()
        sleep(5)
        driver.get(url)

    try:
        view_all_filter_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label=\"Expand panel to see all filters\"]")))
        view_all_filter_button.click()
    except:
        arrow_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg vertical-accordion--trigger\"]")))
        arrow_button.click()
        sleep(2)
        view_all_filter_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label=\"Expand panel to see all filters\"]")))
        view_all_filter_button.click()
    sleep(2)
    filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class=\"artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary search-filter__focus-target--button mlA button--fill-click-area artdeco-button--0 flex-shrink-zero\"]")
    filter_buttons[7].click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class=\"artdeco-typeahead__result ember-view  pv1 ph4 relative\"]")))
    seniority_level_elements = driver.find_elements(By.CSS_SELECTOR, "li[class=\"artdeco-typeahead__result ember-view  pv1 ph4 relative\"]")
    for level_element in seniority_level_elements:
        level_text = level_element.find_element(By.CSS_SELECTOR, "span[class=\"mh1 t-14 color-inherit nowrap-ellipsis\"]").text
        level_text = re.sub(r'\d+', '', level_text).strip()
        print(level_text)
        # if "CXO" in level_text or "Vice President" in level_text:
        #     level_element.click()
        for type_of_employee in type_of_employees:
            if type_of_employee == level_text:
                level_element.click()
    # sleep(3)
    # save_search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"ember-view _button_ps32ck _small_ps32ck _secondary_ps32ck _emphasized_ps32ck _left_ps32ck _container_iq15dg ml2 \"]")))
    # save_search_button.click()

    # save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"ember-view _button_ps32ck _small_ps32ck _primary_ps32ck _emphasized_ps32ck _left_ps32ck _container_iq15dg ml2\"]")))
    # save_button.click()
    while(True):
        sleep(3)
        start_time = time.time()
        try:
            while time.time() - start_time < 10:
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
        ################################################## scraping employee data #################################################
        # try:
        elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-space-between full-width\"]")
        if len(elements) == 0:
            elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-space-between full-width \"]")
        # except:
        # elements = []
        for element in elements:
            sleep(3)
            try:
                employee_name = element.find_element(By.CSS_SELECTOR, "span[data-anonymize=\"person-name\"]").text
                employee_title = element.find_element(By.CSS_SELECTOR, "span[data-anonymize=\"title\"]").text
                # print(f'Full Name: {employee_name}')

                names = employee_name.split()
                # Extract the first name
                first_name = names[0]
                # Extract the last name
                last_name = names[-1]
                print(f'First Name: {first_name}')
                print(f'Last Name: {last_name}')

                print(f'Company Name: {companyName}')

                print(f'Title: {employee_title}')
                name_element = element.find_element(By.CSS_SELECTOR, "div[class=\"artdeco-entity-lockup__title ember-view\"]")
                name_element.click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-anonymize=\"headline\"]")))
                employee_headline = driver.find_element(By.CSS_SELECTOR, "span[data-anonymize=\"headline\"]").text
                print(f'Headline: {employee_headline}')
                try:
                    driver.find_elements(By.CSS_SELECTOR, "button[aria-label=\"Open actions overflow menu\"]")[1].click()
                    sleep(2)
                    all_a_tag = driver.find_elements(By.TAG_NAME, 'a')
                    linkedin_url = "None"
                    for a_tag in all_a_tag:
                        if "View LinkedIn profile" in a_tag.text:
                            linkedin_url = a_tag.get_attribute('href')
                except:
                    linkedin_url = ""
                print(f'LinkedIn URL: {linkedin_url}')


                email_address, phone_numbers = scraping_employee_contact_info.get_contact_info(linkedin_url)
                emails = "\n".join(email_address)
                phones = "\n".join(phone_numbers)
                quickstart_employee.main()
                columnCount = quickstart_employee.getColumnCount()
                RANGE_DATA = f'employee!A{columnCount + 2}:I'

                quickstart_employee.insert_data(RANGE_DATA,
                                            columnCount + 1, first_name, last_name, companyName, employee_title, employee_headline, linkedin_url, emails, phones)
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
        sleep(3)

    driver.quit()

# url = "https://www.linkedin.com/sales/search/people?coach=false&query=(recentSearchParam%3A(id%3A3268263572%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A18338882%2Ctext%3AAFWERX%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0))))))&sessionId=IJb5zuewQfOqDRrWUNtfdw%3D%3D"
# get_employee_info(url, "Eve Air Mobility")