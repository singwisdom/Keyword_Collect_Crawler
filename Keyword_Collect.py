from time import time
from PyQt5 import QtCore, QtGui, QtWidgets
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
from tqdm import tqdm
from send_email import send_success_mail, send_fail_mail


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(522, 471)
        font = QtGui.QFont()
        font.setUnderline(False)
        Dialog.setFont(font)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("")
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(210, 400, 81, 41))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.ok.setFont(font)
        self.ok.setStyleSheet("font: 75 12pt \"나눔스퀘어 Bold\";\n")
        self.ok.setObjectName("ok")
        self.find = QtWidgets.QTextEdit(Dialog)
        self.find.setGeometry(QtCore.QRect(70, 80, 381, 231))
        self.find.setObjectName("find")
        self.find_info = QtWidgets.QLabel(Dialog)
        self.find_info.setGeometry(QtCore.QRect(160, 30, 231, 31))
        self.find_info.setStyleSheet("font: 75 18pt \"나눔스퀘어OTF Bold\";")
        self.find_info.setScaledContents(False)
        self.find_info.setIndent(-1)
        self.find_info.setObjectName("find_info")
        self.email_info = QtWidgets.QLabel(Dialog)
        self.email_info.setGeometry(QtCore.QRect(60, 340, 81, 31))
        self.email_info.setStyleSheet("font: 75 18pt \"나눔스퀘어OTF Bold\";")
        self.email_info.setScaledContents(False)
        self.email_info.setIndent(-1)
        self.email_info.setObjectName("email_info")
        self.email = QtWidgets.QTextEdit(Dialog)
        self.email.setGeometry(QtCore.QRect(150, 330, 301, 41))
        self.email.setObjectName("email")

        self.ok.clicked.connect(self.btnClick) # 확인 버튼 이벤트 등록

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def btnClick(self):
     
        input_keyword=self.find.toPlainText() # 에디트 박스에서 키워드를 받아옴
        receiver = self.email.toPlainText() # 에디트 박스에서 이메일 주소를 받아옴
        keyword = input_keyword.split('\n') # 엔터로 키워드를 구분해서 리스트에 입력
    
        for count in range(0,len(keyword)):

            check_success=True
            wb = openpyxl.Workbook() # Workbook 생성
            sheet = wb.active # Sheet 활성

            driver = turn_on_chrome_driver() # 크롬 드라이버 옵션 설정
            print("\n\n>>>>>>> '%s' 키워드 분석을 시작합니다. <<<<<<<\n" %keyword[count])

            try :
                #각 모듈의 함수 호출
                [sheet.append([i]) for i in tqdm(get_auto_keyword(keyword[count], driver), desc="자동완성어")]
                print(">> 네이버 자동완성어 수집 완료\n")
                [sheet.append([i]) for i in tqdm(get_blog_keyword(keyword[count], driver), desc="블로그")]
                print(">> 블로그 연관검색어 수집 완료\n")   
                [sheet.append([i]) for i in tqdm(get_cafe_keyword(keyword[count], driver), desc="카페")]
                print(">> 카페 연관검색어 수집 완료\n")
                [sheet.append([i]) for i in tqdm(get_shopping_keyword_and_relatedword(keyword[count], driver), desc="네이버 쇼핑 검색어")]
                print(">> 네이버 쇼핑사이트 키워드추천, 연관검색어 수집 완료\n")

                category_title=[] # 카테고리와 타이틀을 반환받을 리스트
                category_title= get_category_title(keyword[count], driver) # 카테고리와 타이틀을 저장

                [sheet.append([i]) for i in tqdm(category_title[0], desc="네이버 쇼핑 검색어")] # 타이틀을 엑셀에 저장
                print(">> 네이버 쇼핑 사이트 카테고리, 타이틀 수집 완료\n")
                
                for k in tqdm(range(1,len(category_title[1])+1), desc="네이버 데이터랩"):
                    [sheet.append([i]) for i in get_datalab(category_title[1][k-1], driver)]

                    if k%5==0:
                        driver.quit() # 종료
                        driver = turn_on_chrome_driver() # 새 드라이버를 받음
                       
                print(">> 데이터랩 인기검색어 수집 완료\n")
                driver.quit() # 종료

            except Exception as e: # 에러가 생길 경우
                send_fail_mail(receiver, keyword[count]) # 실패 메일 전송
                check_success =  False
                print("'%s' 키워드 수집에 실패하였습니다." %keyword[count])
                self.find_info.setText("키워드 수집 실패")
                self.find_info.setFont(QtGui.QFont("나눔스퀘어OTF Bold", 18)) # 폰트, 크기 조절 
                self.find_info.setAlignment(Qt.AlignCenter) # 가운데 정렬
                self.find_info.setStyleSheet("Color : red") # 글자색 변환

            if check_success == True :
                print("'%s' 키워드 수집이 완료되었습니다." %keyword[count])

            wb.save("[%s] 키워드 수집.xlsx" %keyword[count]) # 엑셀 파일로 저장
            wb.close()

            if count%5==0: # 데이터랩에서 과부하 걸리지 않기 위해 5번마다 쉬어줌
                time.sleep(30)

        if check_success==True :
            print("◆ 모든 작업이 완료되었습니다. ◆")
            send_success_mail(receiver, keyword) # 성공 메일 전송
            self.find_info.setText("키워드 수집 완료")
            self.find_info.setFont(QtGui.QFont("나눔스퀘어OTF Bold", 18)) # 폰트, 크기 조절 
            self.find_info.setAlignment(Qt.AlignCenter) # 가운데 정렬
            self.find_info.setStyleSheet("Color : green") # 글자색 변환
            

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "키워드 수집 프로그램"))
        self.ok.setText(_translate("Dialog", "확인"))
        self.find_info.setText(_translate("Dialog", "<html><head/><body><p>검색어를 입력하세요!</p></body></html>"))
        self.email_info.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">이메일</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
