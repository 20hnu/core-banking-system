from db.db_config import get_connection
from datetime import datetime

class Transaction:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
    
    def add_transaction(self, account_id, transaction_type, amount, remarks,to_account_id=None):
        if account_id != account_id:
            try:
                txn_query = """ INSERT INTO Transactions (account_id, type, amount,remarks,status,to_account_id) VALUES (%s, %s, %s, %s, %s, %s) """
                # self.cursor.execute(txn_query,(1, "Deposit",80000, "Salary","Success",None))
                self.cursor.execute(txn_query,(account_id, transaction_type,amount,remarks,"Success",None))


                if transaction_type == "Deposit":
                    balance_query = "UPDATE Account SET balance = balance + %s WHERE account_id = %s"
                elif transaction_type == "Withdraw":
                    balance_query = "UPDATE Account SET balance = balance - %s WHERE account_id = %s"
                else:
                    sender_balance_query = "UPDATE Account SET balance = balance - %s WHERE account_id = %s"
                    reciever_balance_query = "UPDATE Account SET balance = balance + %s WHERE account_id = %s"
                    self.cursor.execute(sender_balance_query,(amount,account_id))
                    self.cursor.execute(reciever_balance_query,(amount,to_account_id))
                    self.conn.commit()
                    print("Transaction successful")
                    return True

                self.cursor.execute(balance_query,(amount,account_id))
                self.conn.commit()
                print("Transaction successful")
                return True
            
            except Exception as e:
                self.conn.rollback()
                print("Error",e)
                return False
        else:
            print("Transaction failed")
            return False

    

    