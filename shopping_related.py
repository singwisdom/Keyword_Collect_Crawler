from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl


##############쇼핑 연관 검색어 크롤러##############

print("검색어를 입력해주세요:")
keyword=input()

#Workbook 생성
wb = openpyxl.Workbook()

#Sheet 활성
sheet = wb.active

#sheet 이름 설정
sheet.title="자동완성어"

#데이터 프레임 내 변수명 생성
sheet.append(["결과"])


# 크롬드라이버 옵션 설정

options = webdriver.ChromeOptions()
# options.add_argument('headless') # 헤드리스
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")

driver = webdriver.Chrome("chromedriver", chrome_options=options)

# 대기 설정
wait = WebDriverWait(driver, 3)
visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족

# 쇼핑 연관 검색어 페이지 이동
driver.get("https://search.shopping.naver.com/search/all?query="+keyword)

htmlSource = driver.page_source

soup = BeautifulSoup(htmlSource, "lxml")
    
# 연관검색어 크롤링
# relationKeywords = soup.select("#__next > div > div.style_container__1YjHN > div.relatedTags_relation_tag__2sDdc > div > ul>li")
relationKeywords = soup.select("#__next > div > div.style_container__1YjHN > div.relatedTags_relation_tag__2sDdc > div > ul>li")


words = []
# 연관검색어들을 리스트에 저장
for word in relationKeywords:
    words.append(word.text)

#엑셀에 저장
for i in words:
    sheet.append([i])

#엑셀로 저장
wb.save("쇼핑연관검색어.xlsx") 

driver.quit()



