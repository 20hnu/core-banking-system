from models.customers import Customer
from models.transaction import Transaction

customer = Customer()
txn = Transaction()
def open_account():
    customer_details ={
        "first_name" : "Ramesh",
        "middle_name" :"Kumar",
        "last_name" : "Sharma",
        "email" : "sharma.ramesh.2081@gmail.com",
        "phone_number" :"980597499",
        "dob" : "2058-01-01"
    }
    account_details = {
        "account_type" : "Savings",
        "account_number" : "473569234",
        "balance" : 50000
    }
    authenticate_details = {
        "username" : "ramesh",
        "password" : ";'[h]"
    }

    if customer.open_account(customer_details,account_details,authenticate_details):
        print("Account opened")
    else:
        print("Failed to open account")

def login():
    user_name = "bishow"
    password = "12345678"
    user = customer.login(user_name,password)
    if user:
        print("Login success")
        if txn.add_transaction(user['customer_id'], "Deposit", 80000):
            print("Transaction completed")

# login()
open_account()