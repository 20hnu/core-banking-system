import streamlit as st
import pandas as pd
import plotly.express as px
from dbconnect.db_config import get_connection

#account number = 123467890
st.header("Transactions Analytics")
conn = get_connection()
curr = conn.cursor()

st.subheader("Overall Transaction Summary")
stacked_query = """select date, sum(total_amount) as total_amount,sum(deposit_count) as deposit_count,sum(withdraw_count) as withdraw_count,sum(transfer_count) as transfer_count,sum(payment_count) as payment_count from 
    Analytics group by date order by date desc"""

curr.execute(stacked_query)
total_data = curr.fetchall()

if total_data:
    # Convert the fetched data in pandas dataframe and cange dtype of total_amount decimal to float
    df = pd.DataFrame(total_data, columns=['date','total_amount', 'deposit_count', 'withdraw_count','transfer_count','payment_count'])
    df['total_amount'] = df['total_amount'].astype(float)
    df['deposit_count'] = df['deposit_count'].astype(float)
    df['withdraw_count'] = df['withdraw_count'].astype(float)
    df['transfer_count'] = df['transfer_count'].astype(float)
    df['payment_count'] = df['payment_count'].astype(float)

    # Bar Chart
    fig1 = px.bar(df,x='date',y=['deposit_count','withdraw_count','transfer_count','payment_count'],title="Transaction Count per Transaction Type",template='plotly_dark')

    fig2 = px.line(df, x="date", y = "total_amount", title = "Total Transaction Amount",template='plotly_dark')

    tab1, tab2 = st.tabs(["Transaction type summary (per day)","Toatal Transaction Amount(per day)"])

    with tab1:
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.plotly_chart(fig2, use_container_width=True)

# For individual account
customer = st.text_input( "Enter account number: ")
data_query = "SELECT account_id, customer_id, balance from Account WHERE account_number = %s"
clicked = st.button("Submit")
if clicked:
    curr.execute(data_query,(customer,))
    data = curr.fetchone()
    name_query = "SELECT first_name,middle_name, last_name from Customers WHERE customer_id = %s"
    curr.execute(name_query,(data["customer_id"],))
    name = curr.fetchone()
    st.write(f"Transaction history of {name['first_name']} {name['middle_name']} {name['last_name']}")
    st.write (f"Account balance: {data['balance']}")

    transaction_query = "SELECT type, sum(amount) as total_amount,count(*) as count from Transactions WHERE account_id = %s and status = 'Success' GROUP BY type"
    curr.execute(transaction_query,(data["account_id"],))
    detail = curr.fetchall()

    #Convert the fetched data in pandas dataframe and cange dtype of total_amount decimal to float
    df = pd.DataFrame(detail, columns=['type', 'total_amount','count'])
    df['total_amount'] = df['total_amount'].astype(float)

    # Check if data exists
    if not df.empty:
        st.subheader("Transaction Summary by Type")
        
        # Bar Chart
        fig1 = px.bar(
            df,
            x='type',
            y='total_amount',
            color='type',
            title='Total Amount per Transaction Type',
            text='total_amount',
            template='plotly_dark'
        )
        fig2 = px.pie(df, values="count",names="type", title="Transaction Count by Type")

        tab1, tab2 = st.tabs(["Transaction summary","Transaction Type count"])

        with tab1:
            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("No transactions found for this account.")