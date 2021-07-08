from bs4 import BeautifulSoup
import time
from random import uniform
from selenium.webdriver.remote.webdriver import WebDriver

############### 쇼핑 타이틀, 카테고리 크롤러 ###############
category=[]

def get_category_title(keyword:str, driver:WebDriver):

    category_tmp=[]
    title=[]
    shopping_title=[]

    # 쇼핑 페이지 이동
    url = "https://search.shopping.naver.com/search/all?origQuery="+keyword+"&pagingIndex={}&pagingSize=40&productSet=total&query="+keyword+"&sort=rel&timestamp=&viewType=list"
    
    # 1페이지 부터 3페이지까지 크롤링
    for i in range(1, 4):
        link = url.format(i)
        driver.get(link)
        time.sleep(uniform(1.0, 2.0))

        #스크롤 끝까지 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(uniform(1.5, 2.0))
        soup = BeautifulSoup(driver.page_source, "lxml")
        time.sleep(uniform(1.5, 2.5))

        # 카테고리
        length = len(soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div"))

        for j in range(1, length+1) :
            get_title = soup.select("#__next > div > div > div > div > div > ul > div > div:nth-child(%d) > li > div > div > div.basicList_title__3P9Q7 > a"%j) # 타이틀
             # 모든 타이틀 저장
            for word in get_title:
                title=word.text.split()
                shopping_title+=title
        time.sleep(uniform(2.0, 3.0))

        # 모든 카테고리 리스트 저장
        for k in range(1, length+1):
            category_words = []
            category_a = soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_depth__2QIie > a"%k)
            [category_words.append(word.text) for word in category_a]
            category_tmp.append(category_words)
       
    # category_tmp 리스트에 있는 내용 중복 제거
    for v in category_tmp:
        if v not in category:
            category.append(v)

    print("◆ 네이버 쇼핑 사이트 카테고리, 타이틀 수집 완료")
    return shopping_title

def get_category():
    return category

