from dbconnect.db_config import get_connection
from datetime import datetime

def update_analytics(account_id, txn_type, amount):
    try:
        date = datetime.now().date()
        conn = get_connection()
        curr = conn.cursor()
        check_row = "SELECT * from Analytics WHERE account_id = %s AND date = %s"
        curr.execute(check_row, (account_id, date))
        data = curr.fetchone()
        txn_type = "Deposit" if txn_type == 1 else ("Withdraw" if txn_type == 2 else ("Transfer" if txn_type == 3 else "Payment"))
        if data:
            update_query = f""" UPDATE Analytics
            SET 
                total_transaction = total_transaction + 1,
                total_amount = total_amount + %s,
                average_amount = (total_amount + %s)/(total_transaction + 1),
                {txn_type.lower()}_count = {txn_type.lower()}_count + 1
                WHERE account_id = %s AND date = %s
            """
            curr.execute(update_query, (amount, amount, account_id, date))
            conn.commit()

        else:
            insert_query = f""" INSERT INTO Analytics (account_id, date, total_transaction, total_amount,average_amount, {txn_type.lower()}_count)
            VALUES (%s,%s,1,%s,%s,1) """

            curr.execute(insert_query,(account_id, date, amount, amount))
            conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error from analytics:", e)
        return