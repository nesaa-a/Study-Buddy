import os
from backend.config.db_config import get_db_connection

# 🧠 Save document with extracted content
def save_document(user_id, filename, file_path, content):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert with uploaded_at + content
    query = """
        INSERT INTO documents (user_id, title, file_path, content, uploaded_at)
        VALUES (%s, %s, %s, %s, NOW())
    """
    cursor.execute(query, (user_id, filename, file_path, content))
    connection.commit()
    cursor.close()
    connection.close()


# 📄 Get all documents for user
def get_user_documents(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, title AS filename, file_path, uploaded_at AS upload_date
        FROM documents
        WHERE user_id = %s
        ORDER BY uploaded_at DESC
    """
    cursor.execute(query, (user_id,))
    docs = cursor.fetchall()
    cursor.close()
    connection.close()

    for doc in docs:
        doc["file_size"] = None  # optional placeholder
    return docs


# 🧾 Get single document including text
def get_document_by_id(document_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, title AS filename, file_path, content, uploaded_at AS upload_date
        FROM documents
        WHERE id = %s AND user_id = %s
    """
    cursor.execute(query, (document_id, user_id))
    doc = cursor.fetchone()
    cursor.close()
    connection.close()
    return doc
