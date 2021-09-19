import base64
from email.mime.multipart import MIMEMultipart

from googleapiclient import errors
import connect
import csv


class Message:

    def __init__(self, sender, receiver):
        self.message = MIMEMultipart('alternative')
        self.sender = sender
        self.receiver = receiver

    def send(self):
        """
        Sends the message using the Gmail API
        """
        service = connect.get_service()

        try:
            with open(self.receiver) as file:
                reader = csv.reader(file)
                for first_name, last_name, receiver_email in reader:
                    self.message['to'] = receiver_email
                    print('Email to', receiver_email, 'successfully added to list!')

                # need to put outside of loop because self.message['bcc']
                # appends assignment to a list (not resetting as one might think)
                raw = {'raw': base64.urlsafe_b64encode(self.message.as_string().encode()).decode()}
                service.users().messages().send(userId=self.sender, body=raw).execute()
                print('Mass email successfully sent!')

        except errors.HttpError as error:
            print('An error occurred: %s' % error)
