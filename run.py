from app import app, db


# ✅ create tables on first run
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
