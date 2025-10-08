from backend.config.db_config import get_db_connection

def save_summary(document_id, summary_text):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO summaries (document_id, summary_text) VALUES (%s, %s)"
    cursor.execute(query, (document_id, summary_text))
    connection.commit()
    cursor.close()
    connection.close()

def get_summary_by_document(document_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM summaries WHERE document_id = %s", (document_id,))
    summary = cursor.fetchone()
    cursor.close()
    connection.close()
    return summary
