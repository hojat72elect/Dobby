from src.oop.BankAccount import BankAccount

if __name__ == '__main__':

    account = BankAccount(name='Joe', balance=100, password='soup')

    while True:
        print()
        print('Press b to get the balance')
        print('Press d to make a deposit')
        print('Press w to make a withdrawal')
        print('Press s to show the account')
        print('Press q to quit\n')

        action: str = input('What do you want to do? ').lower()[0]

        if action == 'b':
            print('\nGet Balance:')
            user_password: str = input('Please enter the password: ')
            if user_password != account.password:
                print('Incorrect password')
            else:
                print('Your balance is:', account.balance)

        elif action == 'd':
            print('Deposit:')
            user_deposit_amount = int(input('Please enter amount to deposit: '))
            user_password: str = input('Please enter the password: ')

            if user_deposit_amount < 0:
                print('You cannot deposit a negative amount!')

            elif user_password != account.password:
                print('Incorrect password')

            else:  # everything was OK
                account.balance += user_deposit_amount
                print('Your new balance is:', account.balance)

        elif action == 's':
            print('Show:')
            print('       Name', account.name)
            print('       Balance:', account.balance)
            print('       Password:', account.password)
            print()

        elif action == 'q':
            break

        elif action == 'w':
            print('Withdraw:')

            user_withdraw_amount = int(input('Please enter the amount to withdraw: '))
            user_password = input('Please enter the password: ')

            if user_withdraw_amount < 0:
                print('You cannot withdraw a negative amount')

            elif user_password != account.password:
                print('Incorrect password for this account')

            elif user_withdraw_amount > account.balance:
                print('You cannot withdraw more than you have in your account')

            else:  # Everything was OK
                account.balance -= user_withdraw_amount
                print(f'Your new balance is : {account.balance}')

    print('Done')
