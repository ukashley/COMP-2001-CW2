import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.engine import URL
import urllib.parse

# Set up Flask and Connexion app
basedir = pathlib.Path(__file__).parent.resolve()  
connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app

# Define the connection string
odbc_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=dist-6-505.uopnet.plymouth.ac.uk,1433;"
    "DATABASE=COMP2001_AUkenna;"
    "UID=AUkenna;"
    "PWD=StlK188+;"
    "TrustServerCertificate=Yes;"
    "Encrypt=Yes;"
)

connection_string = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": urllib.parse.quote_plus(odbc_str)},
)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = str(connection_string)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)