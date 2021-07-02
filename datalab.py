from unicodedata import category
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

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

# 1분류 선택
first = driver.find_element_by_class_name("select_list scroll_cst")
li=first.find_elements_by_tag_name('li')
print(li)
# driver.implicitly_wait(1)

# #2분류 선택
# driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/span").click()
# driver.implicitly_wait(1)

# #3분류 선택
# driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul").click() 
# driver.implicitly_wait(1)
    
# #4분류 선택
# driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[4]/ul").click() 
# driver.implicitly_wait(1)


#기간 1년 선택
driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[2]/div[1]/span/label[3]").click()
driver.implicitly_wait(1)

#기기 전체 선택
driver.find_element_by_xpath("//*[@id='18_device_0']").click()
driver.implicitly_wait(1)

#성별 전체 선택
driver.find_element_by_xpath("//*[@id='19_gender_0']").click()
driver.implicitly_wait(1)

#연령 전체 선택
driver.find_element_by_xpath("//*[@id='20_age_0']").click()
driver.implicitly_wait(1)

#조회하기
driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/a").click()
driver.implicitly_wait(1)


words=[]

#인기 검색어 10페이지까지 크롤링
count = 1
for i in range(1,11):

    #다음 페이지로 넘어가기
    driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]").click()
     
    driver.implicitly_wait(1)

    soup = BeautifulSoup(htmlSource, "lxml")

    PopularKeywords =driver.find_elements_by_class_name("link_text")
  
   
    for word in PopularKeywords:
        words.append(word.text[len(str(count)):])
        count += 1

new_words=[]

# 앞에 필요없는 부분 정제
for v in words:
        new_words.append(v.replace('\n',''))


#엑셀에 저장
for i in new_words:
    sheet.append([i])

driver.quit()
    
wb.save("자동완성어.xlsx")
