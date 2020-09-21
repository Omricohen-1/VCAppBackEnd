from selenium import webdriver
from bs4 import BeautifulSoup
import json


def login_facebook(email, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('/home/ubuntu/chrome_driver/chromedriver', chrome_options=chrome_options)
    driver.get('https://www.facebook.com/login.php')
    driver.find_element_by_id('email').send_keys(email)
    driver.find_element_by_id('pass').send_keys(password)
    driver.find_element_by_id('loginbutton').click()
    return json.dumps(['Success'])
