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
    """Return float if user has entered valid amount; else 'Invalid amount.'"""
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
    print('Exiting')
    return True


def report():
    rows = []
    for donor, amounts in DATA.items():
        amount_string = ' '.join([format_donation_amount(a) for a in amounts])
        row = ': '.join((donor, amount_string))
        rows.append(row)
    result = menu('\n'.join(rows), None)
    return result


def send():
    result = menu(SEND_MENU_PROMPT, validate_name_menu)
    print('Menu with name menu prompt returns {}'.format(result))
    return False


def name():
    result = menu(AMOUNT_PROMPT, valid_amount)
    print('Menu with amount menu prompt returns {}'.format(result))
    return result


def amount():
    name = WORKING_DONOR_INFO['name']
    amount = WORKING_DONOR_INFO['amount']
    update_donor_donations(name, amount, DATA)
    email = print_email(name, amount)
    menu(email, None)
    return True


def list_donors():
    for donor in DATA:
        print(donor)
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