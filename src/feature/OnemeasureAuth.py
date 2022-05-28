from src.config.InitApp import *
import json


def Login_user(email, password):
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
