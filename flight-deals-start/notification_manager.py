import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:
    """This class is responsible for sending email notifications with flight deal details."""
    
    def send_emails(self, email_list, email_body):
        """Send email notifications to all users in the email list."""
        with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
            connection.starttls()
            connection.login(os.environ["EMAIL"], os.environ["PASSWORD"])
            for email in email_list:
                connection.sendmail(
                    from_addr=os.environ["EMAIL"],
                    to_addrs=email,  # Fixed: was sending to self instead of recipient
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )
