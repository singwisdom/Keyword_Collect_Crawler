import time
from bs4 import BeautifulSoup
from random import uniform
from selenium.webdriver.chrome.webdriver import WebDriver

############### 자동완성어 크롤러 ###############################

def get_auto_keyword(keyword:str, driver:WebDriver):

    # 자동완성어 페이지 이동
    driver.get("https://www.naver.com/")

    driver.find_element_by_name("query").send_keys(keyword) # 검색창을 찾고 키워드 입력
    soup = BeautifulSoup(driver.page_source, "lxml")
    time.sleep(uniform(1.0,2.0))

    #자동완성어 크롤링
    auto_keyword =driver.find_elements_by_css_selector("#autoFrame > div > div > div.atcmp_fixer._atcmp_layer > div.atcmp_container._words > ul > li")

    auto_words = []
    # 자동완성어들을 리스트에 저장
    [auto_words.append(word.text.replace('\n추가','')) for word in auto_keyword]
    return auto_words
        
    







    
