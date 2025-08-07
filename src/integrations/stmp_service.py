
import smtplib
from email.mime.text import MIMEText
from src.core import global_settings, logger

class EmailService:
    def __init__(self):
        self.stmp_host = global_settings.mail_host
        self.stmp_port = global_settings.mail_port
        self.stmp_user = global_settings.mail_user
        self.stmp_password = global_settings.mail_pass

    def send_email(self, to_email: str, subject: str, body: str):
        """Send an email using SMTP."""
       

        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.stmp_user
            msg['To'] = to_email

            with smtplib.SMTP(self.stmp_host, self.stmp_port) as server:
                server.starttls()
                server.login(self.stmp_user, self.stmp_password)
                server.sendmail(self.stmp_user, to_email, msg.as_string())
                logger.info(f"Email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise e