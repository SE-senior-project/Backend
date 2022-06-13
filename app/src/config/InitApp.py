import pandas as pd
import requests
from app.src.config.Service import *
import hashlib


class InitApp:
    @staticmethod
    def drop_table():
        try:
            cursor = builder.cursor()
            delete_project_material = '''DROP TABLE IF EXISTS ProjectMaterials;'''
            cursor.execute(delete_project_material)
            delete_project = '''DROP TABLE IF EXISTS Projects;'''
            cursor.execute(delete_project)
            delete_admin = '''DROP TABLE IF EXISTS Admins;'''
            cursor.execute(delete_admin)
            delete_contractor = '''DROP TABLE IF EXISTS Contractors;'''
            cursor.execute(delete_contractor)
            delete_user = '''DROP TABLE IF EXISTS Users;'''
            cursor.execute(delete_user)
            delete_material = '''DROP TABLE IF EXISTS Materials;'''
            cursor.execute(delete_material)
            builder.commit()
            print('Already drop all tables')
        except:
            print('Fail in drop all tables')

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
              INSERT INTO Users (`user_id`,`role`,`status`) VALUES (NULL ,'admin', 1),(NULL ,'admin', 1),(NULL ,'admin', 1),(NULL ,'contractor', 1),(NULL ,'contractor', 0),(NULL ,'contractor', 1),(NULL ,'contractor', 0);
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
              INSERT INTO Contractors (`contractor_id`,`first_name`,`last_name`,`email`,`password`,`active`,`user_id`) VALUES (NULL ,'ก้อง','เปียงใจ','kong@gmail.com',%s,1, 4),(NULL ,'แฟค','พุทธิแจ่ม','fax@gmail.com',%s,1, 5),(NULL ,'โอ๊ต','สหฌาณ','oat@gmail.com',%s,0, 6),(NULL ,'ปีเตอร์','แพนนี่','peter@gmail.com',%s,1, 7);
              '''
            pass1 = 'kong1234'
            pass2 = 'fax1234'
            pass3 = 'oat1234'
            pass4 = 'peter1234'
            pass1 = hashlib.md5(pass1.encode()).hexdigest()
            pass2 = hashlib.md5(pass2.encode()).hexdigest()
            pass3 = hashlib.md5(pass3.encode()).hexdigest()
            pass4 = hashlib.md5(pass4.encode()).hexdigest()
            cursor.execute(insert_contractor, (pass1, pass2, pass3, pass4))
            builder.commit()
            print('Created Contractor')
        except:
            print('Create fail')

    # Admin_Entity
    @staticmethod
    def build_table_admin():
        try:
            cursor = builder.cursor()
            admin = '''
                       CREATE TABLE Admins (
                       admin_id INT AUTO_INCREMENT PRIMARY KEY,
                       admin_name VARCHAR(255) NOT NULL,
                       email VARCHAR(255) NOT NULL,
                       password VARCHAR(255) NOT NULL,
                       user_id INT,
                       CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id)
                       ON DELETE  CASCADE
                       ON UPDATE CASCADE 
                       )
                       '''
            cursor.execute(admin)

            insert_admin = '''
                 INSERT INTO Admins (admin_id,admin_name,email,password,user_id) VALUES (NULL ,'admin','admin@gmail.com', %s ,1),(NULL ,'admin1','admin_1@gmail.com', %s ,2),(NULL ,'admin2','admin_2@gmail.com', %s ,3);
                 '''
            admin_pass = 'admin1234'
            admin_pass = hashlib.md5(admin_pass.encode()).hexdigest()
            val = (admin_pass, admin_pass, admin_pass)
            cursor.execute(insert_admin, val)
            builder.commit()
            print('Created Admin')
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
            df.dropna(inplace=True)
            df.drop(df.index[14:37], inplace=True)
            df.drop(df.index[27:29], inplace=True)
            df.drop(df.index[91:100], inplace=True)
            # clean_data
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
            n = len(material_name)
            insert_material = '''
                           INSERT INTO Materials (`material_name`,`material_price`,`material_unit`) VALUES (%s,%s,%s);
                           '''
            for i in range(1, n, 1):
                val_name = str(material_name[i])
                val_unit = str(material_unit[i])
                val_price = str(material_price[i])
                cursor.execute(insert_material, (val_name, val_price, val_unit))
            # update_category_phase
            sql_update_material_category = '''UPDATE Materials SET material_category = %s  WHERE material_id = %s'''
            for i in range(1, n, 1):
                if 1 <= i <= 13:
                    cursor.execute(sql_update_material_category, ('building_material', i))
                if 14 <= i <= 22:
                    cursor.execute(sql_update_material_category, ('steel', i))
                if 23 <= i <= 26:
                    cursor.execute(sql_update_material_category, ('roof_ceiling', i))
                if 27 <= i <= 31:
                    cursor.execute(sql_update_material_category, ('steel', i))
                if 32 <= i <= 40:
                    cursor.execute(sql_update_material_category, ('electrical', i))
                if 41 <= i <= 90:
                    cursor.execute(sql_update_material_category, ('water_supply_pipes_fittings', i))
                if 91 <= i <= 103:
                    cursor.execute(sql_update_material_category, ('roof_ceiling', i))
                if 104 <= i <= 106:
                    cursor.execute(sql_update_material_category, ('wood', i))
                if 107 <= i <= 110:
                    cursor.execute(sql_update_material_category, ('roof_ceiling', i))
                if 111 <= i <= 113:
                    cursor.execute(sql_update_material_category, ('flooring_materials', i))
                if 114 <= i <= 115:
                    cursor.execute(sql_update_material_category, ('glass', i))
                if 116 <= i <= 117:
                    cursor.execute(sql_update_material_category, ('roof_ceiling', i))
                if 118 <= i <= 120:
                    cursor.execute(sql_update_material_category, ('flooring_materials', i))
                if 121 <= i <= 124:
                    cursor.execute(sql_update_material_category, ('building_material', i))
                if 125 <= i <= 141:
                    cursor.execute(sql_update_material_category, ('wood', i))
                if 142 <= i <= 153:
                    cursor.execute(sql_update_material_category, ('color_lacquer', i))
                if 154 <= i <= 163:
                    cursor.execute(sql_update_material_category, ('door_window', i))
                if 164 <= i <= 167:
                    cursor.execute(sql_update_material_category, ('steel', i))
                if 168 <= i <= 170:
                    cursor.execute(sql_update_material_category, ('door_window', i))
                if 171 <= i <= 173:
                    cursor.execute(sql_update_material_category, ('building_material', i))
                if i == 174:
                    cursor.execute(sql_update_material_category, ('color_lacquer', i))
                if 175 <= i <= 176:
                    cursor.execute(sql_update_material_category, ('water_supply_pipes_fittings', i))
                if 177 <= i <= 189:
                    cursor.execute(sql_update_material_category, ('building_material', i))
                if 190 <= i <= 195:
                    cursor.execute(sql_update_material_category, ('water_supply_pipes_fittings', i))
                if 196 <= i <= 201:
                    cursor.execute(sql_update_material_category, ('electrical', i))
                if 202 <= i <= 212:
                    cursor.execute(sql_update_material_category, ('water_supply_pipes_fittings', i))
            # update_type_phase
            sql_update_material_type = '''UPDATE Materials SET material_type = %s  WHERE material_id = %s'''
            for i in range(1, n, 1):
                if 1 <= i <= 11:
                    cursor.execute(sql_update_material_type, ('concrete', i))
                if 12 <= i <= 13:
                    cursor.execute(sql_update_material_type, ('brick', i))
                if 14 <= i <= 15:
                    cursor.execute(sql_update_material_type, ('sr_steel', i))
                if 16 <= i <= 19:
                    cursor.execute(sql_update_material_type, ('sd_steel', i))
                if i == 20:
                    cursor.execute(sql_update_material_type, ('steel_binding_wire', i))
                if 21 <= i <= 22:
                    cursor.execute(sql_update_material_type, ('angle_iron', i))
                if 23 <= i <= 26:
                    cursor.execute(sql_update_material_type, ('light_lip_channel_steel', i))
                if 27 <= i <= 31:
                    cursor.execute(sql_update_material_type, ('hollow_steel_tubing', i))
                if 32 <= i <= 40:
                    cursor.execute(sql_update_material_type, ('bs-m', i))
                if 41 <= i <= 46:
                    cursor.execute(sql_update_material_type, ('steel_fitting', i))
                if 47 <= i <= 49:
                    cursor.execute(sql_update_material_type, ('pipe_steel_fitting', i))
                if 50 <= i <= 65:
                    cursor.execute(sql_update_material_type, ('pvc_pipe', i))
                if 66 <= i <= 90:
                    cursor.execute(sql_update_material_type, ('pvc_fitting', i))
                if i == 91:
                    cursor.execute(sql_update_material_type, ('heat_insulation', i))
                if 92 <= i <= 103:
                    cursor.execute(sql_update_material_type, ('thatched', i))
                if 104 <= i <= 106:
                    cursor.execute(sql_update_material_type, ('rubber_veneer', i))
                if 107 <= i <= 110:
                    cursor.execute(sql_update_material_type, ('gypsum_board', i))
                if 111 <= i <= 113:
                    cursor.execute(sql_update_material_type, ('black_flat_steel', i))
                if 114 <= i <= 115:
                    cursor.execute(sql_update_material_type, ('clear_glass', i))
                if 116 <= i <= 117:
                    cursor.execute(sql_update_material_type, ('thatched', i))
                if 118 <= i <= 120:
                    cursor.execute(sql_update_material_type, ('glazed_floor_tiles', i))
                if 121 <= i <= 124:
                    cursor.execute(sql_update_material_type, ('glazed_wall_tiles', i))
                if 125 <= i <= 128:
                    cursor.execute(sql_update_material_type, ('teng_wood', i))
                if 129 <= i <= 132:
                    cursor.execute(sql_update_material_type, ('dang_wood', i))
                if 133 <= i <= 137:
                    cursor.execute(sql_update_material_type, ('yang_wood', i))
                if 138 <= i <= 141:
                    cursor.execute(sql_update_material_type, ('ka_bak_wood', i))
                if i == 142:
                    cursor.execute(sql_update_material_type, ('glaze_oil', i))
                if 143 <= i <= 144:
                    cursor.execute(sql_update_material_type, ('interior', i))
                if 145 <= i <= 146:
                    cursor.execute(sql_update_material_type, ('exterior', i))
                if 147 <= i <= 149:
                    cursor.execute(sql_update_material_type, ('foundation', i))
                if 150 <= i <= 151:
                    cursor.execute(sql_update_material_type, ('glaze_oil ', i))
                if 152 <= i <= 153:
                    cursor.execute(sql_update_material_type, ('lacquer', i))
                if 154 <= i <= 157:
                    cursor.execute(sql_update_material_type, ('teak_plywood', i))
                if 158 <= i <= 161:
                    cursor.execute(sql_update_material_type, ('rubber_plywood', i))
                if 162 <= i <= 163:
                    cursor.execute(sql_update_material_type, ('jamb', i))
                if 164 <= i <= 167:
                    cursor.execute(sql_update_material_type, ('nail', i))
                if 168 <= i <= 169:
                    cursor.execute(sql_update_material_type, ('window_hinge', i))
                if i == 170:
                    cursor.execute(sql_update_material_type, ('door_lock', i))
                if 171 <= i <= 172:
                    cursor.execute(sql_update_material_type, ('mortar', i))
                if i == 173:
                    cursor.execute(sql_update_material_type, ('flint_coat', i))
                if i == 174:
                    cursor.execute(sql_update_material_type, ('lacquer', i))
                if 175 <= i <= 176:
                    cursor.execute(sql_update_material_type, ('bonding_agent', i))
                if 177 <= i <= 178:
                    cursor.execute(sql_update_material_type, ('sand', i))
                if 179 <= i <= 180:
                    cursor.execute(sql_update_material_type, ('fine_sand', i))
                if 181 <= i <= 185:
                    cursor.execute(sql_update_material_type, ('rock', i))
                if i == 186:
                    cursor.execute(sql_update_material_type, ('sand', i))
                if 187 <= i <= 189:
                    cursor.execute(sql_update_material_type, ('stone', i))
                if 190 <= i <= 192:
                    cursor.execute(sql_update_material_type, ('tap', i))
                if 193 <= i <= 195:
                    cursor.execute(sql_update_material_type, ('tank', i))
                if i == 196:
                    cursor.execute(sql_update_material_type, ('electric_wire', i))
                if i == 197:
                    cursor.execute(sql_update_material_type, ('cable', i))
                if i == 198:
                    cursor.execute(sql_update_material_type, ('breaker', i))
                if 199 <= i <= 201:
                    cursor.execute(sql_update_material_type, ('light_bulb', i))
                if 202 <= i <= 205:
                    cursor.execute(sql_update_material_type, ('wc', i))
                if 206 <= i <= 207:
                    cursor.execute(sql_update_material_type, ('basin', i))
                if 208 <= i <= 210:
                    cursor.execute(sql_update_material_type, ('dish_soap ', i))
                if 211 <= i <= 212:
                    cursor.execute(sql_update_material_type, ('toilet_paper_holder', i))

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
                         project_material_price FLOAT,
                         project_id INT, FOREIGN KEY (project_id) REFERENCES Projects(project_id)ON DELETE  CASCADE ON UPDATE CASCADE
                        )
                         '''
            cursor.execute(project_material)
            insert_project_material = '''
                      INSERT INTO `ProjectMaterials` ( `project_material_id`,`project_material_name`,`project_material_price`,`project_id`) VALUES (NULL ,'คอนกรีตผสมเสร็จรูปลูกบาศก์ 180 กก./ตร.ซม. และ รูปทรงกระบอก 140กก./ตร.ซม. ตราซีแพค',1794.39, 1);
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
                     deadline DATE NOT NULL,
                     contractor_id INT, FOREIGN KEY (contractor_id) REFERENCES Contractors(contractor_id)ON DELETE  CASCADE ON UPDATE CASCADE)
                     '''
            cursor.execute(project)
            insert_contractor = '''
                    INSERT INTO `Projects` ( `project_id`,`project_name`,`project_description`,`customer_name`,`deadline`,`contractor_id`) VALUES (NULL ,'project I','project I is for testing project card','oat','2022-12-25', 1);
                    '''
            cursor.execute(insert_contractor)
            builder.commit()
            print('Created Project')
        except:
            print('Create fail')
        # Project_Entity

    @staticmethod
    def build_all_table():
        try:
            InitApp.drop_table()
            InitApp.build_table_user()
            InitApp.build_table_admin()
            InitApp.build_table_contractor()
            InitApp.build_table_material()
            InitApp.build_table_project()
            InitApp.build_table_project_material()
            # InitApp.build_table_project()
            print('Complete build all tables')
        except:
            print('uncompleted build')
