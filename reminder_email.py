from datetime import datetime, timedelta
from email.mime.text import MIMEText

from threading import Timer
from message import Message

REMINDER_TEXT = open('templates/reminder.txt', 'r').read()
REMINDER_HTML = open('templates/reminder.html', 'r').read()


class ReminderEmail(Message):
    thread_pool = []

    def __init__(self, si_message):
        super().__init__(si_message.sender, si_message.receiver)
        self.si_message = si_message
        self.build()

    def _calculate_seconds(self):
        num_seconds = 0

        si_date = self.si_message.datetime
        date = datetime(si_date.year, si_date.month, si_date.day)  # hours and seconds will be set to midnight

        # times in seconds from now to date
        num_seconds += (datetime.now() - date).total_seconds()

        # add seconds based on time
        if self.si_message.letter == 'A':
            # starting at 1:00pm, send reminder at 12:30pm
            num_seconds += timedelta(hours=12.5).total_seconds()
        elif self.si_message.letter == 'B':
            # starting at 11:00am, send reminder at 10:30am
            num_seconds += timedelta(hours=10.5).total_seconds()

        return num_seconds

    def build(self):
        self.message['Subject'] = 'GCIS-123 - SI SESSION IN 30 MINUTES!'

        text = REMINDER_TEXT.format(
            title=self.si_message.title,
            datetime=self.si_message.datetime.strftime('%B %d, %Y'),
            location=self.si_message.location,
            description=self.si_message.description
        )

        html = REMINDER_HTML.format(
            title=self.si_message.title,
            datetime=self.si_message.datetime.strftime('%B %d, %Y'),
            location=self.si_message.location,
            description=self.si_message.description
        )

        self.message.attach(MIMEText(text, "plain"))
        self.message.attach(MIMEText(html, "html"))

    def start_thread(self):
        time = self._calculate_seconds()
        thread = Timer(30, self.send)
        #thread.setDaemon(True)  # set as background task
        thread.start()
        print('Reminder email is set!')
        self.thread_pool.append(thread)

        return True

    def cancel(self, index):
        self.thread_pool[index].cancel()
