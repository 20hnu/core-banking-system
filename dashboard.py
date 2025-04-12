import streamlit as st
import pandas as pd
import numpy as np
from dbconnect.db_config import get_connection


st.write("Dashboard For Transactions Analytics")
conn = get_connection()
curr = conn.cursor()
select_query = "SELECT * FROM Analytics"
curr.execute(select_query)
data = curr.fetchall()
st.dataframe(data)
st.bar_chart(data, x="account_id", y="total_transaction")