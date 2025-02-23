class BankAccount():
    """
    This is a class to represent a bank account.
    """

    def __init__(self, name: str, balance: int, password: str):
        self.name = name
        self.balance = balance
        self.password = password

    def deposit(self, amount_to_deposit: int, password: str) -> int | None:
        if password != self.password:
            print('Sorry, incorrect password')
            return None

        # User has provided the correct password
        if amount_to_deposit <= 0:
            print('The amount to deposit must be greater than zero')
            return None

        # The amount to deposit is greater than zero
        self.balance += amount_to_deposit
        return self.balance

    def withdraw(self, amount_to_withdraw: int, password: str) -> int | None:
        if password != self.password:
            print('Incorrect password for this account')
            return None

        # User has provided the correct password
        if amount_to_withdraw <= 0:
            print('The amount to withdraw must be greater than zero')
            return None

        # The amount to withdraw is greater than zero
        if amount_to_withdraw > self.balance:
            print('You cannot withdraw more than you have in your account')
            return None

        # The amount to withdraw is less than or equal to the balance
        self.balance -= amount_to_withdraw
        return self.balance

    def getBalance(self, password: str) -> int | None:
        if password != self.password:
            print('Sorry, incorrect password')
            return None
        return self.balance

    # Added for debugging
    def show(self):
        print(f'       Name : {self.name}')
        print(f'       Balance : {self.balance}')
        print(f'       Password : {self.password}')
