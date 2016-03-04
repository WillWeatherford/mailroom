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
    ('blerg', False),
    ('398fn2_*3j3s2', False),
    ('', False),
]

TEST_NAME = [
    ('x', 'exit'),
    ('list', 'list'),
    ('Bill Gates', 'name'),
    ('BILL Gates', 'name'),
    ('bill gates', 'name'),
    ('Joe', False),
    ('0', False),
    ('B1ll G4t3s', False),
    ('', False),
]


TEST_AMOUNT = [
    ('x', 'exit'),
    ('5', 'amount'),
    ('100', 'amount'),
    ('100.0', 'amount'),
    ('33.33', 'amount'),
    ('5.50', 'amount'),
    ('33.333333', 'amount'),
    ('a thousand simoleans', False),
    ('0', 'amount'),
    ('', False),
]


TEST_UPDATE = [
    ({}, 'Bill Gates'),
    ({'Bill Gates': 5}, 'Bill Gates'),
    ({'Bill Gates': 0.00}, 'Bill Gates')
]


DONOR_DONATIONS = [
    ({'Bill Gates': [455]}, 'Bill Gates', 455),
    ({'Jane Doe': [100]}, 'Jane Doe', 100),
]


DATA_TABLE = [
    ('./donors_test_file.json',
    {
    "Bill Gates": ["5000", "4000.50", "1.0"],
    "Cris Ewing": ["25", "0.50", "1.0"],
    })
]


@pytest.mark.parametrize('user_input, output', MAIN_MENU)
def test_main_menu(user_input, output):
    """Test main menu function."""
    from mailroom import validate_main_menu
    assert validate_main_menu(user_input) == output


@pytest.mark.parametrize('user_input, output', TEST_NAME)
def test_name_menu(user_input, output):
    """Test name_menu validation function."""
    from mailroom import validate_name_menu
    assert validate_name_menu(user_input) == output


@pytest.mark.parametrize('data, name', TEST_UPDATE)
def test_update_name_data(data, name):
    from mailroom import update_donor_data
    update_donor_data(data, name)
    assert name in data.keys()


@pytest.mark.parametrize('user_input, output', TEST_AMOUNT)
def test_amount(user_input, output):
    """Test amount validation function."""
    from mailroom import valid_amount
    assert valid_amount(user_input) == output


@pytest.mark.parametrize('data, input_name, input_amount', DONOR_DONATIONS)
def test_update_donor_donations(data, input_name, input_amount):
    """Test the update of a donor's donation value."""
    from mailroom import update_donor_data
    test_data = {}
    update_donor_data(test_data, input_name, input_amount)
    assert data == test_data


@pytest.mark.parametrize('file_name, data', DATA_TABLE)
def test_donor_file(file_name, data):
    """Test using the JSON file for storing donor data."""
    from mailroom import read_donor_data
    assert read_donor_data(file_name) == data
