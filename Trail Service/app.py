from config import connex_app, db

connex_app.add_api("swagger.yml")

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=8000)
