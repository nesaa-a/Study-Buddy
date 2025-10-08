import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",          
        password="12345678",  
        database="study_buddy"
    )
    return connection
