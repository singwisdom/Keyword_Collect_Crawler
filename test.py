import smtplib
from email.mime.text import MIMEText

session = smtplib.SMTP('smtp.gmail.com', 587) # 이메일을 보내기 위한 SMTP 세션
session.starttls() # SMTP 연결을 TLS 모드로 설정
session.login('0903jihyie@gmail.com', 'wpbfsxzhztuwpwrb') # 순서대로 지메일 계정, 앱 비밀번호 (여기서 앱 비밀먼호는 단순 계정 비밀번호가 아님. IMAP 설정 참고)

msg = MIMEText('내용 : %s 모든 키워드 수집이 완료되었습니다.')
msg['Subject'] = '제목 : 키워드 수집 완료 알림' # 메일 보내기
session.sendmail("0903jihyie@gmail.com" , "epqlfdusrma@daum.net" , msg.as_string())
session.quit() # 세션 종료