import pytest
from app.calculations import sum, multiply, divide, subtract, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize ("num1, num2, expected", [
    (5, 3, 8),
    (10, 20, 30),
    (0, 0, 0),
    (-5, -3, -8),
    (-5, 3, -2)
])
def test_add(num1, num2, expected):
    print("Testing the sum function...")
    assert sum(num1, num2) == expected


def test_subtract():
    print("Testing the subtract function...")
    assert subtract(5, 3) == 2

def test_multiply():
    print("Testing the multiply function...")
    assert multiply(5, 3) == 15

def test_divide():
    print("Testing the divide function...")
    assert divide(5, 3) == 5/3

def test_bank_set_initial_balance(bank_account):
    assert bank_account.balance == 100

def test_bank_default_initial_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 70

def test_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 150

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 110

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(ValueError):
        zero_bank_account.withdraw(200)