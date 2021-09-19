from si_message import SiMessage

"""
Sender email addresses and receiver email list file
"""
DEV_EMAIL = 'aliew9104@bths.edu'
DEV_EMAIL_LIST = 'email_lists/test_list.csv'

RIT_EMAIL = 'acl9213@g.rit.edu'
RIT_EMAIL_LIST = 'email_lists/list.csv'

"""
Ask user for message variables and create the message
@return SiMessage object
"""


def create_message():
    week = input("Enter week: ")

    letter = ''
    while letter not in ['A', 'B']:
        letter = input("Enter session letter (a/b): ").upper()

    title = input("Enter session title: ")
    description = input("Enter session description: ")

    return SiMessage(week, letter, title, description)


"""
Main method to send the message
"""


def main():
    mail = create_message()
    mail.send(RIT_EMAIL, DEV_EMAIL_LIST)


if __name__ == '__main__':
    main()
