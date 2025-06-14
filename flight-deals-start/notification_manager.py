import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    # def __init__(self):
    def send_emails(self, email_list, email_body):
        with smtplib.SMTP(os.environ["SMTP_ADDRESS"],port=587) as connection:
            connection.starttls()
            connection.login(os.environ["Email"], os.environ["Password"])
            for email in email_list:
                connection.sendmail(
                    from_addr=os.environ["Email"],
                    to_addrs=os.environ["Email"],
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )


