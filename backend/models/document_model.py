import os
from backend.config.db_config import get_db_connection

def save_document(user_id, filename, file_path):
    connection = get_db_connection()
    cursor = connection.cursor()

    # calculate file size
    file_size = os.path.getsize(file_path)

    # Insert with uploaded_at
    query = """
        INSERT INTO documents (user_id, title, file_path, uploaded_at)
        VALUES (%s, %s, %s, NOW())
    """
    cursor.execute(query, (user_id, filename, file_path))
    connection.commit()
    cursor.close()
    connection.close()


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

    # Add a default file_size placeholder for frontend
    for doc in docs:
        doc["file_size"] = None  # or 0 if you prefer
    return docs

