from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# Initialize Flask app
app = Flask(__name__)

# Database connection details
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=dist-6-505.uopnet.plymouth.ac.uk;"
    "DATABASE=COMP2001_AUkenna;"
    "UID=AUkenna;"
    "PWD=StlK188+;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Trusted_Connection=no;"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Test connection
try:
    with app.app_context():
        # Run a simple query to verify the connection
        db.session.execute(text("SELECT 1"))
        print("SQLAlchemy connection successful!")
except Exception as e:
    print(f"Error: {e}")
