import mysql.connector


def create_server():
    try:
        db = mysql.connector.connect(
            host="20.219.189.82",
            user="root",
            password="password",
            database='onemeasure'
        )
        print('MySQL Database connection successful')
    except:
        print('MySQL Database connection unsuccessful')
    return db


try:
    builder = create_server()
    print('Can connect with the database')
except:
    print('Cannot connect with the database')