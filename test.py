import re
import openpyxl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#ppt 1페이지 쇼핑 - 자동완성어 크롤러

print("검색어를 입력해주세요:")
keyword=input()

#Workbook 생성
wb = openpyxl.Workbook()

#Sheet 활성
sheet = wb.active

#sheet 이름 설정
wb.title="자동완성어"

def getHtmlSource(keyword):
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
    driver.find_element_by_xpath("//*[@id='search_btn']/span[2]")

    soup = BeautifulSoup(htmlSource, "lxml")
    key = soup.select("#autoFrame > div > div > div.atcmp_fixer._atcmp_layer > div.atcmp_container._words > ul > li")

    #자동완성어 크롤링
    relationKeywords =driver.find_elements_by_css_selector("#autoFrame > div > div > div.atcmp_fixer._atcmp_layer > div.atcmp_container._words > ul > li")

    words = []
    for word in relationKeywords:
        words.append(word.text.replace('\n추가',''))
    return words

    driver.quit()

print((getHtmlSource(keyword)))