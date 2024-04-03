import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    sender_email = 'ticketshow.somya@gmail.com'
    sender_password = 'tztvvpyydsvvuxdg'

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False