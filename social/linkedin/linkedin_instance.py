from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from webdriver_manager.chrome import ChromeDriverManager

import time
from dynaconf import settings
from bs4 import BeautifulSoup as bs
import json


class LinkedinInstance:
    def __init__(self, email, password):
        # display = Display(visible=0, size=(1024, 768))
        # display.start()
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--allow-running-insecure-content')
        # chrome_options.add_argument("--window-size=1920x1080")
        # binary = FirefoxBinary('C:\\Users\\FourI\\OneDrive\\Desktop\\Omri\\webdriver\\geckodriver')
        self.driver = webdriver.Firefox()
        self.main_url = 'https://www.linkedin.com'
        # self.driver = webdriver.Chrome("/home/ubuntu/chrome_driver/chromedriver", chrome_options=chrome_options)
        self.driver.get(self.main_url)
        if self.driver.find_element_by_xpath('//*[@id="session_key"]'):
            print('[LinkedinInstance] Sign-in requierd')
            self.sign_in(email, password)

    # TODO add a check to see if connected or not and the manage connection
    def sign_in(self, email, password):
        print('[LinkedinInstance][sign-in]  Starting')
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
        print('[LinkedinInstance][sign-in] Success')
        # TODO arrange until
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-global-typeahead__input')))

    def search(self, search_string):
        print('[LinkedinInstance][search] search_string=' + search_string)
        search_bar = self.driver.find_element_by_class_name(
            'search-global-typeahead__input')
        search_bar.send_keys(search_string)
        search_bar.send_keys(Keys.ENTER)
        # TODO fix it to lazy wait prooperly
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-result__wrapper')))
        time.sleep(1)

    def parse_search_results(self):
        html_source = self.driver.page_source
        soup = bs(html_source, "html")
        search_object_list = []
        for el in soup.find_all("div", class_="search-result__wrapper"):
            search_object_list.append(self.parse_single_elment(el))

        return search_object_list

    def parse_single_elment(self, banner_element):
        # TODO manage a state and log if more then 1 finding
        # TODO ass scroll Down
        # TODO add shared connections url search and parse
        # TODO add shared connections count
        result = {}
        result['name'] = [element.text for element in banner_element.find_all(
            "span", class_="name actor-name")][0]
        result['profile_url'] = self.main_url + [element["href"]
                                                 for element in banner_element.find_all("a",
                                                                                        class_="search-result__result-link ember-view")][
            0]
        result['role'] = [element.text for element in banner_element.find_all(
            "p", class_="subline-level-1 t-14 t-black t-normal search-result__truncate")][0]
        result['location'] = [element.text for element in banner_element.find_all(
            "p", class_="subline-level-2 t-12 t-black--light t-normal search-result__truncate")][0]
        try:
            result['profile_img'] = [element['src'] for element in banner_element.findChildren(
                "img")][0]
        except:
            None
            # TODO LOG this
        return result

    def get_users_by_search(self, search_string):
        # TODO Make it headless
        # TODO add headers to connect as his default browser?

        self.search(search_string)
        return json.dumps(self.parse_search_results())


def test_instance():
    test_data = json.loads(open(r'mocks\FB_TEST.json', 'r').read())
    return LinkedinInstance(
        test_data['email'], test_data['password'])


if __name__ == "__main__":
    # TODO remove test data and get parmaters
    test = test_instance()
    test = test.get_users_by_search('Aviv Sharon')
    print()
