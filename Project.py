import pickle
import os
import tkinter as tk
from tkinter import messagebox


class BankAccount:
    def __init__(self, account_number, account_holder_name, balance=0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def transfer(self, receiver, amount):
        if amount > 0 and amount <= self.balance:
            self.withdraw(amount)
            receiver.deposit(amount)
            return True
        return False

    def __str__(self):
        return f"Account Number: {self.account_number}, Account Holder: {self.account_holder_name}, Balance: ${self.balance}"


class BankingSystem:
    DATA_FILE = "accounts.dat"

    def __init__(self):
        self.accounts = self.load_accounts()

    def create_account(self, account_number, account_holder_name, initial_deposit):
        if account_number in self.accounts:
            return False
        new_account = BankAccount(account_number, account_holder_name, initial_deposit)
        self.accounts[account_number] = new_account
        return True

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def save_accounts(self):
        with open(self.DATA_FILE, 'wb') as file:
            pickle.dump(self.accounts, file)

    def load_accounts(self):
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'rb') as file:
                return pickle.load(file)
        return {}


class BankingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking System")
        self.banking_system = BankingSystem()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Create Account
        tk.Label(self.master, text="Account Number").grid(row=0, column=0)
        self.account_number_entry = tk.Entry(self.master)
        self.account_number_entry.grid(row=0, column=1)

        tk.Label(self.master, text="Account Holder Name").grid(row=1, column=0)
        self.account_holder_entry = tk.Entry(self.master)
        self.account_holder_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Initial Deposit").grid(row=2, column=0)
        self.initial_deposit_entry = tk.Entry(self.master)
        self.initial_deposit_entry.grid(row=2, column=1)

        tk.Button(self.master, text="Create Account", command=self.create_account).grid(row=3, columnspan=2)

        # Deposit
        tk.Label(self.master, text="Deposit Amount").grid(row=4, column=0)
        self.deposit_amount_entry = tk.Entry(self.master)
        self.deposit_amount_entry.grid(row=4, column=1)

        tk.Button(self.master, text="Deposit", command=self.deposit).grid(row=5, columnspan=2)

        # Withdraw
        tk.Label(self.master, text="Withdraw Amount").grid(row=6, column=0)
        self.withdraw_amount_entry = tk.Entry(self.master)
        self.withdraw_amount_entry.grid(row=6, column=1)

        tk.Button(self.master, text="Withdraw", command=self.withdraw).grid(row=7, columnspan=2)

        # Check Balance
        tk.Button(self.master, text="Check Balance", command=self.check_balance).grid(row=8, columnspan=2)

        # Exit Button
        tk.Button(self.master, text="Exit", command=self.exit_program).grid(row=9, columnspan=2)

    def create_account(self):
        account_number = self.account_number_entry.get()
        account_holder_name = self.account_holder_entry.get()
        initial_deposit = float(self.initial_deposit_entry.get())

        if self.banking_system.create_account(account_number, account_holder_name, initial_deposit):
            messagebox.showinfo("Success", "Account created successfully.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Account number already exists.")

    def deposit(self):
        account_number = self.account_number_entry.get()
        amount = float(self.deposit_amount_entry.get())
        account = self.banking_system.get_account(account_number)

        if account and account.deposit(amount):
            messagebox.showinfo("Success", "Deposit successful.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Account not found or invalid amount.")

    def withdraw(self):
        account_number = self.account_number_entry.get()
        amount = float(self.withdraw_amount_entry.get())
        account = self.banking_system.get_account(account_number)

        if account and account.withdraw(amount):
            messagebox.showinfo("Success", "Withdrawal successful.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Account not found or insufficient funds.")

    def check_balance(self):
        account_number = self.account_number_entry.get()
        account = self.banking_system.get_account(account_number)

        if account:
            messagebox.showinfo("Balance", str(account))
        else:
            messagebox.showerror("Error", "Account not found.")

    def exit_program(self):
        self.banking_system.save_accounts()
        self.master.quit()

    def clear_entries(self):
        self.account_number_entry.delete(0, tk.END)
        self.account_holder_entry.delete(0, tk.END)
        self.initial_deposit_entry.delete(0, tk.END)
        self.deposit_amount_entry.delete(0, tk.END)
        self.withdraw_amount_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()

