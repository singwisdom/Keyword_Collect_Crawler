from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import openpyxl
from autokeyword import get_auto_keyword
from blog import get_blog_keyword
from cafe import get_cafe_keyword
from shopping_key_related import get_shopping_keyword_and_relatedword
from shopping_category_title import get_category_title
from datalab import get_datalab
from turn_on_chrome import turn_on_chrome_driver
import sys
from PyQt5 import uic, QtGui

#리스트 
autokeyword_list=[]
blog_list=[]
cafe_list=[]
shopping_list=[]
title_list=[]
datalab=[]

wb = openpyxl.Workbook() #Workbook 생성
sheet = wb.active #Sheet 활성
wb.title="합본" #sheet 이름 설정
sheet.append(["결과"]) #데이터 프레임 내 변수명 생성

# Ui 파일을 불러옴
form_class = uic.loadUiType("UI.ui")[0]

class MyWindow(QMainWindow, form_class):
    
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        self.ok.clicked.connect(self.btnClick)

    def btnClick(self):

        # 에디트 박스에서 키워드를 받아옴
        keyword=self.edit.toPlainText()
        driver = turn_on_chrome_driver() # 크롬 드라이버 옵션 설정

        #각 모듈의 함수 호출
        autokeyword_list=get_auto_keyword(keyword, driver)
        [sheet.append([i]) for i in autokeyword_list]
        print(len(autokeyword_list))

        blog_list=get_blog_keyword(keyword, driver)
        [sheet.append([i]) for i in blog_list]
        print(len(blog_list))

        cafe_list=get_cafe_keyword(keyword, driver)
        [sheet.append([i]) for i in cafe_list]
        print(len(cafe_list))
        
        shopping_list=get_shopping_keyword_and_relatedword(keyword, driver)
        [sheet.append([i]) for i in shopping_list]
        print(len(shopping_list))

        title_list=get_category_title(keyword, driver)
        [sheet.append([i]) for i in title_list]
        print(len(title_list))

        datalab=get_datalab(driver)
        [sheet.append([i]) for i in datalab]
        print(len(datalab))

        driver.quit() # 종료

        # 엑셀 파일로 저장
        wb.save("키워드 수집.xlsx")
        print("모든 작업이 완료되었습니다.")
        
        self.info.setText("키워드 수집 완료")
        self.info.setFont(QtGui.QFont("나눔스퀘어OTF Bold",18)) #폰트,크기 조절 
        self.info.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.info.setStyleSheet("Color : green") # 글자색 변환
            
if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    sys.exit(app.exec_())







