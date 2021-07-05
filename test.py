from unicodedata import category
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl


#검색어를 입력
print("검색어를 입력해주세요:")
keyword=input()

############### 쇼핑 키워드 추천 크롤러 ###############################


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

#더보기 선택 (예외처리)
try:
    soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.filter_finder__1Gtei > div > div.filter_finder_col__3ttPW.filter_is_active__3qqoC > div.filter_finder_tit__2VCKd > a").click() #더보기 버튼 클릭

    driver.implicitly_wait(1)
except:
    driver.implicitly_wait(1)

soup = BeautifulSoup(htmlSource, "lxml")

#키워드추천 크롤링
# keysuggest = driver.find_elements_by_css_selector("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.filter_finder__1Gtei > div > div.filter_finder_col__3ttPW.filter_is_active__3qqoC > div.filter_finder_row__1rXWv > div > ul >li")
keysuggest = soup.select("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.filter_finder__1Gtei > div > div.filter_finder_col__3ttPW.filter_is_active__3qqoC > div.filter_finder_row__1rXWv > div > ul >li")
driver.implicitly_wait(1)

words = []
for word in keysuggest:
    words.append(word.text.replace('\n',''))
print(words)

driver.quit()

