import pyodbc

# Database connection details
server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_AUkenna'
username = 'AUkenna'
password = 'StlK188+'
driver = '{ODBC Driver 17 for SQL Server}'

# Connection string
conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=Yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No'
)

try:
    # Establish connection
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Verify current database
    cursor.execute("SELECT DB_NAME()")
    current_db = cursor.fetchone()
    print(f"Connected to database: {current_db[0]}")

    # Verify current user
    cursor.execute("SELECT USER_NAME()")
    current_user = cursor.fetchone()
    print(f"Connected as user: {current_user[0]}")

    # Create necessary tables
    print("Creating tables...")

    cursor.execute('''
        CREATE TABLE CW2.[USER] (
            UserID INT IDENTITY(1,1) PRIMARY KEY,
            Email_Address NVARCHAR(255) NOT NULL UNIQUE,
            Role NVARCHAR(50)
        )
    ''')
    print("USER table created.")

    cursor.execute('''
        CREATE TABLE CW2.TRAIL (
            TrailID INT IDENTITY(1,1) PRIMARY KEY,
            TrailName NVARCHAR(255) NOT NULL,
            TrailSummary NVARCHAR(MAX),
            TrailDescription NVARCHAR(MAX),
            Difficulty NVARCHAR(50),
            Location NVARCHAR(255),
            Length DECIMAL(10, 2),
            ElevationGain DECIMAL(10, 2),
            RouteType NVARCHAR(100),
            OwnerID INT,
            Pt1_Lat DECIMAL(10, 6),
            Pt1_Long DECIMAL(10, 6),
            Pt1_Desc NVARCHAR(MAX),
            Pt2_Lat DECIMAL(10, 6),
            Pt2_Long DECIMAL(10, 6),
            Pt2_Desc NVARCHAR(MAX),
            FOREIGN KEY (OwnerID) REFERENCES CW2.[USER](UserID)
        )
    ''')
    print("TRAIL table created.")

    cursor.execute('''
        CREATE TABLE CW2.FEATURE (
            TrailFeatureID INT IDENTITY(1,1) PRIMARY KEY,
            TrailFeature NVARCHAR(255) NOT NULL
        )
    ''')
    print("FEATURE table created.")

    cursor.execute('''
        CREATE TABLE CW2.TRAIL_FEATURE (
            TrailID INT,
            TrailFeatureID INT,
            PRIMARY KEY (TrailID, TrailFeatureID),
            FOREIGN KEY (TrailID) REFERENCES CW2.TRAIL(TrailID),
            FOREIGN KEY (TrailFeatureID) REFERENCES CW2.FEATURE(TrailFeatureID)
        )
    ''')
    print("TRAIL_FEATURE table created.")

    # Commit the changes
    conn.commit()
    print("Tables created successfully!")

except pyodbc.Error as ex:
    print(f"An error occurred: {ex}")

finally:
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")
