from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

############### 쇼핑 카테고리 크롤러 ###############################

def getCategory(keyword):

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
    
    
    #추천검색어
    keysuggest = driver.find_elements_by_class_name("filter_finder_list__16XU5")

    words = []
    new_words=[]
    category=[]

    # 1페이지 부터 3페이지까지 크롤링
    for i in range(1,4):
        link = url.format(i)
        driver.get(link)
        driver.implicitly_wait(1)

        htmlSource = driver.page_source

        #스크롤 끝까지 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(2)

        soup = BeautifulSoup(htmlSource, "lxml")
        time.sleep(0.5)

        # 카테고리
        category_length = len(soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div"))
       

        # 모든 카테고리 리스트 저장
        for k in range(1,category_length+1):
            words=[]
            category_a = soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(%d) > li > div > div.basicList_info_area__17Xyo > div.basicList_depth__2QIie > a"%k)
            [words.append(word.text) for word in category_a]
            # for word in category_a:
            #     words.append(word.text)
            new_words.append(words)
    

    driver.quit() #종료

    # new_words 리스트에 있는 내용 중복 제거
    for v in new_words:
        if v not in category:
            category.append(v)
    return category

