from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs
import json





class LinkedinInstance:
    def __init__(self, email, password):
        self.main_url = 'https://www.linkedin.com'
        self.driver = webdriver.Chrome(r'.\chromedriver')
        self.driver.get(self.main_url)
        self.sign_in(email, password)

    # TODO add a check to see if connected or not and the manage connection
    def sign_in(self, email, password):
        usename_place = self.driver.find_element_by_xpath(
            '//*[@id="session_key"]')
        usename_place.click()
        usename_place.send_keys(email)

        usename_place = self.driver.find_element_by_xpath(
            '//*[@id="session_password"]')
        usename_place.click()
        usename_place.send_keys(password)

        self.driver.find_element_by_xpath(
            '/html/body/main/section[1]/div[2]/form/button').click()

        try:
            confirmition = self.driver.find_element_by_xpath(
                '//*[@id="ember512"]/button[1]')
            confirmition.click()

        except:
            None

        # TODO arrange until
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ember41"]/input')))

    def search(self, search_string):
        search_bar = self.driver.find_element_by_xpath(
            '//*[@id="ember41"]/input')
        search_bar.send_keys(search_string)
        search_bar.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-result__wrapper')))

    def parse_search_results(self):
        html_source = self.driver.page_source
        soup = bs(html_source, "html")
        search_object_list = []
        for el in soup.find_all("div", class_="search-result__wrapper"):
            search_object_list.append(self.parse_single_elment(el))

        return search_object_list

    def parse_single_elment(self, banner_element):
        # TODO manage a state and log if more then 1 finding
        # TODO add shared connections url search and parse
        # TODO add shared connections count
        result = {}
        result['name'] = [element.text for element in banner_element.find_all(
            "span", class_="name actor-name")][0]
        result['profile_url'] = self.main_url+[element["href"]
                                               for element in banner_element.find_all("a", class_="search-result__result-link ember-view")][0]
        result['role'] = [element.text for element in banner_element.find_all(
            "p", class_="subline-level-1 t-14 t-black t-normal search-result__truncate")][0]
        result['location'] = [element.text for element in banner_element.find_all(
            "p", class_="subline-level-2 t-12 t-black--light t-normal search-result__truncate")][0]

        return result


def get_users_by_search(search_string):
    # TODO Make it headless
    # TODO add headers to vonnevt as his default browser?
    linkedin_instance = LinkedinInstance(
        test_data['email'], test_data['password'])
    linkedin_instance.sign_in()
    linkedin_instance.search(search_string)
    linkedin_instance.parse_search_results()


if __name__ == "__main__":
    # TODO remove test data and get parmaters
    test_data = json.loads(open('mocks\FB_TEST.json', 'r').read())
    test = get_users_by_search('Aviv Sharon')
