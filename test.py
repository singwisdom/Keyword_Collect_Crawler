import smtplib
from email.mime.text import MIMEText

session = smtplib.SMTP('smtp.worksmobile.com', 587) # 이메일을 보내기 위한 SMTP 세션
session.starttls() # SMTP 연결을 TLS 모드로 설정
session.login('intern@martroo.com', 'akxmfn0617%') # 순서대로 네이버 웍스 계정 아이디,비밀번호 

msg = MIMEText('키워드 수집 중 오류가 발생했습니다. 해당 키워드부터 다시 실행해주세요')
msg['Subject'] = '키워드 수집 오류' # 메일 보내기
session.sendmail('intern@martroo.com', 'epqlfdusrma@daum.net' , msg.as_string())
session.quit() # 세션 종료