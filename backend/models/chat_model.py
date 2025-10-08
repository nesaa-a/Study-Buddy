from backend.config.db_config import get_db_connection

def save_chat_message(user_id, message, response):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO chat_history (user_id, message, response) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, message, response))
    connection.commit()
    cursor.close()
    connection.close()

def get_chat_history(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chat_history WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
    chats = cursor.fetchall()
    cursor.close()
    connection.close()
    return chats
