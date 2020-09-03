from selenium import webdriver
from bs4 import BeautifulSoup
import json

driver = webdriver.Chrome(r'.\chromedriver')

driver.get('https://www.facebook.com/')

# you should create a mocks folder and a FB_TEST.json file with 'email' and 'password' keys
test_data = json.loads(open('mocks\FB_TEST.json', 'r').read())


usename_place = driver.find_element_by_xpath('//*[@id="email"]')
usename_place.click()
usename_place.send_keys(test_data['email'])


usename_place = driver.find_element_by_xpath('//*[@id="pass"]')
usename_place.click()
usename_place.send_keys(test_data['password'])

driver.find_element_by_xpath(
    '/html/body/main/section[1]/div[2]/form/button').click()

confirmition = driver.find_element_by_xpath('//*[@id="u_0_b"]')
confirmition.click()
