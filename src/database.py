import sqlite3


DB_PATH = "data/procurement.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS procurement_requests (

        request_id TEXT PRIMARY KEY,

        part_id TEXT,
        part_name TEXT,

        current_stock INTEGER,
        recommended_order INTEGER,
        ordered_quantity INTEGER,

        supplier_name TEXT,
        supplier_email TEXT,

        ai_analysis TEXT,

        status TEXT,

        manager_instructions TEXT DEFAULT '',

        risk_level TEXT DEFAULT 'MEDIUM',

        supplier_status TEXT DEFAULT 'PENDING',

        expected_delivery_date TEXT,

        supplier_response TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()