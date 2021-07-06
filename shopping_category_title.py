from unicodedata import category
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import *

############### 쇼핑 타이틀, 카테고리 크롤러 ###############################

category=[]

def getCategory_Title(keyword):

    tmp=[]
    title=[]
    new_title=[]

    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()

    # options.add_argument('headless') # 헤드리스
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    # 대기 설정
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족


    # 쇼핑 페이지 이동
    url = "https://search.shopping.naver.com/search/all?origQuery="+keyword+"&pagingIndex={}&pagingSize=40&productSet=total&query="+keyword+"&sort=rel&timestamp=&viewType=list"
    

    # 1페이지 부터 3페이지까지 크롤링
    for i in range(1,4):
        link = url.format(i)
        driver.get(link)
        time.sleep(uniform(2.0,5.0))

        htmlSource = driver.page_source

        #스크롤 끝까지 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(uniform(3.0,5.0))

        soup = BeautifulSoup(htmlSource, "lxml")
        time.sleep(uniform(3.0,5.0))

        # 카테고리
        category_length = len(soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div"))
        time.sleep(uniform(2.0,4.5))


        # 타이틀
        get_title = driver.find_elements_by_class_name("basicList_link__1MaTN")
        time.sleep(uniform(2.0,4.5))

        
        # 모든 카테고리 리스트 저장
        for k in range(1,category_length+1):
            category_words = []
            category_a = soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_depth__2QIie > a"%k)
            [category_words.append(word.text) for word in category_a]
            tmp.append(category_words)

        # 모든 타이틀 저장
        for word in get_title:
            title=word.text.split()
            new_title+=title


    driver.quit() #종료

    # new_words 리스트에 있는 내용 중복 제거
    for v in tmp:
        if v not in category:
            category.append(v)

    return new_title


def GetCategory():

    return category


