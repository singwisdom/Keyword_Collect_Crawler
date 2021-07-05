import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shopping_category import getCategory
from random import *

############### 데이터랩 크롤러 ###############################

#검색어를 입력
print("검색어를 입력해주세요:")
keyword=input()

data=[]

def GetDatalab(keyword):

    #카테고리 모듈에서 카테고리를 받아옴
    find=getCategory(keyword)
    print(find)

    #카테고리의 길이
    length = len(find)

    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()

    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    # find의 길이만큼 반복
    for j in range(0,length):

        # 대기 설정
        wait = WebDriverWait(driver, 3)
        visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족

        driver.get("https://datalab.naver.com/shoppingInsight/sCategory.naver")
        htmlSource = driver.page_source

        soup = BeautifulSoup(htmlSource, "lxml")


        ###### 1분류 선택 #########
        first = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(1) > ul > li")

        words1 = []
        # 분류들을 리스트에 저장
        [words1.append(word.text) for word in first]


        for i in range(len(words1)):  
            if(words1[i]==find[j][0]):
                print(words1[i])
                element = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li["+str(i+1)+"]/a")
                driver.execute_script("arguments[0].click();",element)

        time.sleep(2)

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, "lxml")

        ##### 2분류 선택 #########
        second = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(2) > ul > li")

        words2 = []
        # 분류들을 리스트에 저장
        for word in second:
            words2.append(word.text)

        for i in range(len(words2)):  
            if(words2[i]==find[j][1]):
                print(words2[i])
                element = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[2]/ul/li["+str(i+1)+"]/a")
                driver.execute_script("arguments[0].click();",element)

        time.sleep(2)

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, "lxml")

        ###### 3분류 선택 #########
        third = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(3) > ul > li")

        words3 = []
        # 분류들을 리스트에 저장
        for word in third:
            words3.append(word.text)

        for i in range(len(words3)):  
            if(words3[i]==find[j][2]):
                print(words3[i])
                element = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[3]/ul/li["+str(i+1)+"]/a")
                driver.execute_script("arguments[0].click();",element)

        time.sleep(2)

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, "lxml")

        ###### 4분류 선택 #########
        four = soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(4) > ul > li")

        words4 = []
        # 분류들을 리스트에 저장
        for word in four:
            words4.append(word.text)

        for i in range(len(words4)):  
            if(words4[i]==find[j][3]):
                print(words4[i])
                element = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[4]/ul/li["+str(i+1)+"]/a")
                driver.execute_script("arguments[0].click();",element)
        time.sleep(2)


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


        data=[]

        #인기 검색어 10페이지까지 크롤링
        count = 1
        for i in range(1,11):

            soup = BeautifulSoup(htmlSource, "lxml")
            time.sleep(3)

            #다음 페이지로 넘어가기
            driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]").click()
            
            time.sleep(2.7)

            PopularKeywords =driver.find_elements_by_class_name("link_text")

            time.sleep(3.1)
        
        
            for word in PopularKeywords:
                data.append(word.text[len(str(count)):])
                count += 1

            time.sleep(2)

        new_words=[]

        # 앞에 필요없는 부분 제거
        for v in data:
                new_words.append(v.replace('\n',''))

        # 데이터들을 하나로 합침
        data+=new_words
    
    driver.quit()

    return data

print(GetDatalab(keyword))

