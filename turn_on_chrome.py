from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def turn_on_chrome_driver():

    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    # 대기 설정
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족

    return driver
