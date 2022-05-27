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
    # User
    cursor = builder.cursor()
    delete_user = '''DROP TABLE IF EXISTS Users;'''
    delete_contractor = '''DROP TABLE IF EXISTS Contractors;'''
    cursor.execute(delete_contractor)
    cursor.execute(delete_user)
    user = '''
        CREATE TABLE Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        role VARCHAR(255) NOT NULL,
        status BIT NOT NULL
        )
        '''
    cursor.execute(user)

    contractor = '''
            CREATE TABLE Contractors (
            contractor_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            status BIT NOT NULL,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
            )
            '''
    cursor.execute(contractor)


build_table()


def Login_user(email, password):
    array_user = []
    output = []
    cursor = builder.cursor()
    sql = '''
        SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name FROM onemeasure.Contractors
        FROM Users
        INNER JOIN Contractors ON Contractors.user_id=Users.user_id;
        '''
    # val = (email,)
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        print(i)
    #     val = json.dumps(i)
    #     array_user.append(val.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"\r\])' + U'\xa8')))
    # 
    # print(array_user)

    # if username == 'kong' and password == '1234':
    #     check = True
    #     output.append(
    #         {
    #             'userid': array_user[len(array_user) - 1],
    #             'email': email,
    #             'password': password,
    #             'check': check
    #         }
    #     )
    #     return output
      