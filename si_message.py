from __future__ import print_function

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime, timedelta

from message import Message
from reminder_email import ReminderEmail

"""
Text templates
"""
SESSION_TEXT = open('templates/session.txt', 'r').read()
SESSION_HTML = open('templates/session.html', 'r').read()
LOCATIONS_TEXT = open('templates/locations.txt', 'r').read()
LOCATIONS_HTML = open('templates/locations.html', 'r').read()


class SiMessage(Message):
    """
    Email structure for the SI session template
    """

    def __init__(self, week, letter, title, description, sender, receiver):
        """
        Sets the SI message properties

        @param week     the week of the session
        @param letter   the letter of the session (A/B)
        @param title    the title of the activities
        @param description      the description of the activities
        """
        super().__init__(sender, receiver)
        self.week = week
        self.letter = letter
        self.title = title
        self.description = description
        self.datetime = self._get_date()
        self.location = self._get_location()

        self.build()

    def _get_location(self):
        """
        Returns the time and location based on session letter
        """
        if self.letter == 'A':
            return '1:00pm - 2:00pm, NRH-1250'
        elif self.letter == 'B':
            return '11:00am - 12:00pm, LBR-3232'

    def _get_date(self):
        """
        Returns the session date based on next session day
        """
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

        return date

    def build(self):
        """
        Constructs the message with the given properties
        @returns a MIMEText object with text and html
        """

        self.message['Subject'] = 'GCIS-123 - SI SESSION ' + self.week + self.letter

        date = self.datetime.strftime('%B %d, %Y')

        text = \
            SESSION_TEXT.format(week=self.week, letter=self.letter, title=self.title, description=self.description,
                                location=self.location, datetime=date) + \
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
                                location=self.location, datetime=date) + \
            LOCATIONS_HTML + \
            '''
                </body>
            </html>
            '''

        self.message.attach(MIMEText(text, "plain"))
        self.message.attach(MIMEText(html, "html"))

    def send(self):
        """
        Send message and start reminder email thread
        :param sender:
        :param receiver:
        """
        super().send()
        reminder_email = ReminderEmail(self)
        reminder_email.start_thread()


