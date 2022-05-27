import mysql.connector


def create_server():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database='onemeasure'
        )
        print('MySQL Database connection successful')
    except:
        pass
    return db


builder = create_server()

def build_table():
    cursor = builder.cursor()