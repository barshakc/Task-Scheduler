from db.database import engine

try:
    conn = engine.connect()
    print("Connected to PostgreSQL successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
