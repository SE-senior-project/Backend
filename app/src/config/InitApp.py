import pandas as pd
import requests
from app.src.config.Service import *
import hashlib


class InitApp:
    @staticmethod
    def drop_table():
        try:
            cursor = builder.cursor()
            delete_BOQ_list = '''DROP TABLE IF EXISTS BOQLists;'''
            cursor.execute(delete_BOQ_list)
            delete_BOQ = '''DROP TABLE IF EXISTS BOQs;'''
            cursor.execute(delete_BOQ)
            delete_customer_views = '''DROP TABLE IF EXISTS CustomerViews;'''
            cursor.execute(delete_customer_views)
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
            # delete_material_comparators = '''DROP TABLE IF EXISTS MaterialComparators;'''
            # cursor.execute(delete_material_comparators)
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
            material_name = df[1].to_numpy()
            material_unit = df[2].to_numpy()
            material_price = df[3].to_numpy()
            n = len(material_name)
            insert_material = '''
                           INSERT INTO Materials (`material_name`,`material_price`,`material_unit`) VALUES (%s,%s,%s);
                           '''
            for i in range(1, n, 1):
                val_name = str(material_name[i])
                val_name = val_name.translate(str.maketrans('', '', '([$\'_&+\n?@\[\]#|<>^*()%\\!"-\r\])' + U'\xa8'))
                val_unit = str(material_unit[i])
                val_price = str(material_price[i])
                cursor.execute(insert_material, (val_name, val_price, val_unit))
            # update_category_phase
            sql_update_material_category = '''UPDATE Materials SET material_category = %s  WHERE material_id = %s'''
            for i in range(1, n, 1):
                if 1 <= i <= 13:
                    cursor.execute(sql_update_material_category, ('วัสดุก่อสร้าง', i))
                if 14 <= i <= 22:
                    cursor.execute(sql_update_material_category, ('เหล็ก', i))
                if 23 <= i <= 26:
                    cursor.execute(sql_update_material_category, ('หลังคาและเพดาน', i))
                if 27 <= i <= 31:
                    cursor.execute(sql_update_material_category, ('เหล็ก', i))
                if 32 <= i <= 40:
                    cursor.execute(sql_update_material_category, ('งานไฟฟ้า', i))
                if 41 <= i <= 90:
                    cursor.execute(sql_update_material_category, ('ท่อประปาและข้อต่อ', i))
                if 91 <= i <= 103:
                    cursor.execute(sql_update_material_category, ('หลังคาและเพดาน', i))
                if 104 <= i <= 106:
                    cursor.execute(sql_update_material_category, ('ไม้', i))
                if 107 <= i <= 110:
                    cursor.execute(sql_update_material_category, ('หลังคาและเพดาน', i))
                if 111 <= i <= 113:
                    cursor.execute(sql_update_material_category, ('วัสดุปูพื้น', i))
                if 114 <= i <= 115:
                    cursor.execute(sql_update_material_category, ('กระจก', i))
                if 116 <= i <= 117:
                    cursor.execute(sql_update_material_category, ('หลังคาและเพดาน', i))
                if 118 <= i <= 120:
                    cursor.execute(sql_update_material_category, ('วัสดุปูพื้น', i))
                if 121 <= i <= 124:
                    cursor.execute(sql_update_material_category, ('วัสดุก่อสร้าง', i))
                if 125 <= i <= 141:
                    cursor.execute(sql_update_material_category, ('ไม้', i))
                if 142 <= i <= 153:
                    cursor.execute(sql_update_material_category, ('สีและอุปกรณ์ทาสี', i))
                if 154 <= i <= 163:
                    cursor.execute(sql_update_material_category, ('ประตูและหน้าต่าง', i))
                if 164 <= i <= 167:
                    cursor.execute(sql_update_material_category, ('เหล็ก', i))
                if 168 <= i <= 170:
                    cursor.execute(sql_update_material_category, ('ประตูและหน้าต่าง', i))
                if 171 <= i <= 173:
                    cursor.execute(sql_update_material_category, ('วัสดุก่อสร้าง', i))
                if i == 174:
                    cursor.execute(sql_update_material_category, ('สีและอุปกรณ์ทาสี', i))
                if 175 <= i <= 176:
                    cursor.execute(sql_update_material_category, ('ท่อประปาและข้อต่อ', i))
                if 177 <= i <= 189:
                    cursor.execute(sql_update_material_category, ('วัสดุก่อสร้าง', i))
                if 190 <= i <= 195:
                    cursor.execute(sql_update_material_category, ('ท่อประปาและข้อต่อ', i))
                if 196 <= i <= 201:
                    cursor.execute(sql_update_material_category, ('งานไฟฟ้า', i))
                if 202 <= i <= 212:
                    cursor.execute(sql_update_material_category, ('ท่อประปาและข้อต่อ', i))
            # update_type_phase
            sql_update_material_type = '''UPDATE Materials SET material_type = %s  WHERE material_id = %s'''
            for i in range(1, n, 1):
                if 1 <= i <= 11:
                    cursor.execute(sql_update_material_type, ('คอนกรีต', i))
                if 12 <= i <= 13:
                    cursor.execute(sql_update_material_type, ('อิฐ', i))
                if 14 <= i <= 15:
                    cursor.execute(sql_update_material_type, ('เหล็กผิวเรียบ', i))
                if 16 <= i <= 19:
                    cursor.execute(sql_update_material_type, ('เหล็กผิวข้ออ้อย', i))
                if i == 20:
                    cursor.execute(sql_update_material_type, ('ลวดผูกเหล็ก', i))
                if 21 <= i <= 22:
                    cursor.execute(sql_update_material_type, ('เหล็กฉาก', i))
                if 23 <= i <= 26:
                    cursor.execute(sql_update_material_type, ('เหล็กตัวซี', i))
                if 27 <= i <= 31:
                    cursor.execute(sql_update_material_type, ('ท่อเหล็กกลวง', i))
                if 32 <= i <= 40:
                    cursor.execute(sql_update_material_type, ('ท่อเหล็กเคลือบสังกะสี', i))
                if 41 <= i <= 46:
                    cursor.execute(sql_update_material_type, ('ข้อต่อเหล็ก', i))
                if 47 <= i <= 49:
                    cursor.execute(sql_update_material_type, ('ท่อสามทาง 90 องศา', i))
                if 50 <= i <= 65:
                    cursor.execute(sql_update_material_type, ('ท่อพีวีซี', i))
                if 66 <= i <= 90:
                    cursor.execute(sql_update_material_type, ('ข้อต่อท่อพีวีซี', i))
                if i == 91:
                    cursor.execute(sql_update_material_type, ('ฉนวนกันความร้อน', i))
                if 92 <= i <= 103:
                    cursor.execute(sql_update_material_type, ('มุงหลังคา', i))
                if 104 <= i <= 106:
                    cursor.execute(sql_update_material_type, ('แผ่นไม้อัดยาง', i))
                if 107 <= i <= 110:
                    cursor.execute(sql_update_material_type, ('แผ่นยิปซัม', i))
                if 111 <= i <= 113:
                    cursor.execute(sql_update_material_type, ('เหล็กแผ่นเรียบดำ', i))
                if 114 <= i <= 115:
                    cursor.execute(sql_update_material_type, ('กระจกใส', i))
                if 116 <= i <= 117:
                    cursor.execute(sql_update_material_type, ('มุงหลังคา', i))
                if 118 <= i <= 120:
                    cursor.execute(sql_update_material_type, ('กระเบื้องเคลือบปูพื้น', i))
                if 121 <= i <= 124:
                    cursor.execute(sql_update_material_type, ('กระเบื้องเคลือบบุผนัง', i))
                if 125 <= i <= 128:
                    cursor.execute(sql_update_material_type, ('ไม้เต็ง', i))
                if 129 <= i <= 132:
                    cursor.execute(sql_update_material_type, ('ไม้แดง', i))
                if 133 <= i <= 137:
                    cursor.execute(sql_update_material_type, ('ไม้ยาง', i))
                if 138 <= i <= 141:
                    cursor.execute(sql_update_material_type, ('ไม้กะบาก', i))
                if i == 142:
                    cursor.execute(sql_update_material_type, ('สีน้ำมันเคลือบ', i))
                if 143 <= i <= 144:
                    cursor.execute(sql_update_material_type, ('สีทาภายใน', i))
                if 145 <= i <= 146:
                    cursor.execute(sql_update_material_type, ('สีทาภายนอก', i))
                if 147 <= i <= 149:
                    cursor.execute(sql_update_material_type, ('สีรองพื้น', i))
                if 150 <= i <= 151:
                    cursor.execute(sql_update_material_type, ('เจลเคลือบเงา', i))
                if 152 <= i <= 153:
                    cursor.execute(sql_update_material_type, ('สารจำพวกเคลือบ', i))
                if 154 <= i <= 157:
                    cursor.execute(sql_update_material_type, ('ประตูไม้อัดสัก', i))
                if 158 <= i <= 161:
                    cursor.execute(sql_update_material_type, ('ประตูไม้อัดยาง', i))
                if 162 <= i <= 163:
                    cursor.execute(sql_update_material_type, ('วงกบ', i))
                if 164 <= i <= 167:
                    cursor.execute(sql_update_material_type, ('ตะปู', i))
                if 168 <= i <= 169:
                    cursor.execute(sql_update_material_type, ('บานพับ', i))
                if i == 170:
                    cursor.execute(sql_update_material_type, ('กลอนประตู', i))
                if 171 <= i <= 172:
                    cursor.execute(sql_update_material_type, ('ปูน', i))
                if i == 173:
                    cursor.execute(sql_update_material_type, ('ฟลิ้นโค้ท', i))
                if i == 174:
                    cursor.execute(sql_update_material_type, ('สารจำพวกเคลือบ', i))
                if 175 <= i <= 176:
                    cursor.execute(sql_update_material_type, ('น้ำยาประสาน', i))
                if 177 <= i <= 178:
                    cursor.execute(sql_update_material_type, ('ทรายหยาบ', i))
                if 179 <= i <= 180:
                    cursor.execute(sql_update_material_type, ('ทรายละเอียด', i))
                if 181 <= i <= 185:
                    cursor.execute(sql_update_material_type, ('หินย่อย', i))
                if i == 186:
                    cursor.execute(sql_update_material_type, ('ทรายหยาบ', i))
                if 187 <= i <= 189:
                    cursor.execute(sql_update_material_type, ('หิน', i))
                if 190 <= i <= 192:
                    cursor.execute(sql_update_material_type, ('ก๊อกน้ำ', i))
                if 193 <= i <= 195:
                    cursor.execute(sql_update_material_type, ('ถัง', i))
                if i == 196:
                    cursor.execute(sql_update_material_type, ('สายไฟ', i))
                if i == 197:
                    cursor.execute(sql_update_material_type, ('สายเคเบิ้ล', i))
                if i == 198:
                    cursor.execute(sql_update_material_type, ('เบรกเกอร์', i))
                if 199 <= i <= 201:
                    cursor.execute(sql_update_material_type, ('หลอดไฟ', i))
                if 202 <= i <= 205:
                    cursor.execute(sql_update_material_type, ('โถส้วม', i))
                if 206 <= i <= 207:
                    cursor.execute(sql_update_material_type, ('อ่างล้างหน้า', i))
                if 208 <= i <= 210:
                    cursor.execute(sql_update_material_type, ('ที่วางสบู่', i))
                if 211 <= i <= 212:
                    cursor.execute(sql_update_material_type, ('ที่ใส่กระดาษชำระ', i))

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
                         project_material_total INT,
                         project_id INT, 
                         FOREIGN KEY (project_id) REFERENCES Projects(project_id)
                         ON DELETE  CASCADE 
                         ON UPDATE CASCADE
                        )
                         '''
            cursor.execute(project_material)
            insert_project_material = '''
                      INSERT INTO `ProjectMaterials` ( `project_material_id`,`project_material_name`,`project_material_price`, `project_material_total`,`project_id`) VALUES (NULL ,'คอนกรีตผสมเสร็จรูปลูกบาศก์ 180 กก./ตร.ซม. และ รูปทรงกระบอก 140กก./ตร.ซม. ตราซีแพค',1794.39, 1, 1);
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
                     status BIT NOT NULL,
                     contractor_id INT, FOREIGN KEY (contractor_id) REFERENCES Contractors(contractor_id)ON DELETE  CASCADE ON UPDATE CASCADE)
                     '''
            cursor.execute(project)
            insert_contractor = '''
                    INSERT INTO `Projects` ( `project_id`,`project_name`,`project_description`,`customer_name`,`deadline`, `status`,`contractor_id`) VALUES (NULL ,'โปรเจคที่ 1','project I is for testing project card Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua.','โอ๊ต','2022-12-25', 1, 1),(NULL ,'โปรเจคที่ 2','project II is for testing project card Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua.','ก้อง','2022-12-25', 0, 1),(NULL ,'โปรเจคที่ 3','project II is for testing project card Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua.','ปั้น','2022-12-10', 1, 1);
                    '''
            cursor.execute(insert_contractor)
            builder.commit()
            print('Created Project')
        except:
            print('Create fail')
        # Project_Entity

    # BOQ_Entity
    @staticmethod
    def build_table_BOQ():
        try:
            cursor = builder.cursor()
            BOQ = '''
                     CREATE TABLE BOQs (
                     BOQ_id INT AUTO_INCREMENT PRIMARY KEY,
                     BOQ_name VARCHAR(255) NOT NULL,
                     project_id INT, FOREIGN KEY (project_id) REFERENCES Projects(project_id)ON DELETE  CASCADE ON UPDATE CASCADE
                     )
                     '''
            cursor.execute(BOQ)
            insert_BOQ = '''
                    INSERT INTO BOQs ( BOQ_id,BOQ_name,project_id) VALUES (NULL ,'BOQที่ 1', 1 ),(NULL ,'BOQที่ 2', 1),(NULL ,'BOQที่ 3', 1);
                    '''
            cursor.execute(insert_BOQ)
            builder.commit()
            print('Created BOQ')
        except:
            print('Create fail')

    # BOQList_Entity
    @staticmethod
    def build_table_BOQ_list():
        try:
            cursor = builder.cursor()
            BOQ_list = '''
                        CREATE TABLE BOQLists (
                        BOQ_list_id INT AUTO_INCREMENT PRIMARY KEY,
                        list_name VARCHAR(255) NOT NULL,
                        total_quantity FLOAT,
                        unit VARCHAR(255) NOT NULL,
                        cost_of_materials_per_unit FLOAT,
                        total_cost_materials FLOAT,
                        cost_of_wage_per_unit FLOAT,
                        total_wages FLOAT,
                        total_price FLOAT,
                        BOQ_id INT, 
                         FOREIGN KEY (BOQ_id) REFERENCES BOQs(BOQ_id)
                         ON DELETE  CASCADE 
                         ON UPDATE CASCADE,
                        customer_view_id INT, FOREIGN KEY (customer_view_id) REFERENCES CustomerViews(customer_view_id)ON DELETE  CASCADE ON UPDATE CASCADE
                        )
                         '''
            cursor.execute(BOQ_list)
            insert_BOQ_list = '''
                      INSERT INTO BOQLists ( BOQ_list_id,list_name,total_quantity,unit,cost_of_materials_per_unit,total_cost_materials,cost_of_wage_per_unit,total_wages,total_price,BOQ_id,customer_view_id) VALUES (NULL ,'ทาสีผนัง',18.00,'ตร.ม',200.00,3600.00,100.00,1800.00,5400.00, 1,1),(NULL ,'ก่อปูน',18.00,'ตร.ม',400.00,7200.00,100.00,1800.00,9000.00, 1,1);
                      '''
            cursor.execute(insert_BOQ_list)
            builder.commit()
            print('Created BOQlist')
        except:
            print('Create fail')

    # CustomerView_Entity
    @staticmethod
    def build_table_customer_view():
        try:
            cursor = builder.cursor()
            customer_view = '''
                         CREATE TABLE CustomerViews (
                         customer_view_id INT AUTO_INCREMENT PRIMARY KEY,
                         customer_view_name VARCHAR(255) NOT NULL,
                         project_id INT, FOREIGN KEY (project_id) REFERENCES Projects(project_id)ON DELETE  CASCADE ON UPDATE CASCADE
                     )
                          '''
            cursor.execute(customer_view)
            insert_customer_view = '''
                    INSERT INTO CustomerViews (customer_view_id,customer_view_name,project_id) VALUES (NULL ,'Customerที่ 1', 1 ),(NULL ,'Customerที่ 2', 1),(NULL ,'Customerที่ 3', 1);
                       '''
            cursor.execute(insert_customer_view)
            builder.commit()
            print('Created CustomerViews')
        except:
            print('Create fail')

    # MaterialComparator_Entity
    # @staticmethod
    # def build_table_material_comparator():
    #     try:
    #         cursor = builder.cursor()
    #         material_comparator = '''
    #                     CREATE TABLE MaterialComparators (
    #                     material_comparator_id INT AUTO_INCREMENT PRIMARY KEY,
    #                     material_comparator_name VARCHAR(255) ,
    #                     material_comparator_price VARCHAR(255))
    #                     '''
    #         cursor.execute(material_comparator)
    #         url = 'http://www.indexpr.moc.go.th/PRICE_PRESENT/table_month_regionCsi.asp'
    #         payload = {
    #             'DDMonth': '03',
    #             'DDYear': '2565',
    #             'DDProvince': '50',
    #             'texttable': 'csi_price_north_web_avg',
    #             'text_name': 'unit_code_N',
    #             'B1': '%B5%A1%C5%A7'
    #         }
    #         r = requests.post(url, data=payload).content
    #         df = pd.read_html(r)[0]
    #         df.dropna(inplace=True)
    #         df.drop(df.index[14:37], inplace=True)
    #         df.drop(df.index[27:29], inplace=True)
    #         df.drop(df.index[91:100], inplace=True)
    #         material_name = df[1].to_numpy()
    #         material_price = df[3].to_numpy()
    #         n = len(material_price)
    #         insert_material = '''
    #                           INSERT INTO MaterialComparators (material_comparator_price,material_comparator_name) VALUES (%s,%s);
    #                           '''
    #         for i in range(1, n, 1):
    #             val_name = str(material_name[i])
    #             val_price = str(material_price[i])
    #             cursor.execute(insert_material, (val_price,val_name ))
    #         builder.commit()
    #         print('Created MaterialComparators')
    #     except:
    #         print('Create fail')

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
            InitApp.build_table_BOQ()
            InitApp.build_table_customer_view()
            InitApp.build_table_BOQ_list()
            print('Complete build all tables')
        except:
            print('uncompleted build')
