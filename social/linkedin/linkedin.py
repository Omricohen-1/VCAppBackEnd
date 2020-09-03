from selenium import webdriver
from bs4 import BeautifulSoup
import json

driver = webdriver.Chrome(r'.\chromedriver')

driver.get('https://www.linkedin.com/')

test_data = json.loads(open('mocks\FB_TEST.json', 'r').read())


usename_place = driver.find_element_by_xpath('//*[@id="session_key"]')
usename_place.click()
usename_place.send_keys(test_data['email'])


usename_place = driver.find_element_by_xpath('//*[@id="session_password"]')
usename_place.click()
usename_place.send_keys(test_data['password'])

driver.find_element_by_xpath(
    '/html/body/main/section[1]/div[2]/form/button').click()

try:
    confirmition = driver.find_element_by_xpath(
        '//*[@id="ember512"]/button[1]')
    confirmition.click()

except:
    None

search_bar = driver.find_element_by_xpath(
    '//*[@id="ember39"]/div[2]/button').click()
search_bar.send_keys('Aviv Sharon')
search_bar.click()
