# File: modules/tinder.py
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Chrome options to connect to the remote debugging port
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
service = Service()

try:
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"Error starting Chrome with remote debugging: {e}")
    exit(1)

actions = ActionChains(driver)

def like():
    try:
        element = driver.find_element(By.XPATH, '//*[@style="transform: scale(1); background-color: rgba(16, 224, 132, 0);"]')
        actions.move_to_element(element).click().perform()
        time.sleep(1)
    except Exception as e:
        print(f"Error in like function: {e}")

def unlike():
    try:
        element = driver.find_element(By.XPATH, '//*[@style="transform: scale(1); background-color: rgba(253, 84, 108, 0);"]')
        actions.move_to_element(element).click().perform()
        time.sleep(1)
    except Exception as e:
        print(f"Error in unlike function: {e}")

def get_profile_info():
    try:
        username = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
        age = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="age"]').text
        return username, age
    except Exception as e:
        print(f"Error getting profile info: {e}")
        return None, None

def download_first_image(username, age):
    folder_path = 'Picax'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    base_file_name = f'{username}-{age}.png'
    file_name = base_file_name
    
    count = 1
    while os.path.exists(os.path.join(folder_path, file_name)):
        file_name = f'{username}-{age}-{count}.png'
        count += 1
    
    slide = driver.find_element(By.CSS_SELECTOR, '.keen-slider__slide .StretchedBox')
    
    try:
        style_attr = slide.get_attribute('style')
        url_match = re.search(r'url\("(.+?)"\)', style_attr)
        if url_match:
            img_url = url_match.group(1)
            img_data = requests.get(img_url).content
            img_path = os.path.join(folder_path, file_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f'Downloaded {img_path}')
    except Exception as e:
        print(f'Failed to download image: {e}')

def scape():
    username, age = get_profile_info()
    if username and age:
        download_first_image(username, age)
    else:
        print("Profile information not found.")
        
