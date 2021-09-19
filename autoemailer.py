from colorama import init
from termcolor import colored, cprint
from si_message import SiMessage

# used this library function for initial input values
from pyautogui import typewrite

"""
Sender email addresses and receiver email list file
"""
RIT_EMAIL = 'acl9213@g.rit.edu'
DEV_EMAIL_LIST = 'email_lists/test_list.csv'
RIT_EMAIL_LIST = 'email_lists/list.csv'

# The colorama docs say "init() will filter ANSI escape
# sequences out of any text sent to stdout or stderr,
# and replace them with equivalent Win32 calls."
init()

# Every input will be prefixed with a question mark
QMARK = colored("?", 'yellow')

"""
Ask for user input
@param query_str    the input query string
@param init_value   initial input value, default is blank
"""


def get_input(query_str, init_value=''):
    print(QMARK, end=' ')
    cprint(query_str, 'cyan', end='')
    typewrite(init_value)
    return input()


"""
Display the message content
"""


def print_message(message: SiMessage):
    print('\n======= Email Contents =======')
    print('SI Session ' + message.week + message.letter + ' - ' + message.title)
    print(message.datetime.strftime('%B %d, %Y') + '\n' + message.location)
    print(message.description)
    print('==============================\n')


"""
Main function that runs the CLI
"""


def main():
    # get the initial values

    week = ''
    while not week.isdigit():
        week = get_input('Week: ')

    letter = ''
    while letter not in ['A', 'B']:
        letter = get_input('Letter (a/b): ').upper()

    title = get_input('Title: ')
    description = get_input('Description: ')

    # change values if needed

    message = None
    need_change = 1  # uses the trick that True is any non-zero value
    while need_change:

        message = SiMessage(week, letter, title, description, RIT_EMAIL, DEV_EMAIL_LIST)
        print_message(message)

        cprint("Do you need to change anything?\n"
               "\t(1) Week\n"
               "\t(2) Letter\n"
               "\t(3) Title\n"
               "\t(4) Description\n"
               "\t____OR____    \n"
               "\t(0) Nothing\n",
               'red')
        need_change = int(get_input('Answer: '))

        if need_change:
            if need_change == 1:
                week = get_input("New week: ")
            elif need_change == 2:
                letter = get_input("New letter: ").upper()
            elif need_change == 3:
                title = get_input("New title: ", title)
            elif need_change == 4:
                description = get_input("New description: ", description)

    # final confirmation

    print('\n')
    if get_input("Are you sure this is good to send? (y/n) ") == 'y':
        print('\n====== Sending Emails ======')
        message.send()
        print('==============================\n')
    else:
        cprint("\nAUTO-EMAILER TERMINATED\n(NO EMAILS SENT)", 'red')


if __name__ == '__main__':
    cprint(
        "\n WELCOME TO AUTO-EMAILER \n"
        "=========================\n")
    main()
