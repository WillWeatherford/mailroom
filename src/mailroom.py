"""Interactive command-line program to send emails to their donors."""
import re


DATA = {
    'Bill Gates': [5000, 4000.50, 1.0],
    'Cris Ewing': [25, .50, 1.0],
}

WORKING_DONOR_INFO = {'name': '', 'amount': 0}

MAIN_MENU_PROMPT = 'This is the main menu.\n S R X\n'
SEND_MENU_PROMPT = 'This is the send menu.\n list or Enter a Name'
AMOUNT_PROMPT = 'Enter an amount'

EXIT_PATTERN = r'(?P<exit>x|exit)'
MAIN_MENU_PATTERN = r'^(?P<send>s(end)?)|(?P<report>r(eport)?)|' + EXIT_PATTERN
NAME_MENU_PATTERN = r'^(?P<name>[a-z]*\s[a-z]*)|(?P<list>list)|' + EXIT_PATTERN
AMOUNT_PATTERN = r'^(?P<amount>[1-9^0][0-9]*.?[0-9]{,2})|' + EXIT_PATTERN

EMAIL_TEMPLATE = """
Dear {name},

    Thank you for your donation of {amount}.  We really need it.

    Sincerely,

    Someone
"""

DONOR_NAME, TOTAL, NUM, AVG = ('Donor Name', 'Total Donated',
                               'Donations', 'Average Donation')


def validate_main_menu(user_input):
    """Match the user input from main menu."""
    match = re.match(MAIN_MENU_PATTERN, user_input, flags=re.IGNORECASE)
    if not match:
        return False
    return match.lastgroup


def validate_name_menu(user_input):
    """Match the user input from name menu."""
    match = re.match(NAME_MENU_PATTERN, user_input, flags=re.IGNORECASE)
    if not match:
        return False
    WORKING_DONOR_INFO['name'] = match.group('name')
    return match.lastgroup


def valid_amount(user_input):
    """Return float if user has entered valid amount; else 'Invalid amount'."""
    match = re.match(AMOUNT_PATTERN, user_input, flags=re.IGNORECASE)
    if not match:
        return False
    amount = match.group('amount') or 0
    WORKING_DONOR_INFO['amount'] = float(amount)
    return match.lastgroup


def update_name_in_database(full_name, data):
    """Check if name is database; if not, add name."""
    data.setdefault(full_name, [])


def update_donor_donations(name, amount, data):
    donations_list = data.setdefault(name, [])
    donations_list.append(amount)


def format_donation_amount(amount):
    """Format the donation amount into $ and decimal."""
    dollar_format = '${:.2f}'
    return dollar_format.format(amount)


def print_email(name, amount):
    return EMAIL_TEMPLATE.format(name=name,
                                 amount=format_donation_amount(amount))


def exit_menu():
    print('Exiting...')
    return True


def make_report_header():
    cells = ['{:>20}'.format(n) for n in (TOTAL, NUM, AVG)]
    cells.insert(0, '\t{:<20}'.format(DONOR_NAME))
    return ''.join(cells)


def format_donor_row(donor_name, donations):
    total = format_donation_amount(sum(donations))
    num = len(donations)
    avg = format_donation_amount(sum(donations) / float(num))

    cells = ['{:>20}'.format(n) for n in [total, num, avg]]
    cells.insert(0, '\t{:<20}'.format(donor_name))
    return ''.join(cells)


def report():
    rows = [format_donor_row(donor_name, donations)
            for donor_name, donations in DATA.items()]
    rows.insert(0, make_report_header())
    rows.insert(1, '\t' + '-' * 20 * 4)
    menu('\n'.join(rows), None)
    return False


def send():
    menu(SEND_MENU_PROMPT, validate_name_menu)
    return False


def name():
    result = menu(AMOUNT_PROMPT, valid_amount)
    return result


def amount():
    name = WORKING_DONOR_INFO['name']
    amount = WORKING_DONOR_INFO['amount']
    update_donor_donations(name, amount, DATA)
    email = print_email(name, amount)
    menu(email, None)
    return True


def list_donors():
    donor_output = '\n'.join(DATA.keys())
    menu(donor_output, None)
    return False


def menu(prompt, validator):
    while True:
        user_input = input(prompt)
        if validator:
            valid_command = validator(user_input)
            if valid_command:
                func = COMMANDS[valid_command]
                result = func()
                if result:
                    return result
            else:
                print('Invalid command.')
        else:
            break


COMMANDS = {
    'report': report,
    'send': send,
    'name': name,
    'amount': amount,
    'exit': exit_menu,
    'list': list_donors,
}


if __name__ == '__main__':
    menu(MAIN_MENU_PROMPT, validate_main_menu)
