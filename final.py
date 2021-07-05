import openpyxl
from autokeyword import GetAutokeyword
from blog import GetBlog_keyword
from cafe import GetCafe_keyword
from shopping_key_related import GetShopping_keyword_and_relatedword
from shopping_title import GetShopping_title
from datalab import GetDatalab

#리스트 
autokeyword_list=[]
blog_list=[]
cafe_list=[]
keyword_list=[]
related_list=[]
title_lst=[]
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

#검색어를 입력
print("검색어를 입력해주세요:")
keyword=input()

# 각 모듈의 함수 호출
autokeyword_list=GetAutokeyword(keyword)
blog_list=GetBlog_keyword(keyword)
cafe_list=GetCafe_keyword(keyword)
shopping_list=GetShopping_keyword_and_relatedword(keyword)
title_list=GetShopping_title(keyword)
datalab=GetDatalab(keyword)

# 출력(테스트)
print(autokeyword_list)
print(blog_list)
print(cafe_list)
print(shopping_list)
print(title_list)
print(datalab)

# 리스트들을 하나로 
final_list=autokeyword_list+blog_list+cafe_list+keyword_list+related_list+title_list+datalab

#엑셀에 저장
[sheet.append([i]) for i in final_list]

print("\n\n")
print(final_list)

# 엑셀 파일로 저장
wb.save("검색어합본.xlsx")



