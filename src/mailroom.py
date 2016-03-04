import re

EXIT_PATTERN = r'(?P<exit>x|exit)'
MAIN_MENU_PATTERN = r'^(?P<send>s(end)?)|(?P<report>r(eport)?)|' + EXIT_PATTERN
NAME_MENU_PATTERN = r'^(?P<name>[a-z]*\s[a-z]*)|(?P<list>list)|' + EXIT_PATTERN
AMOUNT_PATTERN = r'^(?P<amount>[^0][0-9]*.?[0-9]{,2})$'


def main_menu(user_input):
    match = re.match(MAIN_MENU_PATTERN, user_input, flags=re.IGNORECASE)
    if not match:
        return 'Invalid entry.'
    return match.lastgroup


def name_menu(user_input):
    match = re.match(NAME_MENU_PATTERN, user_input, flags=re.IGNORECASE)
    if not match:
        return 'Invalid name.'
    if match.group('list'):
        return 'list'
    return match.group('name').title()


def update_name_in_database(full_name, data):
    """Check if name is database; if not, add name."""
    data.setdefault(full_name, [])


def valid_amount(user_input):
    """Return float if user has entered valid amount; else 'Invalid amount.'"""
    match = re.match(AMOUNT_PATTERN, user_input)
    if not match:
        return 'Invalid amount.'
    return float(match.group('amount'))


def update_donor_donations(name, amount, data):
    donations_list = data.setdefault(name, [])
    donations_list.append(amount)
