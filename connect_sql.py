import pyodbc

# Step 3: Connection string
server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_AUkenna'
username = 'AUkenna'
password = 'StlK188+'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=Yes;"
    "TrustServerCertificate=Yes;"
    "Connection Timeout=30;"
    "Trusted_Connection=No;"
)

try:
    # Step 4: Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")

    # Step 5: Create table and insert data
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INT PRIMARY KEY,
            name NVARCHAR(50),
            age INT
        )
    ''')
    cursor.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (1, 'Alice', 30))
    cursor.execute('INSERT INTO users (id, name, age) VALUES (?, ?, ?)', (2, 'Bob', 25))
    conn.commit()
    print("Data inserted successfully.")

    # Step 6: Fetch and print data
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

finally:
    # Step 7: Close connection
    cursor.close()
    conn.close()
    print("Connection closed.")
