import pandas as pd
import requests
from app.src.config.Service import *
import re


class InitApp:
    @staticmethod
    def drop_table():
        try:
            cursor = builder.cursor()
            delete_project = '''DROP TABLE IF EXISTS Projects;'''
            cursor.execute(delete_project)
            delete_project_material = '''DROP TABLE IF EXISTS ProjectMaterials;'''
            cursor.execute(delete_project_material)
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

    # User_Entity
    @staticmethod
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
              INSERT INTO Users (`user_id`,`role`,`status`) VALUES (NULL ,'contractor', 1),(NULL ,'contractor', 0);
              '''
            cursor.execute(insert_user)
            builder.commit()
            print('Created User')
        except:
            print('Create fail')

    # Contractor_Entity
    @staticmethod
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
              INSERT INTO Contractors (`contractor_id`,`first_name`,`last_name`,`email`,`password`,`active`,`user_id`) VALUES (NULL ,'kong','paingjai','kong@gmail.com','kong1234',1, 1),(NULL ,'fax','phonmongkhon','fax@gmail.com','fax1234',0, 2);
              '''
            cursor.execute(insert_contractor)
            builder.commit()
            print('Created Contractor')
        except:
            print('Create fail')

    # Material_Entity
    @staticmethod
    def build_table_material():
        try:
            cursor = builder.cursor()
            material = '''
                     CREATE TABLE Materials (
                     material_id INT AUTO_INCREMENT PRIMARY KEY,
                     material_name VARCHAR(255) ,
                     material_price VARCHAR(255),
                     material_unit VARCHAR(255),
                     material_category VARCHAR(255),
                     material_type VARCHAR(255))
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
            #clean_data
            # df.dropna(inplace=True)
            # df.drop(df.index[14:37], inplace=True)
            # df[4] = df[1].str.find('ขนาด')
            # select_size = df.loc[df[4] >= 1]
            # index = select_size[0]
            # data = select_size[1]
            # size = []
            # pattern = ".*" + 'ขนาด'
            # for i in data:
            #     word = str(i)
            #     strValue = re.sub(pattern, '', word)
            #     size.append(strValue)

            material_name = df[1].to_numpy()
            material_unit = df[2].to_numpy()
            material_price = df[3].to_numpy()
            n = len(material_name) - 1
            insert_material = '''
                           INSERT INTO Materials (`material_name`,`material_price`,`material_unit`,`material_category`) VALUES (%s,%s,%s,%s);
                           '''
            for i in range(1, n, 1):
                val_name = str(material_name[i])
                val_unit = str(material_unit[i])
                val_price = str(material_price[i])
                val_category = 'building_material'
                cursor.execute(insert_material, (val_name, val_price, val_unit, val_category))

            # delete_phase
            sql_delete_materials = '''DELETE FROM Materials   WHERE material_id = %s'''
            for i in range(14, 42, 1):
                cursor.execute(sql_delete_materials, (i,))
            for i in range(53, 55, 1):
                cursor.execute(sql_delete_materials, (i,))
            for i in range(119, 127, 1):
                cursor.execute(sql_delete_materials, (i,))

            # update_phase
            sql_update_material_category = '''UPDATE Materials SET material_category = %s  WHERE material_id = %s'''
            for i in range(1, 14, 1):
                cursor.execute(sql_update_material_category, ('building_material', i))

            # cursor = builder.cursor()
            builder.commit()
            print('Created Material')
        except:
            print('Create fail')

    # ProjectMaterial_Entity
    @staticmethod
    def build_table_project_material():
        try:
            cursor = builder.cursor()
            project_material = '''
                         CREATE TABLE ProjectMaterials (
                         project_material_id INT AUTO_INCREMENT PRIMARY KEY,
                         project_material_name VARCHAR(255) NOT NULL,
                         project_material_price VARCHAR(255) NOT NULL
                        )
                         '''
            cursor.execute(project_material)
            insert_project_material = '''
                      INSERT INTO `ProjectMaterials` ( `project_material_id`,`project_material_name`,`project_material_price`) VALUES (NULL ,'คอนกรีตผสมเสร็จรูปลูกบาศก์ 180 กก./ตร.ซม. และ รูปทรงกระบอก 140กก./ตร.ซม. ตราซีแพค','1794.39');
                      '''
            cursor.execute(insert_project_material)
            builder.commit()
            print('Created ProjectMaterial')
        except:
            print('Create fail')

    # Project_Entity
    @staticmethod
    def build_table_project():
        try:
            cursor = builder.cursor()
            project = '''
                     CREATE TABLE Projects (
                     project_id INT AUTO_INCREMENT PRIMARY KEY,
                     project_name VARCHAR(255) NOT NULL,
                     project_description VARCHAR(1000) NOT NULL,
                     customer_name VARCHAR(255) NOT NULL,
                     date_line DATE NOT NULL,
                     contractor_id INT, FOREIGN KEY (contractor_id) REFERENCES Contractors(contractor_id)ON DELETE  CASCADE ON UPDATE CASCADE,
                     project_material_id INT, FOREIGN KEY (project_material_id) REFERENCES ProjectMaterials(project_material_id)ON DELETE  CASCADE ON UPDATE CASCADE)
                     '''
            cursor.execute(project)
            insert_contractor = '''
                    INSERT INTO `Projects` ( `project_id`,`project_name`,`project_description`,`customer_name`,`date_line`,`contractor_id`,`project_material_id`) VALUES (NULL ,'project I','project I is for testing project card','oat','2022-12-25', 1,1);
                    '''
            cursor.execute(insert_contractor)
            builder.commit()
            print('Created Project')
        except:
            print('Create fail')


InitApp.drop_table()
InitApp.build_table_user()
InitApp.build_table_contractor()
InitApp.build_table_material()
InitApp.build_table_project_material()
InitApp.build_table_project()
