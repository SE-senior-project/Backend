import mysql.connector


def create_server():
    try:
        # engine = create_engine('mysql://scott:tiger@localhost/onemeasure')
        # db = SQLAlchemy
        # db = create_engine("mysql:///?User=root&Password=password&Database=onemeasure&Server=myServer&Port=3306")
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database='onemeasure'
        )
        print('MySQL Database connection successful')
    except:
        print('MySQL Database connection unsuccessful')
    return db


builder = create_server()
