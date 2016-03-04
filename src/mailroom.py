"""Interactive command-line program to send emails to their donors."""
import re
import json
import io
import sys


WORKING_DONOR_INFO = {'name': '', 'amount': 0}

MAIN_MENU_PROMPT = """
Welcome to Mailroom Madness!

MAIN MENU

S: Send an email to a donor.
R: Print report of all donations so far.
X: Exit from the program.
"""
SEND_MENU_PROMPT = """
SEND MENU

Register a new donation and send an email to the donor.

L: List all existing donors.
X: Exit to main menu.

Or enter a donor's name.
"""

DONOR_LIST = """
Here are all the nice people who have donated so far:

{}
"""

AMOUNT_PROMPT = """
Enter the amount donated by {}:
"""

EXIT_RGX = r'(?P<exit>x|exit)'
MAIN_MENU_RGX = r'^(?P<send>s(end)?)|(?P<report>r(eport)?)|' + EXIT_RGX
NAME_MENU_RGX = r'^(?P<name>[a-z]*\s[a-z]*)|(?P<list>l(ist)?)|' + EXIT_RGX
AMOUNT_RGX = r'^(?P<amount>[1-9^0][0-9]*.?[0-9]{,2})|' + EXIT_RGX

EMAIL_TEMPLATE = """
Dear {name},

    Thank you for your donation of {amount} to The Friends of The Large Hadron
    Collider. We really need it.

    Sincerely,

    Dr. Evil
"""

DONOR_NAME, TOTAL, NUM, AVG = ('Donor Name', 'Total Donated',
                               'Donations', 'Average Donation')


DONORS_JSON = 'src/donors.json'

USAGE = """
Usage: mailroom takes no arguments.
"""


def validate_main_menu(user_input):
    """Match the user input from main menu."""
    match = re.match(MAIN_MENU_RGX, user_input, flags=re.IGNORECASE)
    if not match:
        return False
    return match.lastgroup


def validate_name_menu(user_input):
    """Match the user input from name menu."""
    match = re.match(NAME_MENU_RGX, user_input, flags=re.IGNORECASE)
    if not match:
        return False
    WORKING_DONOR_INFO['name'] = str(match.group('name')).title()
    return match.lastgroup


def valid_amount(user_input):
    """Return float if user has entered valid amount; else 'Invalid amount'."""
    # Validator info avialable in the regex docs for the re module.
    match = re.match(AMOUNT_RGX, user_input, flags=re.IGNORECASE)
    if not match:
        return False
    amount = match.group('amount') or 0
    WORKING_DONOR_INFO['amount'] = float(amount)
    return match.lastgroup


def update_donor_data(data, name, amount=0):
    """Check if name is database; if not, add name and donation amount."""
    donations_list = data.setdefault(name, [])
    if amount:
        donations_list.append(amount)


def read_donor_data(file_name):
    """Return dictionary from reading JSON file."""
    data_file = io.open(file_name)
    data = json.load(data_file)
    data_file.close()
    return data


def write_donor_data(data, file_name):
    """Write data from dictionary to file."""
    data_file = io.open(file_name, 'w')
    data = json.dump(data, data_file)
    data_file.close()


def format_donation_amount(amount):
    """Format the donation amount into $ and 2 decimal places."""
    dollar_format = '${:.2f}'
    return dollar_format.format(amount)


def format_email(name, amount):
    """Format the email with correct donor name and amount."""
    return EMAIL_TEMPLATE.format(name=name,
                                 amount=format_donation_amount(amount))


def exit_menu():
    """User exit out of current menu & out of the module if at main menu."""
    return True


def make_report_header():
    """Format the top row of report print output."""
    cells = ['{:>20}'.format(n) for n in (TOTAL, NUM, AVG)]
    cells.insert(0, '\t{:<20}'.format(DONOR_NAME))
    return ''.join(cells)


def format_donor_row(donor_name, donations):
    """Format donor row in report print out."""
    donations = list(map(float, donations))
    total = format_donation_amount(sum(donations))
    num = len(donations)
    avg = format_donation_amount(sum(donations) / float(num))

    cells = ['{:>20}'.format(n) for n in [total, num, avg]]
    cells.insert(0, '\t{:<20}'.format(donor_name))
    return ''.join(cells)


def report():
    """Assemble and display the report of current donors; wait for continue."""
    rows = [format_donor_row(donor_name, donations)
            for donor_name, donations in read_donor_data(DONORS_JSON).items()]
    rows.insert(0, make_report_header())
    rows.insert(1, '\t' + '-' * 20 * 4)
    menu('\n'.join(rows), None)
    return False


def send():
    """Display send menu prompt and wait for valid command."""
    menu(SEND_MENU_PROMPT, validate_name_menu)
    return False


def enter_amount():
    """Display donation amount prompt and wait for valid amount."""
    donor_name = WORKING_DONOR_INFO['name']
    amount_prompt = AMOUNT_PROMPT.format(donor_name)
    result = menu(amount_prompt, valid_amount)
    return result


def display_email():
    """Assemble and display donor thank you email; wait for continue."""
    name = WORKING_DONOR_INFO['name']
    amount = WORKING_DONOR_INFO['amount']

    current_data = read_donor_data(DONORS_JSON)
    update_donor_data(current_data, name, amount)
    write_donor_data(current_data, DONORS_JSON)

    email = format_email(name, amount)
    menu(email, None)

    WORKING_DONOR_INFO['name'] = ''
    WORKING_DONOR_INFO['amount'] = 0
    return True


def list_donors():
    """Assemble and display list of current donor names."""
    donor_data = read_donor_data(DONORS_JSON)
    donor_output = DONOR_LIST.format('\n'.join(donor_data.keys()))
    menu(donor_output, None)
    return False


def menu(prompt, validator):
    """Prompt user, validate input and execute appriate function."""
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

# This table associates valid command keywords to the correct menu functions.
COMMANDS = {
    'report': report,
    'send': send,
    'name': enter_amount,
    'amount': display_email,
    'exit': exit_menu,
    'list': list_donors,
}


def main():
    """Main funct."""
    if len(sys.argv) != 1:
        print(USAGE)
        sys.exit(1)

    menu(MAIN_MENU_PROMPT, validate_main_menu)
    sys.exit(0)
