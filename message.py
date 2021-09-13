from __future__ import print_function

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv

import base64
from googleapiclient import errors

import connect

import text as t
from datetime import datetime, timedelta

PORT = 465
SMTP_SERVER = 'smtp.gmail.com'


class Message:
    context = ssl.create_default_context()

    def __init__(self, week, letter, title, description):
        self.message = MIMEMultipart('alternative')
        self.week = week
        self.letter = letter
        self.title = title
        self.description = description
        self.datetime = self._get_date()
        self.location = self._get_location()

    def _get_location(self):
        if self.letter == 'A':
            return '1:00pm - 2:00pm, NRH-1250'
        elif self.letter == 'B':
            return '11:00am - 12:00pm, LBR-3232'

    def _get_date(self):
        result = ''
        day = None
        if self.letter == 'A':
            result += 'Sunday, '
            day = 0
        elif self.letter == 'B':
            result += 'Thursday, '
            day = 4

        # get the nearest date of day
        today = datetime.now()
        weekday = today.isoweekday()
        delta = day - weekday
        delta += 7 if delta < 0 else 0  # referring to next week
        date = today + timedelta(days=delta)

        result += date.strftime('%B %d, %Y')

        return result

    def build(self):

        self.message['Subject'] = 'GCIS-123 - SI SESSION ' + self.week + self.letter

        text = \
            t.session_text.format(week=self.week, letter=self.letter, title=self.title, description=self.description,
                                  location=self.location, datetime=self.datetime) + \
            t.locations_text

        html = \
            '''
            <html lang="en">
              <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="html/style.css">
              </head>
              <body>
               ''' + \
            t.session_html.format(week=self.week, letter=self.letter, title=self.title, description=self.description,
                                  location=self.location, datetime=self.datetime) + \
            t.locations_html + \
            '''
                </body>
            </html>
            '''

        self.message.attach(MIMEText(text, "plain"))
        self.message.attach(MIMEText(html, "html"))

    def smtp_send(self, email, password, receiver):
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=self.context) as server:
            server.login(email, password)

            with open(receiver) as file:
                reader = csv.reader(file)
                for receiver_email in reader:
                    server.sendmail(
                        email,
                        receiver_email,
                        self.message.as_string()
                    )

                    print('Email to', receiver_email, 'successfully sent!')

    def api_send(self, sender, receiver):

        service = connect.get_service()

        try:
            with open(receiver) as file:
                reader = csv.reader(file)
                for first_name, last_name, receiver_email in reader:
                    self.message['bcc'] = receiver_email  # because receiver_email is seen as a list
                    print('Email to', receiver_email, 'successfully added to list!')

                # need to put outside of loop because self.message['bcc']
                # appends assignment to a list (not resetting as one might think)
                raw = {'raw': base64.urlsafe_b64encode(self.message.as_string().encode()).decode()}
                service.users().messages().send(userId=sender, body=raw).execute()
                print('Mass email successfully sent!')

        except errors.HttpError as error:
            print('An error occurred: %s' % error)
