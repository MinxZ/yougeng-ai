import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

def send_order(img_url, size, address, user_name, phone_number):
    subject = "订单信息"
    # img_url = 'http://lc-b8lJaEKY.cn-n1.lcfile.com/DEDs1lLhaEm8jxPz9TxLADYA5ULPstTA/openai2.jpg'
    # size = 'L号'
    # address = '大理市隐仙路与Z005交叉口东200米'
    body = f"以下是我的订单信息：  \n \
            图片网址：{img_url} \n \
            大小：{size} \n \
            地址：{address} \n  \
            收件人： {user_name} \n \
            电话：{phone_number} \n \
            请尽快发货，谢谢！"

    sender = "z08040992048@gmail.com"
    recipients = ["minxz162@gmail.com", "1176378062@qq.com"]
    password = "dvnllvvdruzrtmcj"
    send_email(subject, body, sender, recipients, password)