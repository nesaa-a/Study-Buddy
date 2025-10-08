from backend.config.db_config import get_db_connection

def create_user(name, email, password_hash):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, password_hash))
    connection.commit()
    cursor.close()
    connection.close()

def get_user_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user
