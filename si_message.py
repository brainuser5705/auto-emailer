from __future__ import print_function
import base64
from googleapiclient import errors
import connect

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import csv
from datetime import datetime, timedelta

"""
Text templates
"""
SESSION_TEXT = open('templates/session.txt', 'r').read()
SESSION_HTML = open('templates/session.html', 'r').read()
LOCATIONS_TEXT = open('templates/locations.txt', 'r').read()
LOCATIONS_HTML = open('templates/locations.html', 'r').read()

"""
Email structure for the SI session template
"""


class SiMessage():
    """
    Sets the SI message properties
    
    @param week     the week of the session
    @param letter   the letter of the session (A/B)
    @param title    the title of the activities
    @param description      the description of the activities
    """

    def __init__(self, week, letter, title, description):
        self.message = MIMEMultipart('alternative')
        self.week = week
        self.letter = letter
        self.title = title
        self.description = description
        self.datetime = self._get_date()
        self.location = self._get_location()
        self.build()

    """
    Returns the time and location based on session letter
    """

    def _get_location(self):
        if self.letter == 'A':
            return '1:00pm - 2:00pm, NRH-1250'
        elif self.letter == 'B':
            return '11:00am - 12:00pm, LBR-3232'

    """
    Returns the session date based on next session day
    """

    def _get_date(self):
        result = ''
        day = None
        if self.letter == 'A':
            result += 'Sunday, '
            day = 0
        elif self.letter == 'B':
            result += 'Thursday, '
            day = 4

        # Gets the difference to the nearest Sunday or Thursday
        today = datetime.now()
        weekday = today.isoweekday()
        delta = day - weekday

        # For past dates, adds 7 to move date to next week
        delta += 7 if delta < 0 else 0

        date = today + timedelta(days=delta)
        result += date.strftime('%B %d, %Y')

        return result

    """
    Constructs the message with the given properties
    @returns a MIMEText object with text and html 
    """
    def build(self):

        self.message['Subject'] = 'GCIS-123 - SI SESSION ' + self.week + self.letter

        text = \
            SESSION_TEXT.format(week=self.week, letter=self.letter, title=self.title, description=self.description,
                                location=self.location, datetime=self.datetime) + \
            LOCATIONS_TEXT

        html = \
            '''
            <html lang="en">
              <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="html/style.css">
              </head>
              <body>
               ''' + \
            SESSION_HTML.format(week=self.week, letter=self.letter, title=self.title, description=self.description,
                                location=self.location, datetime=self.datetime) + \
            LOCATIONS_HTML + \
            '''
                </body>
            </html>
            '''

        self.message.attach(MIMEText(text, "plain"))
        self.message.attach(MIMEText(html, "html"))

    """
    Sends the message using the Gmail API
    """
    def api_send(self, sender, receiver):

        service = connect.get_service()

        try:
            with open(receiver) as file:
                reader = csv.reader(file)
                for first_name, last_name, receiver_email in reader:
                    self.message['bcc'] = receiver_email
                    print('Email to', receiver_email, 'successfully added to list!')

                # need to put outside of loop because self.message['bcc']
                # appends assignment to a list (not resetting as one might think)
                raw = {'raw': base64.urlsafe_b64encode(self.message.as_string().encode()).decode()}
                service.users().messages().send(userId=sender, body=raw).execute()
                print('Mass email successfully sent!')

        except errors.HttpError as error:
            print('An error occurred: %s' % error)
