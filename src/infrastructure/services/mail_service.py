import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from src.config import global_settings

class MailService(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        pass

class SMTPEmailService(MailService):
    def __init__(self):
        self.smtp_host = global_settings.MAIL_HOST
        self.smtp_port = global_settings.MAIL_PORT
        self.username = global_settings.MAIL_USER
        self.password = global_settings.MAIL_PASS

    def send_email(self, to: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = "Paytracker Teams <noreply@paytracker.com>"
            msg['To'] = to
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, [to], msg.as_string())
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False