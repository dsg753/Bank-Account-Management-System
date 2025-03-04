from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import math
import json
import os

MAX_LOAN_AMOUNT = 10000
INTEREST_RATE = 0.03


class BankApp(QtWidgets.QWidget):
    def __init__(self, mode="demo"):
        super().__init__()
        self.mode = mode
        print(f"Running in {self.mode} mode")
        self.init_data()
        self.initUI()

    def init_data(self):
        if self.mode == "persistent":
            self.load_data()
        else:
            self.accounts = {}
            self.transactions = {}
            self.loans = {}

    def load_data(self):
        print(f"Current working directory: {os.getcwd()}")
        if os.path.exists("accounts.json"):
            with open("accounts.json", "r") as f:
                self.accounts = json.load(f)
        else:
            self.accounts = {}

        if os.path.exists("transactions.json"):
            with open("transactions.json", "r") as f:
                self.transactions = json.load(f)
        else:
            self.transactions = {}

        if os.path.exists("loans.json"):
            with open("loans.json", "r") as f:
                self.loans = json.load(f)
        else:
            self.loans = {}

    def save_data(self):
        print("Saving data...")
        with open("accounts.json", "w") as f:
            json.dump(self.accounts, f)
        with open("transactions.json", "w") as f:
            json.dump(self.transactions, f)
        with open("loans.json", "w") as f:
            json.dump(self.loans, f)
        print("Data saved successfully")

    def initUI(self):
        self.setWindowTitle("Bank Account Management")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("🏦 Welcome To George`s Bank System")
        self.layout.addWidget(self.label)

        buttons = [
            ("Create Account", self.create_account),
            ("Deposit Money", self.deposit),
            ("Withdraw Money", self.withdraw),
            ("Check Balance", self.check_balance),
            ("Transfer Funds", self.transfer_funds),
            ("Transaction History", self.view_transaction_history),
            ("Apply for Loan", self.apply_for_loan),
            ("Repay Loan", self.repay_loan),
            ("Identify Card Type", self.identify_card_type),
            ("Loan Calculator", self.loan_calculator),
        ]

        for text, func in buttons:
            btn = QtWidgets.QPushButton(text)
            btn.clicked.connect(func)
            self.layout.addWidget(btn)

        self.setLayout(self.layout)

    def create_account(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Create Account", "Enter account name:")
        if ok and name:
            if name in self.accounts:
                QMessageBox.warning(self, "Error", "Account already exists!")
            else:
                self.accounts[name] = 0
                self.transactions[name] = []
                self.loans[name] = 0
                QMessageBox.information(self, "Success", "Account created successfully!")
                if self.mode == "persistent":
                    self.save_data()

    def deposit(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Deposit", "Enter account name:")
        if ok and name in self.accounts:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Deposit", "Enter amount:", min=1)
            if ok:
                self.accounts[name] += amount
                self.transactions[name].append(f"Deposited ${amount}")
                QMessageBox.information(self, "Success", f"Deposited ${amount} into {name}'s account.")
                if self.mode == "persistent":
                    self.save_data()
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def withdraw(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Withdraw", "Enter account name:")
        if ok and name in self.accounts:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Withdraw", "Enter amount:", min=1)
            if ok and self.accounts[name] >= amount:
                self.accounts[name] -= amount
                self.transactions[name].append(f"Withdrew ${amount}")
                QMessageBox.information(self, "Success", f"Withdrew ${amount} from {name}'s account.")
                if self.mode == "persistent":
                    self.save_data()
            else:
                QMessageBox.warning(self, "Error", "Insufficient funds!")
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def check_balance(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Check Balance", "Enter account name:")
        if ok and name in self.accounts:
            QMessageBox.information(self, "Balance", f"{name}'s Balance: ${self.accounts[name]}")
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def transfer_funds(self):
        sender, ok = QtWidgets.QInputDialog.getText(self, "Transfer", "Enter sender account name:")
        if ok and sender in self.accounts:
            receiver, ok = QtWidgets.QInputDialog.getText(self, "Transfer", "Enter receiver account name:")
            if ok and receiver in self.accounts:
                amount, ok = QtWidgets.QInputDialog.getDouble(self, "Transfer", "Enter amount:", min=1)
                if ok and self.accounts[sender] >= amount:
                    self.accounts[sender] -= amount
                    self.accounts[receiver] += amount
                    self.transactions[sender].append(f"Transferred ${amount} to {receiver}")
                    self.transactions[receiver].append(f"Received ${amount} from {sender}")
                    QMessageBox.information(self, "Success", "Transfer successful!")
                    if self.mode == "persistent":
                        self.save_data()
                else:
                    QMessageBox.warning(self, "Error", "Insufficient funds!")
            else:
                QMessageBox.warning(self, "Error", "Receiver account not found!")
        else:
            QMessageBox.warning(self, "Error", "Sender account not found!")

    def view_transaction_history(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Transactions", "Enter account name:")
        if ok and name in self.transactions:
            history = "\n".join(self.transactions[name]) or "No transactions yet."
            QMessageBox.information(self, "Transaction History", history)
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def apply_for_loan(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Apply for Loan", "Enter account name:")
        if ok and name in self.accounts:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Loan", "Enter loan amount:", min=1,
                                                          max=MAX_LOAN_AMOUNT)
            if ok:
                self.loans[name] += amount * (1 + INTEREST_RATE)
                self.accounts[name] += amount
                QMessageBox.information(self, "Success", f"Loan approved for ${amount}. Interest applied.")
                if self.mode == "persistent":
                    self.save_data()
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def repay_loan(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Repay Loan", "Enter account name:")
        if ok and name in self.loans and self.loans[name] > 0:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Repay Loan", "Enter repayment amount:", min=1)
            if ok and self.accounts[name] >= amount:
                self.loans[name] -= amount
                self.accounts[name] -= amount
                QMessageBox.information(self, "Success", "Loan repaid successfully.")
                if self.mode == "persistent":
                    self.save_data()
            else:
                QMessageBox.warning(self, "Error", "Insufficient funds!")
        else:
            QMessageBox.warning(self, "Error", "No outstanding loan!")

    def identify_card_type(self):
        card_number, ok = QtWidgets.QInputDialog.getText(self, "Identify Card Type", "Enter credit card number:")
        if ok and card_number:
            if card_number.startswith("4"):
                card_type = "Visa"
            elif card_number[:2] in ["51", "52", "53", "54", "55"]:
                card_type = "MasterCard"
            elif card_number[:2] in ["34", "37"]:
                card_type = "American Express"
            else:
                card_type = "Other"
            QMessageBox.information(self, "Card Type", f"Your card type is: {card_type}")
        else:
            QMessageBox.warning(self, "Error", "Invalid card number!")

    def loan_calculator(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Loan Calculator", "Enter account name:")
        if ok and name in self.accounts:
            loan_amount, ok = QtWidgets.QInputDialog.getDouble(self, "Loan Calculator", "Enter loan amount:", min=1)
            if ok:
                interest_rate, ok = QtWidgets.QInputDialog.getDouble(self, "Loan Calculator", "Enter annual interest rate (in %):", min=0.01)
                if ok:
                    loan_term, ok = QtWidgets.QInputDialog.getInt(self, "Loan Calculator", "Enter loan term (in years):", min=1)
                    if ok:
                        monthly_rate = interest_rate / 100 / 12
                        num_payments = loan_term * 12
                        monthly_payment = loan_amount * monthly_rate / (1 - math.pow(1 + monthly_rate, -num_payments))
                        total_payment = monthly_payment * num_payments
                        total_interest = total_payment - loan_amount
                        payoff_date = QtCore.QDate.currentDate().addMonths(num_payments).toString("MMMM yyyy")

                        result = (f"Monthly Payment: ${monthly_payment:.2f}\n"
                                  f"Total Interest Paid: ${total_interest:.2f}\n"
                                  f"Total Payment: ${total_payment:.2f}\n"
                                  f"Payoff Date: {payoff_date}")

                        QMessageBox.information(self, "Loan Calculator Result", result)
        else:
            QMessageBox.warning(self, "Error", "Account not found!")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    mode, ok = QtWidgets.QInputDialog.getItem(None, "Select Mode", "Choose mode:", ["demo", "persistent"], 0, False)
    if ok:
        window = BankApp(mode=mode)
        window.show()
        sys.exit(app.exec_())
