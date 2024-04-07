from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

chromedriver = '/usr/local/bin/chromedriver' # ruta donde esta el chromedriver

service = Service(chromedriver)
prefs = {"credentials_enable_service": False,
        "profile.password_manager_enabled": False}

#Set Options
def get_selenium_driver():
    options = Options()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches',['enable-automation'])
    options.add_experimental_option('prefs', prefs) 
    options.add_argument('--disable-notifications') 
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=service,options=options)
    return driver


def get_service_account():
    path = os.getcwd()
    service_account = path + '/key/key.json'
    return service_account

