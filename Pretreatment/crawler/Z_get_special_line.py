"""
可无视此py
爬取各个专业录取分数线，实现不了，用selenium容易被封；直接上request的数据需要解密method: aes-256-cbc，我破解不出来
"""
import pyppeteer
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import multiprocessing


chrome_options = Options()
No_Image_loading = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", No_Image_loading)
chrome_options.add_argument('--headless')


def main(year):
    with open(f'../result/{year}special_school_line.txt', 'w') as f:
        pass
    browser.get(f'https://gkcx.eol.cn/linespecialty?province=&schoolyear={year}')
    last_page = browser.find_elements_by_css_selector('.fypages ul li')[-1]
    browser.execute_script("arguments[0].click();", last_page)
    all_page = eval(browser.find_elements_by_css_selector('.fypages ul li')[-3].text)
    print(year, all_page)
    browser.get(f'https://gkcx.eol.cn/linespecialty?province=&schoolyear={year}')
    for page in range(1, all_page):
        if page % 50 == 0:
            print(year, page)
        time.sleep(0.3)
        table = browser.find_elements_by_css_selector('.search-table tbody tr')
        txt = ''
        try:
            for row in table:
                txt += str(year) + ' ' + row.text + '\n'
        except:
            pass
        with open(f'../result/{year}special_school_line.txt', 'a') as f:
            f.write(txt)
        next_page = browser.find_elements_by_css_selector('.fypages ul li')[-2]
        browser.execute_script("arguments[0].click();", next_page)


if __name__ == '__main__':
    browser = webdriver.Chrome(options=chrome_options)
    years = [i for i in range(2014, 2019+1)]
    for year in years:
        main(year)
