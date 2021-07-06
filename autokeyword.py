import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from random import *

############### 자동완성어 크롤러 ###############################

def GetAutokeyword(keyword):
    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()
    # options.add_argument('headless') # 헤드리스
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    # 대기 설정
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족

    # 자동완성어 페이지 이동
    driver.get("https://www.naver.com/")
    htmlSource = driver.page_source


    findelem = driver.find_element_by_name("query")
    findelem.send_keys(keyword)
    time.sleep(uniform(2.0,4.0))

    soup = BeautifulSoup(htmlSource, "lxml")
    time.sleep(uniform(2.0,5.0))
   

    #자동완성어 크롤링
    relationKeywords =driver.find_elements_by_css_selector("#autoFrame > div > div > div.atcmp_fixer._atcmp_layer > div.atcmp_container._words > ul > li")

    words = []

    # 자동완성어들을 리스트에 저장
    for word in relationKeywords:
        words.append(word.text.replace('\n추가',''))

    driver.quit()
    return words
    







    
