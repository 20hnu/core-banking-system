from db.db_config import get_connection

class Customer:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
    

    def open_account(self, customer_details,account_details, authenticate_details):
        first_name = customer_details["first_name"]
        middle_name = customer_details["middle_name"]
        last_name = customer_details["last_name"]
        email = customer_details["email"]
        phone_number = customer_details["phone_number"]
        dob = customer_details["dob"]

        username = authenticate_details["username"]
        password = authenticate_details["password"]

        try:
            # insert customer
            query = """Insert into Customers (first_name, middle_name, last_name, email, phone_number, dob)
            values (%s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(query,(first_name, middle_name, last_name, email, phone_number, dob))
            new_cust_id = self.cursor.lastrowid
            print("New customer added",new_cust_id)

            # set username and password
            query = "Insert into Authenticate (customer_id, username, password) values (%s, %s, %s)"
            self.cursor.execute(query,(new_cust_id, username, password))
            print("New user authentication added",new_cust_id)

            # insert account information
            query = "Insert into Account (customer_id, account_type,account_number, balance,status) values (%s, %s, %s, %s, %s)"
            self.cursor.execute(query,(new_cust_id, account_details["account_type"], account_details["account_number"], account_details["balance"],"Active"))
            self.conn.commit()
            print("New account added",new_cust_id)

            return True 
        
        except Exception as e:
            self.conn.rollback()
            print("Error: ", e)
            return False

    def login(self,user_name,password):
        try:
            query = "SELECT customer_id FROM Authenticate WHERE username = %s AND password = %s"
            self.cursor.execute(query, (user_name, password))

            user = self.cursor.fetchone()
            print("login success",user)
            return user
        except Exception as e:
            print("Error:",e)
            return False