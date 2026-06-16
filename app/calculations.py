def sum(num1: int, num2: int) -> int:
    """Returns the sum of two numbers."""
    return num1 + num2

def multiply(num1: int, num2: int) -> int:
    """Returns the product of two numbers."""
    return num1 * num2

def divide(num1: int, num2: int) -> float:
    """Returns the quotient of two numbers."""
    return num1 / num2

def subtract(num1: int, num2: int) -> int:
    """Returns the difference of two numbers."""
    return num1 - num2


class BankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Deposits a specified amount into the account."""
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraws a specified amount from the account if sufficient funds are available."""
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def collect_interest(self) -> None:
        """Collects interest on the current balance."""
        self.balance *= 1.1 