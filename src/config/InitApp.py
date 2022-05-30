import mysql.connector
import requests
import pandas as pd


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
    try:
        cursor = builder.cursor()
        delete_contractor = '''DROP TABLE IF EXISTS Contractors;'''
        cursor.execute(delete_contractor)
        delete_user = '''DROP TABLE IF EXISTS Users;'''
        cursor.execute(delete_user)
        delete_material = '''DROP TABLE IF EXISTS Materials;'''
        cursor.execute(delete_material)
        builder.commit()
        print('Already droup')
    except:
        print('Droup fail')


drop_table()


# User_Entity
def build_table_user():
    try:
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
        print('Created User')
    except:
        print('Create fail')


build_table_user()


# Contractor_Entity
def build_table_contractor():
    try:
        cursor = builder.cursor()
        contractor = '''
                CREATE TABLE Contractors (
                contractor_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                active BIT NOT NULL,
                user_id INT,
                CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id)
                ON DELETE  CASCADE
                ON UPDATE CASCADE 
                )
                '''
        cursor.execute(contractor)

        insert_contractor = '''
          INSERT INTO `Contractors` ( `contractor_id`,`first_name`,`last_name`,`email`,`password`,`active`,`user_id`) VALUES (NULL ,'kong','paingjai','kong@gmail.com','kong1234',1, 1),(NULL ,'fax','phonmongkhon','fax@gmail.com','fax1234',0, 2);
          '''
        cursor.execute(insert_contractor)
        builder.commit()
        print('Created Contractor')
    except:
        print('Create fail')


build_table_contractor()


# Material_Entity
def build_table_material():
    try:
        cursor = builder.cursor()
        material = '''
                 CREATE TABLE Materials (
                 material_id INT AUTO_INCREMENT PRIMARY KEY,
                 material_name VARCHAR(255) ,
                 material_price VARCHAR(255),
                 material_unit VARCHAR(255) )
                 '''
        cursor.execute(material)
        url = 'http://www.indexpr.moc.go.th/PRICE_PRESENT/table_month_regionCsi.asp'
        payload = {
            'DDMonth': '04',
            'DDYear': '2565',
            'DDProvince': '50',
            'texttable': 'csi_price_north_web_avg',
            'text_name': 'unit_code_N',
            'B1': '%B5%A1%C5%A7'
        }
        r = requests.post(url, data=payload).content
        df = pd.read_html(r)[0]
        material_name = df[1].to_numpy()
        material_unit = df[2].to_numpy()
        material_price = df[3].to_numpy()
        n = len(material_name) - 1
        insert_material = '''
                       INSERT INTO `Materials` (`material_name`,`material_price`,`material_unit`) VALUES (%s,%s,%s);
                       '''
        for i in range(1, n, 1):
            val_name = str(material_name[i])
            val_unit = str(material_unit[i])
            val_price = str(material_price[i])
            cursor.execute(insert_material, (val_name, val_price, val_unit))
        builder.commit()
        print('Created Material')
    except:
        print('Create fail')


build_table_material()

# ProjectMaterial_Entity
# def build_table_project_material():
#     cursor = builder.cursor()
#     project_material = '''
#              CREATE TABLE ProjectMaterials (
#              material_id INT AUTO_INCREMENT PRIMARY KEY,
#              material_name VARCHAR(255) NOT NULL,
#              material_price INT NOT NULL,
#              )
#              '''
#     cursor.execute(project_material)
#     builder.commit()
