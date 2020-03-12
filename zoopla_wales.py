import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
import time
import datetime
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup

codes = []
path = "C:\\Users\\Business\\Downloads\\geckodriver-v0.26.0-win64\\geckodriver.exe"
driver = Firefox(executable_path=path)
browser = driver

pages = [1]
for page in pages:
    price = 'https://www.zoopla.co.uk/for-sale/property/wales/?keywords=HMO&identifier=wales&q=Wales&is_shared_ownership=false&is_retirement_home=false&search_source=home&radius=0&pn={}'.format(page)
    driver.get(price)

    no_of_houses = browser.find_element_by_class_name('listing-results').find_elements_by_tag_name("li")

    for item in no_of_houses:
        li_id = item.get_attribute('data-listing-id')
        print(li_id)
        if li_id!=None:
            codes.append(li_id)
print('========================================')
print(codes)
print('========================================')



for zips in codes:
    driver.get('https://www.zoopla.co.uk/for-sale/details/{}'.format(zips))
    address = browser.find_element_by_class_name('ui-property-summary__address').get_attribute('innerHTML')
    postal_code = browser.find_element_by_class_name('ui-property-summary__address').get_attribute('innerHTML').split(' ')
    length = len(postal_code)
    postal_code_new = postal_code[length-1]
    bedroom_exist = len(browser.find_element_by_class_name('dp-features-list').find_elements_by_tag_name('li'))
    bedroom = '0'
    if bedroom_exist >= 1:
        bedroom = browser.find_element_by_class_name('dp-features-list').find_elements_by_tag_name('li')[0].find_element_by_tag_name('span').get_attribute('innerHTML')
    bathroom_exist = len(browser.find_element_by_class_name('dp-features-list').find_elements_by_tag_name('li'))
    bathroom = '0'
    if bathroom_exist >= 2:
        bathroom = browser.find_element_by_class_name('dp-features-list').find_elements_by_tag_name('li')[1].find_element_by_tag_name('span').get_attribute('innerHTML')
    reception = '0'
    reception_exist = len(browser.find_element_by_class_name('dp-features-list').find_elements_by_tag_name('li'))
    if reception_exist >= 3:
        reception = browser.find_element_by_class_name('dp-features-list').find_elements_by_tag_name('li')[2].find_element_by_tag_name('span').get_attribute('innerHTML')
    property_price = browser.find_element_by_class_name('ui-pricing__main-price').get_attribute('innerHTML').replace('£','').replace(',','')
    property_type = browser.find_element_by_class_name('ui-property-summary__title').get_attribute('innerHTML')
    first_listed_date = browser.find_element_by_class_name('dp-price-history__item-date').get_attribute('innerHTML')
    first_listed_date_new = browser.find_element_by_class_name('dp-price-history__item-date').get_attribute('innerHTML').replace('th','').replace('rd','').replace('nd','').replace('st','')
    agent_name = browser.find_element_by_class_name('ui-agent__name').get_attribute('innerHTML')
    Price_Changes = '0'
    last_sold = '0'
    last_sold_exist = len(browser.find_element_by_class_name('dp-price-history-block').find_elements_by_tag_name('div'))
    if last_sold_exist==2:
        last_sold =browser.find_element_by_class_name('dp-price-history-block').find_elements_by_tag_name('div')[1].find_elements_by_tag_name('span')[1].get_attribute('innerHTML').replace('£','').replace(',','')
        Price_Changes = int(property_price) - int(last_sold)
    date1 = datetime.datetime.strptime('{}'.format(first_listed_date_new), '%d %b %Y').strftime('%d,%m,%Y')
    today = date.today()
    today_new = datetime.datetime.strptime('{}'.format(today),'%Y-%m-%d').strftime('%d,%m,%Y')
    def days_between(d1, d2):

        d1 = datetime.datetime.strptime(d1,'%d,%m,%Y')
        d2 = datetime.datetime.strptime(d2,'%d,%m,%Y')
        return abs((d2 - d1).days)

    Changes_date = days_between('{}'.format(today_new),'{}'.format(date1))


    print('Address-:'+address)
    print('Bedrooms-:'+bedroom)
    print('Bathrooms-:'+bathroom)
    print('Reception Room=:'+reception)
    print('Property Type-:'+property_type)
    print('Property Price-:'+property_price)
    print('Price Changes-:',Price_Changes)
    print('Last Sold-:'+last_sold)
    print('Detail URL-:'+'https://www.zoopla.co.uk/for-sale/details/{}?featured=1&utm_content=featured_listing'.format(zips))
    print('First Listed Date-:'+first_listed_date)
    print('Time since first listed-:',Changes_date,'Days')
    print('Agent Name-:'+agent_name)
    print('Postal Code-:'+postal_code_new)




    print('=======================================')
    time.sleep(3)



browser.quit()
