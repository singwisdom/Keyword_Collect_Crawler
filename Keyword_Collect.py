from PyQt5.QtWidgets import QApplication, QMainWindow
import openpyxl
from autokeyword import GetAutokeyword
from blog import GetBlog_keyword
from cafe import GetCafe_keyword
from shopping_key_related import GetShopping_keyword_and_relatedword
from shopping_category_title import getCategory_Title
from datalab import GetDatalab
import sys
from PyQt5.QtQuickWidgets import *
from PyQt5 import uic


#리스트 
autokeyword_list=[]
blog_list=[]
cafe_list=[]
shopping_list=[]
title_list=[]
final_list=[]
datalab=[]

#Workbook 생성
wb = openpyxl.Workbook()

#Sheet 활성
sheet = wb.active

#sheet 이름 설정
wb.title="합본"

#데이터 프레임 내 변수명 생성
sheet.append(["결과"])


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

        # 각 모듈의 함수 호출
        autokeyword_list=GetAutokeyword(keyword)
        blog_list=GetBlog_keyword(keyword)
        cafe_list=GetCafe_keyword(keyword)
        shopping_list=GetShopping_keyword_and_relatedword(keyword)
        title_list=getCategory_Title(keyword)
        datalab=GetDatalab(keyword)
        
        # 리스트들을 하나로 
        final_list=autokeyword_list+blog_list+cafe_list+shopping_list+title_list+datalab
        
        #엑셀에 저장
        [sheet.append([i]) for i in final_list]

        # 엑셀 파일로 저장
        wb.save("검색어합본.xlsx")
            


if __name__=="__main__":
    app=QApplication(sys.argv)
    myWindow=MyWindow()
    myWindow.show()
    sys.exit(app.exec_())







