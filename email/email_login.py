import sys
sys.path.insert(0, '.')

import os
import smtplib, ssl
from email.mime.text import MIMEText
from dotenv import load_dotenv
from database.db_manager import DBConnect
from database.data_models import Jobs
from sqlalchemy.orm import sessionmaker

class SendEmail:
      def __init__(self) -> None:
            load_dotenv()
            self.email = os.environ.get('emailId')
            self.onepass = os.environ.get('onePasswordEmail')
            self.port = 465  # For SSL

            # Create a secure SSL context
            self.context = ssl.create_default_context()

      def send_email(self, message: str):
            sender_email = self.email
            receiver_email = self.email
            with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
                  server.login(self.email, self.onepass)
                  server.sendmail(sender_email, receiver_email, message)
            print('email sent')


class NotifyNewJobs:
      def __init__(self):
            self.db = DBConnect()
            self.send_email_class = SendEmail()
            self.scraped_jobs_data = self.db.sql_fetchall_records(Jobs)
            self.to_notify_data = [i for i in self.scraped_jobs_data if i['notified']==False]

      def notify_new_jobs(self):
            if not self.to_notify_data:
                  return

            SUBJECT = 'Your job postings!!!'
            content = f"Hi,\n\nBelow are new job postings found.\n"

            for count, i in enumerate(self.to_notify_data):
                  print(i, type(i))
                  self.db.update_records(Jobs, 'notified', True, condition_col="job_link", condition_col_val=i["job_link"])
                  content+=f"\n{count+1}. Job title: {i.get('job_title')} and Job link: {i.get('job_link')}"

            message = 'Subject: {}\n\n{}'.format(SUBJECT, content)

            SendEmail().send_email(message)
            

NotifyNewJobs().notify_new_jobs()