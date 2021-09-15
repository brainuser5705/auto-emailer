from colorama import init
from termcolor import colored, cprint
from si_message import SiMessage
from pyautogui import typewrite

RIT_EMAIL = 'acl9213@g.rit.edu'
DEV_EMAIL_LIST = 'email_lists/test_list.csv'
RIT_EMAIL_LIST = 'email_lists/list.csv'

init()

QUERY_STARTER = colored("?", 'yellow')


def get_input(query_str, init_value=''):
    print(QUERY_STARTER, end=' ')
    cprint(query_str, 'cyan', end='')
    typewrite(init_value)
    return input()


def print_message(message: SiMessage):
    print('\n======= Email Contents =======')
    print('SI Session ' + message.week + message.letter + ' - ' + message.title)
    print(message.datetime + '\n' + message.location)
    print(message.description)
    print('==============================\n')


def main():
    cprint(
        "\n WELCOME TO AUTO-EMAILER \n"
        "=========================\n")

    week = ''
    while not week.isdigit():
        week = get_input('Week: ')

    letter = ''
    while letter not in ['A', 'B']:
        letter = get_input('Letter (a/b): ').upper()

    title = get_input('Title: ')
    description = get_input('Description: ')

    message = None
    need_change = 1
    while need_change:

        message = SiMessage(week, letter, title, description)
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
                letter = get_input("New letter: ")
            elif need_change == 3:
                title = get_input("New title: ", title)
            elif need_change == 4:
                description = get_input("New description: ", description)

    print('\n')
    if get_input("Are you sure this is good to send? (y) ") == 'y':
        print('\n====== Sending Emails ======')
        message.api_send(RIT_EMAIL, DEV_EMAIL_LIST)
        print('==============================\n')
    else:
        cprint("\nAUTO-EMAILER TERMINATED\nNO EMAILS SENT", 'red')


if __name__ == '__main__':
    main()
