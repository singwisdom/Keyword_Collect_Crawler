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

wb = openpyxl.Workbook() # Workbook 생성
sheet = wb.active # Sheet 활성
wb.title="합본" # sheet 이름 설정

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("키워드 분석 프로그램")
        Dialog.resize(414, 246)
        Dialog.setStyleSheet("")
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(170, 180, 81, 31))
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.ok.setFont(font)
        self.ok.setStyleSheet("font: 75 12pt \"나눔스퀘어 Bold\";")
        self.ok.setObjectName("ok")
        self.edit = QtWidgets.QTextEdit(Dialog)
        self.edit.setGeometry(QtCore.QRect(50, 110, 311, 51))
        self.edit.setObjectName("edit")
        self.info = QtWidgets.QLabel(Dialog)
        self.info.setGeometry(QtCore.QRect(110, 50, 211, 31))
        self.info.setStyleSheet("font: 75 18pt \"나눔스퀘어OTF Bold\";")
        self.info.setScaledContents(False)
        self.info.setIndent(-1)
        self.info.setObjectName("info")
        self.ok.clicked.connect(self.btnClick)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def btnClick(self):
        keyword=self.edit.toPlainText() # 에디트 박스에서 키워드를 받아옴
        driver = turn_on_chrome_driver() # 크롬 드라이버 옵션 설정
        print("\n>>>>>>> 키워드 분석을 시작합니다. <<<<<<<\n")

        # 각 모듈의 함수 호출
        [sheet.append([i]) for i in tqdm(get_auto_keyword(keyword, driver), desc="자동완성어")]
        print(">> 네이버 자동완성어 수집 완료\n\n")
        [sheet.append([i]) for i in tqdm(get_blog_keyword(keyword, driver), desc="블로그")]
        print(">> 블로그 연관검색어 수집 완료\n\n")   
        [sheet.append([i]) for i in tqdm(get_cafe_keyword(keyword, driver), desc="카페")]
        print(">> 카페 연관검색어 수집 완료\n\n")
        [sheet.append([i]) for i in tqdm(get_shopping_keyword_and_relatedword(keyword, driver), desc="네이버 쇼핑 검색어")]
        print(">> 네이버 쇼핑사이트 키워드추천, 연관검색어 수집 완료\n\n")
        [sheet.append([i]) for i in get_category_title(keyword, driver)]
        print(">> 네이버 쇼핑 사이트 카테고리, 타이틀 수집 완료\n\n")
        [sheet.append([i]) for i in tqdm(get_datalab(driver), desc="네이버 데이터랩")]
        print(">> 데이터랩 인기검색어 수집 완료\n")

        driver.quit() # 종료

        wb.save("키워드 수집.xlsx") # 엑셀 파일로 저장
        print("◆ 모든 작업이 완료되었습니다. ◆")
        self.info.setText("키워드 수집 완료")
        self.info.setFont(QtGui.QFont("나눔스퀘어OTF Bold", 18)) # 폰트,크기 조절 
        self.info.setAlignment(Qt.AlignCenter) # 가운데 정렬
        self.info.setStyleSheet("Color : green") # 글자색 변환

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "키워드 수집 프로그램"))
        self.ok.setText(_translate("Dialog", "확인"))
        self.info.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt;\">검색어를 입력하세요!</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
