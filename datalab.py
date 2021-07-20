import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from turn_on_chrome import turn_on_chrome_driver
from random import uniform

############### 데이터랩 크롤러 ##########################

def get_datalab(find:list, driver:WebDriver):  #카테고리 모듈에서 카테고리를 받아옴

    datalab_tmp=[] # 데이터랩에서 순위 저장할 리스트
    datalab_words=[] # 데이터랩에서 순위 저장하고 정제한 후 return 할 최종 리스트
    section=['', '', '', ''] # 1분류 부터 4분류까지 저장할 리스트

    driver.get("https://datalab.naver.com/shoppingInsight/sCategory.naver")

    try :

        for k in range(1, len(find)+1):
            soup = BeautifulSoup(driver.page_source, "lxml")
            time.sleep(uniform(1.0, 2.0))

            # try : 
            ######## 1 ~ 4 분류 선택 #########
            section[k-1]=soup.select("#content > div.section_instie_area.space_top > div > div.section.insite_inquiry > div > div > div:nth-child(1) > div > div:nth-child(%d) > ul > li"%k)

            words = []
            # 분류들을 리스트에 저장
            [words.append(word.text) for word in section[k-1]]

            for i in range(len(words)): 
                if words[i]==find[k-1]:
                    element = driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[1]/div/div[%d]/ul/li["%k+str(i+1)+"]/a")
                    driver.execute_script("arguments[0].click();", element)
                                
            time.sleep(uniform(2.0, 4.0))
            
        driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/div/div[2]/div[1]/span/label[3]").click() # 기간 1년 선택
        time.sleep(uniform(1.5, 2.5))
        driver.find_element_by_xpath("//*[@id='18_device_0']").click() # 기기 전체 선택
        time.sleep(uniform(4.0, 6.0))
        
        driver.find_element_by_xpath("//*[@id='19_gender_0']").click() # 성별 전체 선택
        time.sleep(uniform(1.5, 2.5))
        driver.find_element_by_xpath("//*[@id='20_age_0']").click() # 연령 전체 선택
        time.sleep(uniform(3.0, 5.0))
        
        driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[1]/div/a").click() # 조회하기
        time.sleep(uniform(4.0, 6.0))

        ranking_num = 1 # 랭킹 순위
        for j in tqdm(range(10), desc="데이터랩 세부 진행상황") : # 인기 검색어 10페이지까지 크롤링
            
            popular_keywords =driver.find_elements_by_class_name("link_text") # 인기 검색어
            # time.sleep(uniform(2.0, 4.0))
        
            for word in popular_keywords:
                datalab_tmp.append(word.text[len(str(ranking_num)):]) # 앞에 필요없는 부분들(rankgin_num)을 지운 후 저장
                ranking_num += 1
            
            if j != 9 :
                driver.find_element_by_xpath("//*[@id='content']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]").click()  # 다음 페이지로 넘어가기
            time.sleep(uniform(4.0, 7.0))

    except Exception as e:
            print("오류가 발생하였습니다")

    # 앞에 필요없는 부분 제거
    [datalab_words.append(v.replace('\n','')) for v in datalab_tmp]
        
    return datalab_words