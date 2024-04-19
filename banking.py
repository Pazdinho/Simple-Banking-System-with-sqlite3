import random
import numpy as np
from random import choice
import sqlite3

# This is simple banking system connected to database
class BankAccount:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.create_table()
        self.set_of_accounts = set()
        self.balance = 0
        self.menu()
    def menu(self):
        while True:
            print('\n1. Create an account \n2. Log into account \n0. Exit')
            option = int(input())
            if option == 1:
                self.account_creator()
            elif option == 2:
                self.log_in()
            elif option == 0:
                print('Bye!')
                break
            else:
                print('Wrong number! Please pick once again')

    def account_creator(self):

        id = 1
        account = self.card_number_generator()
        pin = str(''.join([str(random.randint(0, 9)) for x in range(4)]))
        self.save_acc(id, account, pin)
        id += 1
        return print(f'\nYour card has been created\nYour card number:\n{account}\nYour card PIN:\n{pin}')

    def save_acc(self, id, account, pin):
        sql = "INSERT INTO card (id, number, pin) VALUES (?, ?, ?)"
        values = (id, account, pin)
        self.cur.execute(sql, values)
        self.conn.commit()

    def create_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
        self.conn.commit()
    def log_in(self):
        print('\nEnter your card number:')
        mycard = str(input())
        print('Enter your PIN:')
        mypin = str(input())
        self.logged_acc = self.get_data_login(mycard, mypin)
        if self.logged_acc:
            print('You have successfully logged in!')
            self.account_panel()
        else:
            print('Wrong number!')

    def get_data_login(self, card, pin):
        sql = "SELECT id, number FROM card WHERE number = ? AND pin = ?"
        values = (card, pin)
        self.cur.execute(sql, values)
        return self.cur.fetchone()

    def get_data(self, number):
         sql = "SELECT balance, number FROM card WHERE number LIKE ?"
         values = [number]
         self.cur.execute(sql, values)
         return self.cur.fetchone()

    def update_data(self, income, number):
        sql = "UPDATE card SET balance = ? WHERE number = ?"
        balance = self.get_data(number)
        values = (balance[0] + income, number)
        self.cur.execute(sql, values)
        self.conn.commit()
        pass
    def add_income(self):
        print('Enter income:')
        income = int(input())
        self.update_data(income, self.logged_acc[1])
        print('Income was added!')

    def do_transfer(self):
        print('Transfer \nEnter card number')
        number = str(input())
        if self.numbercheck(number) is False:
            pass
        else:
            print('Enter how much money you want to transfer:')
            money_out = int(input())
            if self.money_check(money_out) is False:
                pass
            else:
                self.update_data(-money_out, self.logged_acc[1])
                self.update_data(money_out, number)
                print('Success!')

    def numbercheck(self, number):
        check = self.get_data(self.logged_acc[1])
        if number != self.luhn_alghoritm(number[:-1]):
            print('Probably you made a mistake in the card number. Please try again!')
            return False
        else:
            if number == check[1]:
                print("You can't transfer money to the same account!")
                return False
            elif number[:-1] not in self.set_of_accounts:
                print('Such a card does not exist')
                return False
            else:
                return True
    def money_check(self,money_out):
        balance = self.get_data(self.logged_acc[1])
        if money_out > balance[0]:
            print('Not enough money!')
            return False
        else:
            return True
    def close_account(self):
        sql = "DELETE FROM card WHERE id = ?"
        values = [self.logged_acc[0]]
        self.cur.execute(sql, values)
        self.conn.commit()
        return (print('The account has been closed!'))
    def account_panel(self):
        while True:
            print('\n1. Balance \n2. Add income \n3. Do transfer \n4. Close account \n5. Log out \n0. Exit')
            option = int(input())
            if option == 1:
                balance = self.get_data(self.logged_acc[1])
                print(f"Balance: {balance[0]}")
            elif option == 2:
                self.add_income()
            elif option == 3:
                self.do_transfer()
            elif option == 4:
                self.close_account()
                break
            elif option == 5:
                print('\nYou have successfully logged out!')
                break
            elif option == 0:
                print('Bye!')
                exit()
            else:
                print('Wrong number! Please pick once again')

    def card_number_generator(self):
        acc_number = str('400000' + ''.join([str(random.randint(0, 9)) for x in range(9)]))

        # To check whether this account number already exists or not
        while acc_number in self.set_of_accounts:
            acc_number = str('400000' + ''.join([str(random.randint(0, 9)) for x in range(9)]))

        self.set_of_accounts.add(acc_number)
        return self.luhn_alghoritm(acc_number)

    def luhn_alghoritm (self, acc_number):
        help = list(map(int, acc_number))
        for i in range(0, len(acc_number), 2):
            if help[i] < 5:
                help[i] = help[i] * 2
            else:
                help[i] = help[i] * 2 - 9

        if sum(help) % 10 == 0:
            acc_number = str(acc_number + '0')
        else:
            acc_number = str(acc_number + f'{10 - sum(help) % 10}')

        return acc_number

if __name__ == '__main__':
    BankAccount()
