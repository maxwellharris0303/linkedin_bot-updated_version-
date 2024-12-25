from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
import time
from time import sleep

def scroll_down(driver):
    while(True):
        start_time = time.time()
        while time.time() - start_time < 20:
            div_element = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex justify-space-between full-width\"]")
            if len(div_element) == 25:
                break
            scroll_origin = div_element[len(div_element) - 1].location_once_scrolled_into_view
            ActionChains(driver)\
                .move_to_element(div_element[len(div_element) - 1])\
                .move_by_offset(0, 200)\
                .perform()

        next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label=\"Next\"]")
        if next_button.get_attribute('class') != "artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view":
            break
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        next_button.click()
        sleep(3)