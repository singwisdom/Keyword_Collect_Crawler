from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

############### 쇼핑 키워드추천 및 연관검색어 크롤러 ###############################

def GetShopping_keyword_and_relatedword(keyword):

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
    driver.get("https://search.shopping.naver.com/search/all?query="+keyword)
        
    htmlSource = driver.page_source

    soup = BeautifulSoup(htmlSource, "lxml")
    words = []
    new_words=[]

    # div의 개수를 구함
    length=len(soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.filter_finder__1Gtei > div > div"))


    for i in range(1,length+1):
        iskeyword=driver.find_elements_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[1]"%i)

        # 분류들을 리스트에 저장a
        for word in iskeyword:
            words.append(word.text.replace('\n',''))

    # 더보기 버튼 선택 

    for i in range(0,len(words)):

        if(words[i]=='키워드추천더보기'):
            tmp=i
            driver.find_element_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[1]/a"%(tmp+1)).click()
            soup = BeautifulSoup(htmlSource, "lxml")
            time.sleep(1)

            # 키워드추천 크롤링
            keysuggest = driver.find_elements_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[2]/div/ul/li"%(tmp+1))
            # word = [word.text.replace('\n','') for word in keysuggest]        

            words = []
            for word in keysuggest:
                words.append(word.text.replace('\n',''))
        elif(words[i]=='키워드추천'):
            tmp=i
            driver.find_element_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[1]/a"%(tmp+1)).click()
            soup = BeautifulSoup(htmlSource, "lxml")
            time.sleep(1)

            # 키워드추천 크롤링
            keysuggest = driver.find_elements_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[2]/div/ul/li"%(tmp+1))
            # word = [word.text.replace('\n','') for word in keysuggest]        

            words = []
            for word in keysuggest:
                words.append(word.text.replace('\n',''))
        else:
            if(i==len(words)-1):
                time.sleep(0.5)
                words = []

    
    soup = BeautifulSoup(htmlSource, "lxml")
    time.sleep(0.9)
        
    # 연관검색어 크롤링
    relationKeywords = soup.select("#__next > div > div.style_container__1YjHN > div.relatedTags_relation_tag__2sDdc > div > ul>li")


    related_words = []
    # 연관검색어들을 리스트에 저장
    for word in relationKeywords:
        related_words.append(word.text)


    driver.quit()
    new_words=words+related_words

    return new_words


