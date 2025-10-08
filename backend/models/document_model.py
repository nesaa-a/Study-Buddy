from backend.config.db_config import get_db_connection

def save_document(user_id, title, file_path):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO documents (user_id, title, file_path) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, title, file_path))
    connection.commit()
    cursor.close()
    connection.close()

def get_user_documents(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documents WHERE user_id = %s", (user_id,))
    docs = cursor.fetchall()
    cursor.close()
    connection.close()
    return docs
