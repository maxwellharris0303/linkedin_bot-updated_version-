from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import getContactUrl
from bs4 import BeautifulSoup
import re
import phonenumbers
import clearEmail

def extract_company_contact_info(url):
    def check_phone_number(phone_number):
        try:
            parsed_number = phonenumbers.parse(phone_number)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
        
    def format_phone_number(phone_number):
        # Remove any non-digit characters from the phone number
        array = []
        for num in phone_number:
            if not "," in num:
                digits = ''.join(filter(str.isdigit, num))
                # digits = digits[-10:]

                # Check if the phone number has a valid length
                if len(digits) >= 10:
                    # Format the phone number in the desired format
                    formatted_number = "{} {}-{}-{}".format(digits[:-10], digits[-10:-7], digits[-7:-4], digits[-4:])
                    checking_number = "+{} {}-{}-{}".format(digits[:-10], digits[-10:-7], digits[-7:-4], digits[-4:])
                    if check_phone_number(checking_number) == True:
                        array.append(formatted_number)
                if len(digits) == 10:
                    # Format the phone number in the desired format
                    formatted_number = "{}-{}-{}".format(digits[-10:-7], digits[-7:-4], digits[-4:])
                    checking_number = "+1 {}-{}-{}".format(digits[-10:-7], digits[-7:-4], digits[-4:])
                    if check_phone_number(checking_number) == True:
                        array.append(formatted_number)

        array = remove_duplicates(array)
        return array

    def extract_contact_info(html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find all phone numbers using regular expression
        phone_numbers = re.findall(r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\0-9]*(?=[^0-9])', soup.get_text())
        # print(phone_numbers)
        # Find all email addresses using regular expression
        email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())

        tel_links = soup.find_all(href=re.compile(r'tel:'))
        href_phone_numbers = [re.sub(r'tel:', '', link.get('href')) for link in tel_links]

        phone_numbers.extend(href_phone_numbers)

        email_links = soup.find_all(href=re.compile(r'mailto:'))
        href_email = [re.sub(r'mailto:', '', link.get('href')) for link in email_links]

        email_addresses.extend(href_email)
        
        phone_numbers = format_phone_number(phone_numbers)
        email_addresses = remove_duplicates(email_addresses)
        return phone_numbers, email_addresses

    def remove_duplicates(arr):
        unique_arr = []
        for item in arr:
            if item not in unique_arr:
                unique_arr.append(item)
        return unique_arr

    def remove_email_duplicates(array):
        unique_strings = set()

        # Iterate over the array
        for email in array:
            # Convert the email to lowercase
            lowercase_email = email.lower()

            # Check if the lowercase email is already in the set
            if lowercase_email not in unique_strings:
                # Add the lowercase email to the set
                unique_strings.add(lowercase_email)

        # Convert the set back to a list
        unique_array = list(unique_strings)

        return unique_array

    driver = webdriver.Chrome()
    driver.maximize_window()

    phoneNumbers = []
    emailAddresses = []

    available_urls = getContactUrl.available_urls(url, driver)
    for u in available_urls:
        driver.get(u)
        sleep(2)
        html_content = driver.page_source
        phone_numbers, email_addresses = extract_contact_info(html_content)

        phoneNumbers.extend(phone_numbers)
        emailAddresses.extend(email_addresses)
    phoneNumbers = remove_duplicates(phoneNumbers)
    emailAddresses = remove_duplicates(emailAddresses)
    driver.quit()

    emailAddresses = clearEmail.clear_emails(emailAddresses)
    emailAddresses = remove_email_duplicates(emailAddresses)

    if len(phoneNumbers) == 0:
        print("No phone number")
    if len(phoneNumbers) != 0:
        print("Phone Numbers:", phoneNumbers)
        # data_save(f"Phone Numbers: {phoneNumbers}")
    if len(emailAddresses) == 0:
        print("No email address")
    if len(emailAddresses) != 0:
        print("Email Addresses:", emailAddresses)
        # data_save(f"Email Addresses: {emailAddresses}")

    return phoneNumbers, emailAddresses

# url = "https://chirophysio16th.com/"
# print(extract_company_contact_info(url))


# def check_phone_number(phone_number):
#         try:
#             parsed_number = phonenumbers.parse(phone_number)
#             return phonenumbers.is_valid_number(parsed_number)
#         except phonenumbers.phonenumberutil.NumberParseException:
#             return False
# print(check_phone_number("+49345674890"))

