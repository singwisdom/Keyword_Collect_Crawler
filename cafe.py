from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from random import uniform
from selenium.webdriver.chrome.webdriver import WebDriver

############### 카페 연관검색어 크롤러 ###############################

def get_cafe_keyword(keyword: str, driver:WebDriver):

    # 카페 페이지 이동
    driver.get("https://section.cafe.naver.com/")
    
    #검색창에 입력할 키워드 받고 입력
    driver.find_element_by_css_selector("#header > div.snb_area > div > form > fieldset > div > div > input").send_keys(keyword)
    time.sleep(uniform(2.0, 3.0))

    #검색 조회
    driver.find_element_by_css_selector("#header > div.snb_area > div > form > fieldset > div > button > span.ico_search").click()
    time.sleep(uniform(2.0, 3.0))

    # 더보기 버튼 누르기
    try:
        driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[1]/div[1]/div/a").click()
        driver.implicitly_wait(1)
    except NoSuchElementException:
        driver.implicitly_wait(1)

    soup = BeautifulSoup(driver.page_source, "lxml")
    time.sleep(uniform(2.0, 3.5))

    #카페 연관검색 크롤링
    try:
        cafe_keywords = driver.find_elements_by_class_name("relation_search_item")
        time.sleep(uniform(2.0, 3.5))
    except NoSuchElementException:
        print("※ 해당 키워드는 카페 연관검색어가 존재하지 않습니다. ※")

    cafe_words = []

    print("◆ 카페 연관검색어 수집 완료")
    return [cafe_words.append(word.text.replace('\n', '')) for word in cafe_keywords]

