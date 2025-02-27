from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import math

# Bank System Data Structures
accounts = {}
transactions = {}
loans = {}

MAX_LOAN_AMOUNT = 10000
INTEREST_RATE = 0.03


class BankApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
            if name in accounts:
                QMessageBox.warning(self, "Error", "Account already exists!")
            else:
                accounts[name] = 0
                transactions[name] = []
                loans[name] = 0
                QMessageBox.information(self, "Success", "Account created successfully!")

    def deposit(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Deposit", "Enter account name:")
        if ok and name in accounts:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Deposit", "Enter amount:", min=1)
            if ok:
                accounts[name] += amount
                transactions[name].append(f"Deposited ${amount}")
                QMessageBox.information(self, "Success", f"Deposited ${amount} into {name}'s account.")
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def withdraw(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Withdraw", "Enter account name:")
        if ok and name in accounts:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Withdraw", "Enter amount:", min=1)
            if ok and accounts[name] >= amount:
                accounts[name] -= amount
                transactions[name].append(f"Withdrew ${amount}")
                QMessageBox.information(self, "Success", f"Withdrew ${amount} from {name}'s account.")
            else:
                QMessageBox.warning(self, "Error", "Insufficient funds!")
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def check_balance(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Check Balance", "Enter account name:")
        if ok and name in accounts:
            QMessageBox.information(self, "Balance", f"{name}'s Balance: ${accounts[name]}")
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def transfer_funds(self):
        sender, ok = QtWidgets.QInputDialog.getText(self, "Transfer", "Enter sender account name:")
        if ok and sender in accounts:
            receiver, ok = QtWidgets.QInputDialog.getText(self, "Transfer", "Enter receiver account name:")
            if ok and receiver in accounts:
                amount, ok = QtWidgets.QInputDialog.getDouble(self, "Transfer", "Enter amount:", min=1)
                if ok and accounts[sender] >= amount:
                    accounts[sender] -= amount
                    accounts[receiver] += amount
                    transactions[sender].append(f"Transferred ${amount} to {receiver}")
                    transactions[receiver].append(f"Received ${amount} from {sender}")
                    QMessageBox.information(self, "Success", "Transfer successful!")
                else:
                    QMessageBox.warning(self, "Error", "Insufficient funds!")
            else:
                QMessageBox.warning(self, "Error", "Receiver account not found!")
        else:
            QMessageBox.warning(self, "Error", "Sender account not found!")

    def view_transaction_history(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Transactions", "Enter account name:")
        if ok and name in transactions:
            history = "\n".join(transactions[name]) or "No transactions yet."
            QMessageBox.information(self, "Transaction History", history)
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def apply_for_loan(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Apply for Loan", "Enter account name:")
        if ok and name in accounts:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Loan", "Enter loan amount:", min=1,
                                                          max=MAX_LOAN_AMOUNT)
            if ok:
                loans[name] += amount * (1 + INTEREST_RATE)
                accounts[name] += amount
                QMessageBox.information(self, "Success", f"Loan approved for ${amount}. Interest applied.")
        else:
            QMessageBox.warning(self, "Error", "Account not found!")

    def repay_loan(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "Repay Loan", "Enter account name:")
        if ok and name in loans and loans[name] > 0:
            amount, ok = QtWidgets.QInputDialog.getDouble(self, "Repay Loan", "Enter repayment amount:", min=1)
            if ok and accounts[name] >= amount:
                loans[name] -= amount
                accounts[name] -= amount
                QMessageBox.information(self, "Success", "Loan repaid successfully.")
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
        if ok and name in accounts:
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


app = QtWidgets.QApplication([])
window = BankApp()
window.show()
app.exec_()
