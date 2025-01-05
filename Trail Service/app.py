from flask import Flask
from config import connex_app
from routes.trails import trail_bp  
import logging

# Configure logging for SQLAlchemy queries
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

connex_app.add_api("swagger.yml")  
app = connex_app.app
app.register_blueprint(trail_bp, url_prefix="/api")  

if __name__ == "__main__":
    app.debug = True
    connex_app.run(host="0.0.0.0", port=8000)
