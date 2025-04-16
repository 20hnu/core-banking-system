from models.customers import Customer
from models.transaction import Transaction
from models.analytics import update_analytics


def banking_system():
    customer = Customer()
    txn = Transaction()

    print("Welcome to Chad Banking System")
    print("Please login:")
    user_name = input("Username: ")
    password = input("Password: ")
    user = customer.login(user_name,password)
    if user:
        print("Login success")
        print("Choose Transaction type: \n1. Deposit \n2. Withdraw \n3. Transfer \n4. Payment")
        txn_type = int(input("Enter transaction type: "))
        amount = int(input("Enter amount: "))
        remarks = input("Enter remarks: ")
        try:
            if txn_type == 1 :
                txn.add_transaction(user['account_id'], "Deposit", amount,remarks)
            elif txn_type == 2:
                txn.add_transaction(user['account_id'], "Withdraw", amount,remarks)
            elif txn_type == 4:
                txn.add_transaction(user['account_id'], "Payment", amount,remarks)
            else:
                to_account_id = int(input("Enter to account id: "))
                txn.add_transaction(user['account_id'], "Transfer", amount,remarks, to_account_id)

            update_analytics(user['account_id'],txn_type,amount)
        except Exception as e:
            print("Error:",e)
            print("Transaction failed")

    else:
        print("Login failed")

if __name__ == '__main__':
    banking_system()