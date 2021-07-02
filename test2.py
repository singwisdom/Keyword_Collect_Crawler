from unicodedata import category
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import openpyxl
import time

############### 데이터랩 크롤러 ###############################

find=['생활/건강', '주방용품', '주방잡화', '일회용식기']

#Workbook 생성
wb = openpyxl.Workbook()

#Sheet 활성
sheet = wb.active

#sheet 이름 설정
wb.title="자동완성어"

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

driver.get("https://datalab.naver.com/shoppingInsight/sCategory.naver")
htmlSource = driver.page_source

soup = BeautifulSoup(htmlSource, "lxml")
time.sleep(2)

# 1분류 선택
first = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(1) > ul > li")

words = []
# 자동완성어들을 리스트에 저장
for word in first:
    words.append(word.text)
print(words)

time.sleep(2)

for i in range(len(words)):  
    if(words[i]==find[0]):
        print(words[i])
        print(i)
        element = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li["+str(i+1)+"]/a")
        driver.execute_script("arguments[0].click();",element)

time.sleep(2)
htmlSource = driver.page_source
soup = BeautifulSoup(htmlSource, "lxml")

##### 2분류 선택 #########
second = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(2) > ul > li")
#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(2) > ul

words2 = []
# 자동완성어들을 리스트에 저장
for word in second:
    words2.append(word.text)
print(words2)

time.sleep(2)

for i in range(len(words2)):  
    if(words2[i]==find[1]):
        print(words2[i])
        element = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li["+str(i+1)+"]/a")
        driver.execute_script("arguments[0].click();",element)

time.sleep(3)
