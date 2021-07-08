from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from random import uniform
from selenium.webdriver.remote.webdriver import WebDriver

############### 쇼핑 키워드추천 및 연관검색어 크롤러 #######################

def get_shopping_keyword_and_relatedword(keyword:str, driver:WebDriver):

    # 쇼핑 페이지 이동
    driver.get("https://search.shopping.naver.com/search/all?query="+keyword)
    soup = BeautifulSoup(driver.page_source, "lxml")

    find_where_recommend = [] # 키워드추천이 어디에 있는지 찾기 위한 변수

    # div의 개수를 구함
    div_length=len(soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.filter_finder__1Gtei > div > div"))

    time.sleep(uniform(1.0, 1.5))

    for i in range(1, div_length+1):
        is_keyword=driver.find_elements_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[1]"%i) # 키워드 추천아 있는지 없는지 확인하기 위함
        [find_where_recommend.append(word.text.replace('\n', '')) for word in is_keyword]  # 분류들을 리스트에 저장

    length = len(find_where_recommend) # 분류들의 개수

    # 더보기 버튼 선택 
    for i in range(0, length):

        if find_where_recommend[i]=='키워드추천더보기' or find_where_recommend[i]=='키워드추천': # 리스트에 키워드 추천이 있을 경우
            try:
                driver.find_element_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[1]/a"%(i+1)).click()
            except ElementNotInteractableException or NoSuchElementException or AttributeError or Exception as e:
                time.sleep(uniform(1.0, 2.5))
            
            time.sleep(uniform(1.0, 2.5))
            soup = BeautifulSoup(driver.page_source, "lxml")
            
            # 키워드추천 크롤링
            keysuggest = driver.find_elements_by_xpath("//*[@id='__next']/div/div[2]/div[2]/div[2]/div/div[%d]/div[2]/div/ul/li"%(i+1))
      
            recommend_word = []
            [recommend_word.append(word.text.replace('\n', '')) for word in keysuggest]
            break
        else: # 리스트에 키워드 추천이 없을 경우
            if i==length-1:
                time.sleep(0.5)
                recommend_word = []

    
    soup = BeautifulSoup(driver.page_source, "lxml")
    time.sleep(uniform(1.0, 2.5))
        
    # 연관검색어 크롤링
    relation_keywords = soup.select("#__next > div > div.style_container__1YjHN > div.relatedTags_relation_tag__2sDdc > div > ul > li")
    related_words = []
    
    # 연관검색어들을 리스트에 저장
    [related_words.append(word.text) for word in relation_keywords]
        
    print("◆ 네이버 쇼핑사이트 키워드추천, 연관검색어 수집 완료")

    return recommend_word+related_words


