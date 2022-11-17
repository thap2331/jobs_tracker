import os
import smtplib, ssl
from dotenv import load_dotenv

class SendEmail:
      def __init__(self) -> None:
            load_dotenv()
            self.email = os.environ.get('emailId')
            self.password = os.environ.get('emailPass')
            self.onepass = os.environ.get('onePasswordEmail')
            self.port = 465  # For SSL

            # Create a secure SSL context
            self.context = ssl.create_default_context()

      def send_email(self, message):
            sender_email = self.email
            receiver_email = self.email
            with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
                  server.login(self.email, self.onepass)
                  server.sendmail(sender_email, receiver_email, message)

message = """
                        Subject: Hi there
                        This message is sent from Python."""
SendEmail().send_email(message)

#https://realpython.com/python-send-email/
#https://stackoverflow.com/questions/73026671/how-do-i-now-since-june-2022-send-an-email-via-gmail-using-a-python-script
#https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j
