"""Test mailroom module."""
import pytest


MAIN_MENU = [
    ('send thank you', 'send'),
    ('report', 'report'),
    ('exit', 'exit'),
    ('S', 'send'),
    ('R', 'report'),
    ('X', 'exit'),
    # ('Report on latest pokemon news', 'Invalid entry.'),
    ('blerg', 'Invalid entry.'),
    ('398fn2_*3j3s2', 'Invalid entry.'),
    ('', 'Invalid entry.'),
]

TEST_NAME = [
    ('list', 'list'),
    ('Bill Gates', 'Bill Gates'),
    ('BILL Gates', 'Bill Gates'),
    ('bill gates', 'Bill Gates'),
    ('Joe', 'Invalid name.'),
    ('0', 'Invalid name.'),
    ('B1ll G4t3s', 'Invalid name.'),
    ('', 'Invalid name.'),
]


TEST_AMOUNT = [
    ('5', 5.0),
    ('100', 100.0),
    ('100.0', 100.0),
    ('33.33', 33.33),
    ('5.50', 5.50),
    ('33.333333', 'Invalid amount.'),
    ('a thousand simoleans', 'Invalid amount.'),
    ('0', 'Invalid amount.'),
    ('', 'Invalid amount.'),
]


TEST_UPDATE = [
    ('Bill Gates', {}),
    ('Bill Gates', {'Bill Gates': []}),
    ('Bill Gates', {'Bill Gates': [0.00, 1000.00]})
]


DONOR_DONATIONS = [
    ('Bill Gates', 455, {'Bill Gates': [455]}),
    ('Jane Doe', 100, {'Jane Doe': [100]}),
]

@pytest.mark.parametrize('user_input, output', MAIN_MENU)
def test_main_menu(user_input, output):
    """Test main menu function."""
    from mailroom import main_menu
    assert main_menu(user_input) == output


@pytest.mark.parametrize('user_input, output', TEST_NAME)
def test_name_menu(user_input, output):
    """Test name_menu validation function."""
    from mailroom import name_menu
    assert name_menu(user_input) == output


@pytest.mark.parametrize('name, data', TEST_UPDATE)
def test_update_name_data(name, data):
    from mailroom import update_name_in_database
    update_name_in_database(name, data)
    assert name in data.keys()


@pytest.mark.parametrize('user_input, output', TEST_AMOUNT)
def test_amount(user_input, output):
    """Test amount validation function."""
    from mailroom import valid_amount
    assert valid_amount(user_input) == output


@pytest.mark.parametrize('input_name, input_amount, data', DONOR_DONATIONS)
def test_update_donor_donations(input_name, input_amount, data):
    """Test the update of a donor's donation value."""
    from mailroom import update_donor_donations
    test_data = {}
    update_donor_donations(input_name, input_amount, test_data)
    assert data == test_data
