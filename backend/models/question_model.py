from backend.config.db_config import get_db_connection

def add_question(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer))
    connection.commit()
    cursor.close()
    connection.close()

def get_questions_by_quiz(quiz_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions WHERE quiz_id = %s", (quiz_id,))
    questions = cursor.fetchall()
    cursor.close()
    connection.close()
    return questions
