from db.db_config import get_connection
from datetime import datetime

class Transaction:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
    
    def add_transaction(self, customer_id, transaction_type, amount):
        try:
            txn_query = """ INSERT INTO Transactions (account_id, type, amount,remarks,status,to_account_id) VALUES (%s, %s, %s, %s, %s, %s) """
            # self.cursor.execute(txn_query,(1, "Deposit",80000, "Salary","Success",None))
            self.cursor.execute(txn_query,(customer_id, transaction_type,amount,"Salary","Success",None))
            self.conn.commit()
            return True
        
        except Exception as e:
            self.conn.rollback()
            print("Error",e)
            return False

    

    