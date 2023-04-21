import os
import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


class Gmail:

    GMAIL_SMTP = 'smtp.gmail.com'
    GMAIL_IMAP = 'imap.gmail.com'

    def __init__(self):
        load_dotenv()
        self.login = os.getenv('GMAIL_LOGIN')
        self.password = os.getenv('GMAIL_PASSWORD')
        self.header = None

    def send_message(self, msg_to: list, msg_subj: str, msg_text: str):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(msg_to)
        msg['Subject'] = msg_subj
        msg.attach(MIMEText(msg_text))

        server = smtplib.SMTP(self.GMAIL_SMTP, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(msg['From'], self.password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    def recieve_message(self):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select('inbox')
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    gmail = Gmail()
    gmail.send_message(['vasya@email.com', 'petya@email.com'], 'Subject', 'Message')
    message = gmail.recieve_message()
