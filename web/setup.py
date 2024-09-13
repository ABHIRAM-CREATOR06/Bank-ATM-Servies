import mysql.connector as sql

# Connect to MySQL server
conn = sql.connect(host="localhost", user="root", password="1234")
if conn.is_connected():
    print("Connection to MySQL server successful")

# Create a cursor object
c1 = conn.cursor(buffered=True)  # Use buffered cursor

# Create the 'services' database if it doesn't exist
c1.execute("CREATE DATABASE IF NOT EXISTS services")

# Connect to the 'services' database
conn.database = 'services'

# Create the 'RECORDS' table
mn = '''
CREATE TABLE IF NOT EXISTS RECORDS(
    ACC_NO INT(4) PRIMARY KEY,
    PASSWORD INT(4),
    NAME VARCHAR(20) UNIQUE,
    CR_AMT INT DEFAULT 0,
    WITHDRAWL INT DEFAULT 0,
    BALANCE INT DEFAULT 0
)
'''
c1.execute(mn)

# Create the 'transfer_history' table
cursor = conn.cursor(buffered=True)  # Use buffered cursor
cursor.execute('''
CREATE TABLE IF NOT EXISTS transfer_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_acc_no INT,
    to_acc_no INT,
    amount DECIMAL(10, 2),
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create the 'withdrawal_history' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS withdrawal_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    acc_no INT,
    amount DECIMAL(10, 2),
    withdrawal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
print("Successfully set up the database and tables")


