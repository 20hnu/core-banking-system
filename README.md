

#  Core Banking System with Analytics

This project is a prototype of a **Core Banking System** developed in **Python** using . It connects to a **MySQL** database using **PyMySQL** and supports authentication, transaction handling, and analytical reporting for account activities using **Streamlit**.

---

## Features

- User registration and authentication
- Password-protected login
- Account management (Savings, Current, Fixed)
- Transactions: Deposit, Withdrawal, Transfer, Payment
- Analytics table to track and summarize transactional activity
- Database connectivity using PyMySQL

---

## 🗃 Database Tables

1. `Customers`
2. `Account`
3. `Transactions`
4. `Analytics`
5. `Authenticate`

---

## Project Structure
- **`db/`**: Handles DB connectivity.
- **`models/`**: Contains all core banking features.
- **`dashboard/`**: Streamlit app for visualizing analytics and metrics.
- **`main.py`**: Provides CLI-based interaction for login and transactions.
- **`requirements.txt`**: Useful to install dependencies using.

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/20hnu/core-banking-system.git
   cd core-banking-system
   ```
2. Create Virtual Environment
   ##### For Linux/macOS
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    
##### For Windows

    python -m venv venv
    .\venv\Scripts\activate
    
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run Program 
    ```
    python3 main.py
    ```

5. Open dashboard
    ```
    streamlit run dashboard.py
    ```

## Entity Relationship Diagram

![Alt Text](https://github.com/20hnu/core-banking-system/blob/main/dbconnect/modified_erd_banking_system.png?raw=true)

## Data Flow Diagram
1. Level 0 DFD
![Will be posted soon](https://github.com/20hnu/core-banking-system/blob/main/dbconnect/dfd_banking_system_lvl0.png?raw=true)

2. Level 1 DFD

![Will be posted soon](https://github.com/20hnu/core-banking-system/blob/main/dbconnect/dbconnect/dbconnect/dfd_banking_system_lvl1.png?raw=true)

## Dashboard 
![Will be posted soon](https://github.com/20hnu/core-banking-system/blob/main/dbconnect/dashboard_Sample.png?raw=true)

## SQL Code for creating database
```sql

create table Customers (
customer_id int primary key auto_increment,
first_name varchar(50) NOT NULL,
middle_name varchar(50),
last_name varchar(50) NOT NULL,
email varchar(50) UNIQUE NOT NULL,
phone_number varchar(10) NOT NULL,
dob DATE,
created_at DATETIME default current_timestamp,
deleted_at DATETIME
);

create table Account (
account_id int primary key auto_increment,
customer_id int NOT NULL,
account_type ENUM('Savings', 'Current','Fixed') NOT NULL, 
account_number VARCHAR(30) UNIQUE NOT NULL,
balance DECIMAl(12,2) default 0.00,
status ENUM('Active', 'Closed', 'Suspended') default 'Active',
opened_at DATETIME DEFAULT current_timestamp,
last_activity DATETIME DEFAULT current_timestamp,
foreign key (customer_id) References Customers(customer_id)
	ON DELETE cascade on update cascade
);


create table Transactions(
transaction_id int primary key auto_increment,
account_id int NOT NULL,
type ENUM('Deposit', 'Withdraw','Transfer', 'Payment') NOT NULL,
amount decimal(12,2) NOT NULL,
remarks Varchar(255),
status ENUM('Success','Pending', 'Failed') DEFAULT 'Success',
transaction_time DATETIME DEFAULT current_timestamp,
to_account_id INT DEFAULT NULL,
FOREIGN KEY (account_id) references Account(account_id)
on delete cascade on update cascade,    
FOREIGN KEY (to_account_id) references Account(account_id)
on delete set null on update cascade
);
 
Create table Analytics (
	analytics_id int auto_increment primary key,
    account_id int not null,
    date DATE not null,
    total_transaction INT default 0,
    total_amount decimal(12,2) default 0.00,
    average_amount decimal(12,2) default 0.00,
    
    deposit_count int default 0,
    withdrawal_count int default 0,
    transfer_count int default 0,
    payment_count int default 0,
    
    last_updated datetime default current_timestamp on update current_timestamp,
    
    foreign key (account_id) references Account(account_id)
    on delete cascade on update cascade
);

create table Authenticate (
	auth_id int primary key auto_increment,
    customer_id int not null unique,
    username varchar(10) unique not null,
    password varchar(8) not null,
    created_at datetime default current_timestamp,
    last_login datetime,
    Foreign Key (customer_id) REFERENCES Customers(customer_id)
    on delete cascade on update cascade
);
```

