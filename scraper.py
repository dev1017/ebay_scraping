import os
from csv import DictWriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

keyword = input('\nKeyword: ')

field_names = ['seller', 'score']

if not os.path.exists(keyword+'.csv'):
    dict={'seller': 'Seller Name', 'score': 'Score'}
    with open(keyword+'.csv', 'a+', newline='', encoding="utf-8") as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames = field_names)
        dictwriter_object.writerow(dict)
        f_object.close()

chromeOptions = Options()
chromeOptions.add_argument('--headless')
chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
chromeOptions.add_argument('--log-level=3')
list_browser = webdriver.Chrome(ChromeDriverManager().install(),options=chromeOptions)
detail_browser = webdriver.Chrome(ChromeDriverManager().install(),options=chromeOptions)

list_browser.get('https://www.ebay.de/sch/i.html?&_nkw=' + keyword + '&_sacat=0')

data = []

print('')

while True:
    soup = BeautifulSoup(list_browser.page_source, 'html.parser')
    product_urls = soup.find_all("a", {"class": "s-item__link"})
    flag = 0
    for link in product_urls:
        if flag:
            detail_browser.get(link['href'])
            detail_page = BeautifulSoup(detail_browser.page_source, 'html.parser')
            seller = detail_page.find("span", {"class": "mbg-nw"}).text
            score = detail_page.find("span", {"class": "mbg-l"}).find("a").text
            print(seller,"(",score,")")
            if seller in data:
                continue
            dict={'seller': seller, 'score': score}
            with open(keyword+'.csv', 'a+', newline='', encoding="utf-8") as f_object:
                dictwriter_object = DictWriter(f_object, fieldnames = field_names)
                dictwriter_object.writerow(dict)
                f_object.close()
            data.append(seller)
        else:
            flag = 1
    try:
        next_btn = list_browser.find_element_by_css_selector('.pagination__next')
        if next_btn.get_attribute("aria-disabled") == 'true':
            break
        else:
            next_btn.click()
    except:
        break

print("\n*************************\n********** End **********\n*************************\n")