from src.config.InitApp import *
import json


def login_user(email, password):
    print('Email :' + str(email))
    print('Password :' + str(password))
    output = []
    prepare_output = []
    array_user_login = []
    tran_tuple = ""
    check = False
    cursor = builder.cursor()
    try:
        sql_login = '''
            SELECT Contractors.contractor_id,Contractors.first_name,Contractors.last_name,Users.role,Users.status
            FROM Contractors
            INNER JOIN Users
            ON Contractors.user_id = Users.user_id
            WHERE Contractors.email = %s 
            AND Contractors.password = %s 
        '''
        val = (email, password)
        cursor.execute(sql_login, val)
        print("Pass valid")
        result = cursor.fetchall()
        print('All data :' + str(result))
        for i in result:
            val = json.dumps(i)
            array_user_login.append(
                val.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"\r\])' + U'\xa8')))

        for list_return in array_user_login:
            tran_tuple += list_return

        array_tran = tran_tuple.split()
        for i in array_tran:
            ans = i.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%,\\!"\r\,])' + U'\xa8'))
            prepare_output.append(ans)
        check = True
        output.append(
            {
                'contractor_id': prepare_output[0],
                'first_name': prepare_output[1],
                'last_name': prepare_output[2],
                'role': prepare_output[3],
                'status': prepare_output[4],
                'check': check
            }
        )
    except:
        print("Connect fail")
        check = False
        output.append({
            'check': check
        })

    return output


def add_user():
    cursor = builder.cursor()
    try:
        sql_register = '''
              INSERT INTO `Users` ( `role`,`status`) VALUES ('contractor' ,0)
              '''
        cursor.execute(sql_register)
        builder.commit()
        print('insert pass')
    except:
        print('insert fail')


def register_user(first_name, last_name, email, password):
    print('User_Firstname :' + str(first_name))
    print('User_Lastname :' + str(last_name))
    print('User_Email :' + str(email))
    print('User_Password :' + str(password))
    add_user()
    cursor = builder.cursor()
    sql_latest_user_id = '''
              SELECT user_id
              FROM Users
              ORDER BY user_id  ASC '''
    cursor.execute(sql_latest_user_id)
    result = cursor.fetchall()
    temp = json.dumps(result[len(result) - 1])
    temp = temp.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\,!"\r\])' + U'\xa8'))
    temp = int(temp)
    print(temp)

    sql_register = '''
      INSERT INTO `Contractors` ( `first_name`,`last_name`,`email`,`password`,`user_id`) VALUES (%s ,%s ,%s ,%s ,%s)
      '''
    val = (first_name, last_name, email, password, temp)
    cursor.execute(sql_register, val)
    builder.commit()