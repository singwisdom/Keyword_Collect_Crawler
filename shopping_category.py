from unicodedata import category
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


############### 쇼핑 카테고리 크롤러 ###############################


print("검색어를 입력해주세요:")
keyword=input()

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

    # 1페이지 부터 3페이지까지 크롤링
    for i in range(1,6):
        link = url.format(i)
        driver.get(link)
        driver.implicitly_wait(1)

        htmlSource = driver.page_source

        #스크롤 끝까지 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        driver.implicitly_wait(1)

        soup = BeautifulSoup(htmlSource, "lxml")

        #카테고리
        # category = driver.find_elements_by_class_name("basicList_depth__2QIie")
        category = soup.select(".basicList_depth__2QIie")
        

        # 모든 카테고리 리스트 저장
        for word in category:
            words.append(word.text)

    driver.quit() #종료

    # words 리스트에 있는 내용 중복 제거
    for v in words:
        if v not in new_words:
            new_words.append(v)
    return new_words

   
    
print(getCategory(keyword))