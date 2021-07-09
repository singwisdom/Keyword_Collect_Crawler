from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from random import uniform
from selenium.webdriver.chrome.webdriver import WebDriver

# ############### 블로그 연관검색어 크롤러 ###############################

def get_blog_keyword(keyword:str, driver:WebDriver):

    blog_words = []

    # 블로그 페이지 이동
    driver.get("https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0")

    driver.find_element_by_name("sectionBlogQuery").send_keys(keyword) # 검색창에 입력할 키워드 받고 입력
    driver.find_element_by_xpath("//*[@id='header']/div[1]/div/div[2]/form/fieldset/a[1]/i").click() # 검색 조회
    soup = BeautifulSoup(driver.page_source, "lxml")
    time.sleep(uniform(1.0, 2.0))

    try:
        blog_keywords = driver.find_elements_by_css_selector("#container > div > aside > div > div.area_keyword > div.list > a") # 블로그 연관검색 
    except  NoSuchElementException or ElementNotInteractableException or Exception as e:
        print("※ 해당 키워드는 블로그 연관검색어가 존재하지 않습니다. ※")

    [blog_words.append(word.text) for word in blog_keywords]

    if len(blog_words)==0 :
        print("※ 해당 키워드는 블로그 연관검색어가 없습니다. ※" )
    return blog_words