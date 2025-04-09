import pymysql
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env
host, user, password, db = os.getenv('host'), os.getenv('user'), os.getenv('password'), os.getenv('db')
def get_connection():
    return pymysql.connect(host=host, user=user, password= password, db=db, port=3306,cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    print(get_connection())