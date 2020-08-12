import smtplib
from email.message import EmailMessage


def create_email_message(sender, recipient, subject, body):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body, subtype='html')
    return msg


def send_email(sender, recipient, subject, body, password):
    msg = create_email_message(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body
    )

    with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.send_message(msg)
