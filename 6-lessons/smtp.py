import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_host = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'nurlanuuulubeksultan@gmail.com'
sender_password = 'qhmvswrwclbusvod'

receiver_email = 'isxaakjz@gmail.com'
subject = 'Это Тестовое сообщение'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

body = 'Это Тестовое сообщение от 3 месяца'
message.attach(MIMEText(body, 'plain'))

while True:
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Успешно отправлена")
    except Exception as e:
        print("Ошибка", e)
    finally:
        server.quit()