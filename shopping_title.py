from unicodedata import category
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import openpyxl

################# 쇼핑 목록 타이틀 크롤러 ########################

print("검색어를 입력해주세요:")
keyword=input()

#Workbook 생성
wb = openpyxl.Workbook()

#Sheet 활성
sheet = wb.active

#sheet 이름 설정
wb.title="자동완성어"

#데이터 프레임 내 변수명 생성
sheet.append(["결과"])

    
options = webdriver.ChromeOptions()

options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")

driver = webdriver.Chrome("chromedriver", chrome_options=options)

wait = WebDriverWait(driver,5)
visible = EC.visibility_of_element_located

url = "https://search.shopping.naver.com/search/all?origQuery="+keyword+"&pagingIndex={}&pagingSize=40&productSet=total&query="+keyword+"&sort=rel&timestamp=&viewType=list"

words=[]

# 1페이지 부터 3페이지까지 크롤링 
for i in range(1,4):

    link=url.format(i)
    driver.get(link)

    htmlSource = driver.page_source
    
    #스크롤 끝까지 내림
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    time.sleep(1)

    soup = BeautifulSoup(htmlSource,"lxml")
        
    title = driver.find_elements_by_class_name("basicList_link__1MaTN")
    time.sleep(1)
       
    for word in title:
        # words=word.text.replace('/','').split() #여쭤보기 => '-' , '/' 이런 기호들은 삭제? 아니면 그냥 엑셀에 출력?
        words=word.text.split()

        for i in words:
            sheet.append([i])
        print(words)
    
driver.quit()

#엑셀파일명 설정 및 저장
wb.save("쇼핑타이틀.xlsx")


