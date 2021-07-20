from email.mime.text import MIMEText
import smtplib

def send_success_mail(receiver, keyword:str):
    works_user = 'intern@martroo.com'
    works_pwd = 'akxmfn0617%'
    TEXT = "%s 키워드 수집이 완료 되었습니다!" %keyword # 메일 내용!!

    message = MIMEText(TEXT, _charset='euc-kr') # 메일 내용
    message['Subject']='알림) 키워드 수집 완료 ' # 메일 제목
    message['From']=works_user # 보내는 사람 메일 주소

    if receiver == '':
        receiver = 'intern@martroo.com' # 이메일 입력칸에 아무것도 입력하지 않았을 때 지정되는 기본 메일주소
        message['To']=receiver
    else :
        message['To']=receiver # 받는 사람 메일 주소

    works_sever = smtplib.SMTP_SSL('smtp.worksmobile.com', 465)
    works_sever.login(works_user, works_pwd)
    works_sever.sendmail(works_user, receiver, message.as_string())
    works_sever.quit()


def send_fail_mail(receiver, keyword:str):
    works_user = 'intern@martroo.com'
    works_pwd = 'akxmfn0617%'
    TEXT = "'%s' 키워드 수집 중 오류가 발생했습니다. 해당 키워드부터 다시 실행해주세요 " %keyword # 메일 내용!!

    message = MIMEText(TEXT, _charset='euc-kr') # 메일 내용
    message['Subject']='알림) 키워드 수집 실패' # 메일 제목
    message['From']=works_user # 보내는 사람 메일 주소

    if receiver == '':
        receiver = 'intern@martroo.com' # 이메일 입력칸에 아무것도 입력하지 않았을 때 지정되는 기본 메일주소
        message['To']=receiver
    else :
        message['To']=receiver # 받는 사람 메일 주소

    works_sever = smtplib.SMTP_SSL('smtp.worksmobile.com', 465)
    works_sever.login(works_user, works_pwd)
    works_sever.sendmail(works_user, receiver, message.as_string())
    works_sever.quit()
