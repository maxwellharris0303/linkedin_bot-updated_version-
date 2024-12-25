from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import extractNumber
import extractContactInfoBot
import quickstart_company
import re

def get_company_info(companyName, interested_industry, view_company_link, employee_number_text, employee_link):
    try:
        firefox_profile_directory = 'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/dir1ccqy.default-release'
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_directory)

        driver = webdriver.Firefox(options=firefox_options)
        driver.maximize_window()
        try:
            driver.get(view_company_link)
        except:
            driver.quit()
            sleep(5)
            driver.get(view_company_link)

        # employee_url_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"_search-link_1no6tq _search-link--vertical-space_1no6tq\"]")))
        # employee_url = employee_url_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        # ####################################### Employee info scraping #################################
        # employee_info_scraping.get_employee_info(employee_url, companyName)
        # ################################################################################################
        
        more_options_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label=\"More options\"]")))
        more_options_button.click()

        linkedin_url_parent = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"_container_x5gf48 _visible_x5gf48 _container_iq15dg _raised_1aegh9\"]")))
        linkedin_url_parent.find_elements(By.TAG_NAME, 'li')[0].click()
        sleep(10)
        driver.switch_to.window(driver.window_handles[1])
        company_linkedin_url = driver.current_url
        print(f'Company LinkedIn URL: {company_linkedin_url}')

        new_url = company_linkedin_url + "about/"
        driver.get(new_url)
        # print(driver.current_url)
        try:
            company_name = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[2]/div[1]/div[2]/div/h1/span"))).text
            if company_name == "":
                company_name = companyName
        except:
            company_name = companyName
        print(f'Company Name: {company_name}')
        try:
            company_title = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "p[class=\"org-top-card-summary__tagline\"]"))).text
        except:
            company_title = "None"
        print(f'Company Title: {company_title}')

        def extract_company_info(field, text):
            match = re.search(r"{}\n(.*?)\n".format(field), text)
            if match:
                matched_string = match.group(1)
            else:
                matched_string = "None"
            return matched_string

        company_info_parent = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "dl[class=\"overflow-hidden\"]")))
        # print(company_info_parent.text)
        company_info_text = company_info_parent.text + "\n"

        company_website = extract_company_info("Website", company_info_text)
        industry = extract_company_info("Industry", company_info_text)

        employees_number_text = extract_company_info("employees", company_info_text)
        employees_number = extractNumber.extract_number(employee_number_text)

        headquarters = extract_company_info("Headquarters", company_info_text)
        founded = extract_company_info("Founded", company_info_text)
        specialties = extract_company_info("Specialties", company_info_text)

        print(f'Company Website: {company_website}')
        print(f'Industry: {industry}')
        print(f'Employees Number: {employees_number}')
        print(f'Headquarters: {headquarters}')
        print(f'Founded: {founded}')
        print(f'Specialties: {specialties}')

        try:
            phone_numbers, email_addresses = extractContactInfoBot.extract_company_contact_info(company_website)
            phone = ", ".join(phone_numbers)
            # for phone_number in phone_numbers:
            #     phone += "(" + phone_number + "), "
            # # phone = ", ".join(phone_numbers)
            email = ", ".join(email_addresses)
            print(f'Phone Nubmers: {phone}')
            print(f'Email Addresses: {email}')
        except:
            phone = ""
            email = ""
        
        quickstart_company.main()
        columnCount = quickstart_company.getColumnCount()
        RANGE_DATA = f'company!A{columnCount + 2}:N'

        quickstart_company.insert_data(RANGE_DATA,
                                    columnCount + 1, company_name, industry, company_title, company_website, employees_number, headquarters,
                                    founded, specialties, email, phone, company_linkedin_url, employee_link)

        driver.quit()
    except:
        driver.quit()
        pass