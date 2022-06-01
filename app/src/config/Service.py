import mysql.connector


class Service:
    @staticmethod
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
            print('MySQL Database connection unsuccessful')
        return db

    builder = create_server()
