from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from proxy import proxy_create
import chromedriver_autoinstaller
from selenium.webdriver.remote.remote_connection import LOGGER, logging

def turn_on_chrome_driver():

    check_chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬버전 확인

    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        driver = webdriver.Chrome(f'./{check_chrome_ver}/chromedriver.exe', chrome_options=options)
    except Exception as e:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{check_chrome_ver}/chromedriver.exe', chrome_options=options)

    # 대기 설정
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족
    
    return driver


def turn_on_chrome_proxy_driver():

    check_chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬버전 확인

    proxy = proxy_create()
    PROXY = proxy

    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }
    LOGGER.setLevel(logging.WARNING)

    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        driver = webdriver.Chrome(f'./{check_chrome_ver}/chromedriver.exe', chrome_options=options)
    except Exception as e:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{check_chrome_ver}/chromedriver.exe', chrome_options=options)

    # 대기 설정
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족
    
    return driver
