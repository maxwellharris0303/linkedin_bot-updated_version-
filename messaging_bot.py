from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from time import sleep
import quickstart_employee

quickstart_employee.main()

unique_list, employee_profile_list, first_name_list, last_name_list, company_name_list = quickstart_employee.getEmployeeProfileList()


firefox_profile_directory = 'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/dir1ccqy.default-release'
firefox_options = webdriver.FirefoxOptions()
firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_directory)

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()

count = len(unique_list)
index = 0
for _ in range(count):
    try:
        driver.get(employee_profile_list[index])
        sleep(5)
        button = driver.find_element(By.CSS_SELECTOR, "button[class=\"artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action\"]")
        print(button.text)
        # Get the initial window handles
        initial_handles = driver.window_handles
        if button.text != "Follow":
            button.click()
        sleep(5)
        
        updated_handles = driver.window_handles
        MESSAGE_HEADER = f"Hello {first_name_list[index]} {last_name_list[index]}"
        MESSAGE_CONTENT = f"I assist liquor retailers implement AI. \n\nOnce we connect, I will share a few ways how {company_name_list[index]} can benefit using AI Technogym.\n\nSanjay,\nCo-founder AIWizards.ai, AISommelier.org, AIHumans.ai, AIKioks.ai"
        MESSAGE_TEMPLATE = f"{MESSAGE_HEADER} \n\n {MESSAGE_CONTENT}"
        if button.text == "Message":
            if len(updated_handles) > len(initial_handles):
                driver.switch_to.window(driver.window_handles[1])
                
                inbox_element = driver.find_element(By.CSS_SELECTOR, "section[class=\"_overlay-container_1m6rrr _container_iq15dg _attachmentBottom_iq15dg _raised_1aegh9\"]")
                # print(inbox_element.text)
                input_subject = inbox_element.find_element(By.CSS_SELECTOR, "input[placeholder=\"Subject (required)\"]")
                input_subject.send_keys(MESSAGE_HEADER)
                text_area_element = inbox_element.find_element(By.CSS_SELECTOR, "textarea[placeholder=\"Type your message here…\"]")
                text_area_element.send_keys(MESSAGE_CONTENT)
                send_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"ember-view _button_ps32ck _small_ps32ck _primary_ps32ck _left_ps32ck _container_iq15dg ml4\"]")
                send_button.click()

                sleep(3)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else :
                message_areas_elements = driver.find_elements(By.CSS_SELECTOR, "div[aria-label=\"Write a message…\"]")
                message_area = message_areas_elements[len(message_areas_elements) - 1]
                message_area.send_keys(MESSAGE_TEMPLATE)
                submit_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
                submit_button.click()
                sleep(3)
            
        if button.text == "Connect":
            add_note_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label=\"Add a note\"]")))
            add_note_button.click()
            sleep(3)
            message_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[id=\"custom-message\"]")))
            message_element.send_keys(MESSAGE_TEMPLATE)
            send_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label=\"Send now\"]")
            send_button.click()
            sleep(5)
    except:
        pass
    index += 1