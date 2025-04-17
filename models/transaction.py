from dbconnect.db_config import get_connection
from models.analytics import update_analytics

class Transaction:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def add_transaction(self, account_id, transaction_type, amount, remarks, to_account_id=None):
        if account_id != to_account_id:
            try:
                # Check account balance
                balance_query = "SELECT balance FROM Account WHERE account_id = %s"
                self.cursor.execute(balance_query, (account_id,))
                account_balance = self.cursor.fetchone()['balance']

                # Restrict withdrawal, payment, or transfer if balance is insufficient
                if transaction_type in ["Withdraw", "Payment", "Transfer"] and amount > account_balance:
                    # Record failed transaction
                    txn_query = """ INSERT INTO Transactions (account_id, type, amount, remarks, status, to_account_id) 
                                    VALUES (%s, %s, %s, %s, %s, %s) """
                    self.cursor.execute(txn_query, (account_id, transaction_type, amount, remarks, "Failed", to_account_id))
                    self.conn.commit()
                    print("Transaction failed: Insufficient balance")
                    return False

                # Record successful transaction
                txn_query = """ INSERT INTO Transactions (account_id, type, amount, remarks, status, to_account_id) 
                                VALUES (%s, %s, %s, %s, %s, %s) """
                self.cursor.execute(txn_query, (account_id, transaction_type, amount, remarks, "Success", to_account_id))

                if transaction_type == "Deposit":
                    update_balance_query = "UPDATE Account SET balance = balance + %s WHERE account_id = %s"
                    self.cursor.execute(update_balance_query, (amount, account_id))

                elif transaction_type == "Withdraw":
                    update_balance_query = "UPDATE Account SET balance = balance - %s WHERE account_id = %s"
                    self.cursor.execute(update_balance_query, (amount, account_id))

                elif transaction_type == "Payment":
                    update_balance_query = "UPDATE Account SET balance = balance - %s WHERE account_id = %s"
                    self.cursor.execute(update_balance_query, (amount, account_id))

                else:  # Transfer
                    sender_balance_query = "UPDATE Account SET balance = balance - %s WHERE account_id = %s"
                    receiver_balance_query = "UPDATE Account SET balance = balance + %s WHERE account_id = %s"
                    self.cursor.execute(sender_balance_query, (amount, account_id))
                    self.cursor.execute(receiver_balance_query, (amount, to_account_id))

                self.conn.commit()
                print(transaction_type)
                update_analytics(account_id,transaction_type,amount)
                print("Transaction successful")
                return True

            except Exception as e:
                self.conn.rollback()
                print("Error from transaction", e)
                return False

            finally:
                self.cursor.close()
                self.conn.close()
        else:
            print("Transaction failed: Cannot transfer to the same account")
            self.cursor.close()
            self.conn.close()
            return False