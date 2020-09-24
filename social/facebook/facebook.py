from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
import time


def get_users_by_search(email, password, search_string):
    driver = login_facebook(email, password)
    page = search_page(driver, search_string)
    links = get_relevant_profile_links(page)
    all_users = extract_data(links, driver)
    return json.dumps(all_users)


def login_facebook(email, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
    driver.get('https://www.facebook.com/login.php')
    driver.find_element_by_id('email').send_keys(email)
    driver.find_element_by_id('pass').send_keys(password)
    driver.find_element_by_id('loginbutton').click()
    return driver


def search_page(driver, search_string):
    time.sleep(10)
    driver.get('https://www.facebook.com/search/top/?q={}'.format(search_string))
    time.sleep(10)
    html_source = driver.page_source
    soup = bs(html_source, "html.parser")
    return soup


def get_relevant_profile_links(soup):
    relevant_profiles = []
    for el in soup.find_all("div",
                            class_="rq0escxv l9j0dhe7 du4w35lb hybvsw6c ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi ni8dbmo4 stjgntxs k4urcfbm sbcfpzgs"):
        for element in el.find_all("a",
                                   class_="oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l oo9gr5id"):
            relevant_profiles.append(element["href"])
    return relevant_profiles


def extract_data(relevant_profiles, driver):
    final_results = []
    for profile in relevant_profiles[0:3]:
        profile_results = {}
        driver.get(profile)
        time.sleep(10)
        html_source = driver.page_source
        soup = bs(html_source, "html.parser")
        profile_results["name"] = get_name(soup)
        profile_results["intro"] = get_intro(soup)
        profile_results["img"] = get_profile_img(soup)
        profile_results["facebook_profile_link"] = profile
        final_results.append(profile_results)
    return final_results


def get_profile_img(soup):
    return soup.find_all("body", "_6s5d _71pn _-kb segoe")[0].find_all("link")[0]["href"]


def get_intro(soup):
    full_intro = []
    intro = soup.find_all("div",
                          class_="rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr p8fzw8mz pcp91wgn iuny7tx3 ipjc6fyt")[
        0]
    intro = intro.find_all('ul')[0]
    for elem in intro:
        subject = elem.find_all("span",
                                class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i jq4qci2q a3bd9o3v knj5qynh oo9gr5id hzawbc8m")[
            0].text
        full_intro.append(subject)
    return full_intro


def get_name(soup):
    name_span = soup.find_all("span",
                              class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 qg6bub1s fe6kdd0r mau55g9w c8b282yb teo7jy3c mhxlubs3 p5u9llcw hnhda86s oo9gr5id oqcyycmt")[
        0]
    return name_span.find_all("h1", class_="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80")[0].text
