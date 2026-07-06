import sqlite3


DB_PATH = "data/procurement.db"


def save_request(request):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO procurement_requests
    (
        request_id,
        part_id,
        part_name,
        current_stock,
        recommended_order,
        ordered_quantity,
        supplier_name,
        supplier_email,
        ai_analysis,
        status,
        manager_instructions,
        risk_level,
        supplier_status,
        expected_delivery_date,
        supplier_response
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        request.request_id,

        request.part_id,
        request.part_name,

        request.current_stock,
        request.recommended_order,

        # Initially 0
        0,

        request.supplier_name,
        request.supplier_email,

        request.ai_analysis,

        request.status,

        request.manager_instructions,

        request.risk_level,

        "PENDING",

        None,

        None
    ))

    conn.commit()
    conn.close()


def get_request(request_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM procurement_requests
    WHERE request_id = ?
    """, (request_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {

        "request_id": row[0],

        "part_id": row[1],
        "part_name": row[2],

        "current_stock": row[3],

        "recommended_order": row[4],

        "ordered_quantity": row[5],

        "supplier_name": row[6],
        "supplier_email": row[7],

        "ai_analysis": row[8],

        "status": row[9],

        "manager_instructions": row[10],

        "risk_level": row[11],

        "supplier_status": row[12],

        "expected_delivery_date": row[13],

        "supplier_response": row[14],

        "created_at": row[15]
    }


def update_status(request_id, status):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE procurement_requests
    SET status = ?
    WHERE request_id = ?
    """, (status, request_id))

    conn.commit()
    conn.close()


def update_manager_instructions(
    request_id,
    instructions
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE procurement_requests
    SET manager_instructions = ?
    WHERE request_id = ?
    """, (

        instructions,
        request_id

    ))

    conn.commit()
    conn.close()


def update_ordered_quantity(
    request_id,
    ordered_quantity
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE procurement_requests
    SET ordered_quantity = ?
    WHERE request_id = ?
    """, (

        ordered_quantity,
        request_id

    ))

    conn.commit()
    conn.close()


def update_supplier_response(
    request_id,
    supplier_status,
    expected_delivery_date,
    supplier_response
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE procurement_requests
    SET
        supplier_status = ?,
        expected_delivery_date = ?,
        supplier_response = ?
    WHERE request_id = ?
    """, (

        supplier_status,
        expected_delivery_date,
        supplier_response,
        request_id

    ))

    conn.commit()
    conn.close()