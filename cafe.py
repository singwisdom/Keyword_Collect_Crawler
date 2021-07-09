from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from random import uniform
from selenium.webdriver.chrome.webdriver import WebDriver

############### 카페 연관검색어 크롤러 ###############################
def get_cafe_keyword(keyword: str, driver:WebDriver):

    cafe_words = []

    # 카페 페이지 이동
    driver.get("https://section.cafe.naver.com/")
    
    driver.find_element_by_css_selector("#header > div.snb_area > div > form > fieldset > div > div > input").send_keys(keyword) # 검색창에 입력할 키워드 받고 입력
    driver.find_element_by_css_selector("#header > div.snb_area > div > form > fieldset > div > button > span.ico_search").click() # 검색 조회
    time.sleep(uniform(2.0, 3.0))

    # 더보기 버튼 누르기
    try:
        driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[1]/div[1]/div/a").click()
        driver.implicitly_wait(1)
    except NoSuchElementException or Exception as e:
        driver.implicitly_wait(1)

    soup = BeautifulSoup(driver.page_source, "lxml")
    time.sleep(uniform(2.0, 3.5))

    #카페 연관검색 수집
    try:
        cafe_keywords = driver.find_elements_by_class_name("relation_search_item")
        time.sleep(uniform(2.0, 3.5))
    except NoSuchElementException or Exception as e:
        print("※ 해당 키워드는 카페 연관검색어가 존재하지 않습니다. ※")

    [cafe_words.append(word.text) for word in cafe_keywords]
    
    if len(cafe_words)==0 :
        print("※ 해당 키워드는 카페 연관검색어가 존재하지 않습니다. ※")
    return cafe_words