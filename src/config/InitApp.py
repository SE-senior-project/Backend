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
        print('MySQL Database connection unsuccessful')
    return db


builder = create_server()


def drop_table():
    cursor = builder.cursor()
    delete_contractor = '''DROP TABLE IF EXISTS Contractors;'''
    cursor.execute(delete_contractor)
    delete_user = '''DROP TABLE IF EXISTS Users;'''
    cursor.execute(delete_user)
    builder.commit()


drop_table()


# User_Entity
def build_table_user():
    cursor = builder.cursor()
    delete_user = '''DROP TABLE IF EXISTS Users;'''
    cursor.execute(delete_user)
    user = '''
        CREATE TABLE Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY ,
        role VARCHAR(255) NOT NULL,
        status BIT NOT NULL
        )
        '''
    cursor.execute(user)
    insert_user = '''
      INSERT INTO `Users` ( `user_id`,`role`,`status`) VALUES (NULL ,'contractor', 1),(NULL ,'contractor', 0);
      '''
    cursor.execute(insert_user)
    builder.commit()


build_table_user()


# Contractor_Entity
def build_table_contractor():
    cursor = builder.cursor()
    contractor = '''
            CREATE TABLE Contractors (
            contractor_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            user_id INT,
            CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ON DELETE  CASCADE
            ON UPDATE CASCADE 
            )
            '''
    cursor.execute(contractor)

    insert_contractor = '''
      INSERT INTO `Contractors` ( `contractor_id`,`first_name`,`last_name`,`email`,`password`,`user_id`) VALUES (NULL ,'kong','paingjai','kong@gmail.com','kong1234', 1),(NULL ,'fax','phonmongkhon','fax@gmail.com','fax1234', 2);
      '''
    cursor.execute(insert_contractor)
    builder.commit()


build_table_contractor()
