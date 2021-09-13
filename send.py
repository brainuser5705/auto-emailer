from getpass import getpass as gp
from message import Message

DEV_EMAIL = 'aliew9104@bths.edu'
RIT_EMAIL = 'acl9213@g.rit.edu'

DEV_EMAIL_LIST = 'test_list.csv'


def create_test_message():
    week = "4"
    letter = "A"
    title = "Errors and Debugging"
    description = "Test your error spotting and debugging skills"

    return Message(week, letter, title, description)


def create_message():
    week = input("Enter week: ")

    letter = ''
    while letter not in ['A', 'B']:
        letter = input("Enter session letter (a/b): ").upper()

    title = input("Enter session title: ")
    description = input("Enter session description: ")

    return Message(week, letter, title, description)


def smtp(message, sender, receiver):
    password = gp()
    message.build()
    message.smtp_send(sender, password, receiver)


def api(message, sender, receiver):
    message.build()  # probably put this in the class??
    message.api_send(sender, receiver)

def main():
    mail = create_message()
    api(mail, RIT_EMAIL, DEV_EMAIL_LIST)


if __name__ == '__main__':
    main()
