from backend.config.db_config import get_db_connection

def create_quiz(document_id, title):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO quizzes (document_id, title) VALUES (%s, %s)"
    cursor.execute(query, (document_id, title))
    connection.commit()
    quiz_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return quiz_id

def get_quizzes_by_document(document_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quizzes WHERE document_id = %s", (document_id,))
    quizzes = cursor.fetchall()
    cursor.close()
    connection.close()
    return quizzes
