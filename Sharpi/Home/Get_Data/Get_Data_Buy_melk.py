# Import the requests library
import requests
import mysql.connector
import json
import time
class Buy_melk_New_data():
    def __init__(self):
        self.Page_address = 'https://api.divar.ir/v8/web-search/tehran/buy-residential?business-type=personal'
    def New_Melk(self, Tokens_in_DB):
        resp = requests.get(self.Page_address)
        resp = json.loads(resp.text)
        list_tokens = []
        for i in resp['web_widgets']['post_list']:

            token = i['data']['action']['payload']['token']
            if token in Tokens_in_DB:
                print(f'This Token {token} is not okay ---')
            else:
                print(f'This Token {token} is okay +++')
                list_tokens.append(token)
        return list_tokens
    def Check_token(self):
        try:
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()
            sql_select_query = """select * from Tokens_alredy_have LIMIT 1000"""
            cursor.execute(sql_select_query)
            record = cursor.fetchall()
            list_lab = []
            for i in range(0, len(record)):
                #list_lab_lab = []
                #list_lab_lab.append(record[i][0])
                #list_lab_lab.append()
                list_lab.append(record[i][1])
        except mysql.connector.Error as error:
            # print("Failed to get record from MySQL table: {}".format(error))
            pass

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print(list_lab)
                print("MySQL connection is closed")
                return list_lab
    def Save_token_into_DB(self, Token_list:list):
        try:
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()
            for i in Token_list:
                sql_select_query = """INSERT INTO Tokens_alredy_have (id, token, is_details) VALUES(%s, %s, %s)"""
                # set variable in query
                cursor.execute(sql_select_query,(None, i, 0,))

                # fetch result
                connection.commit()
                print(f"Record inserted successfully into Tokens_alredy_have table And token was : {i}")
        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    def Start(self):
        while True:
            try:
                Tokens_in_db = self.Check_token()# Get 1000 Tokens form DB From last
                Tokens_should_insert_to_db = self.New_Melk(Tokens_in_db)# Check new token that get from Divar is valid or not then return a list
                self.Save_token_into_DB(Tokens_should_insert_to_db)# this is insert a list of token in db
                time.sleep(10)
            except Exception as e:
                print(f'####   We Have Error and It is : {e} ###')
class Buy_melk_New_details():
    def __init__(self):
        self.Link_Address_for_token_details = 'https://api.divar.ir/v8/posts-v2/web/'
    def Get_one_token(self):
        try:
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()
            sql_select_query = """select * from Tokens_alredy_have WHERE is_details=0 ORDER BY ID DESC LIMIT 1"""
            cursor.execute(sql_select_query)
            record = cursor.fetchall()
            list_lab = []
            ids = 0
            for i in range(0, len(record)):
                #list_lab_lab = []
                #list_lab_lab.append(record[i][0])
                #list_lab_lab.append()
                ids = record[i][0]
                list_lab.append(record[i][1])
        except mysql.connector.Error as error:
            # print("Failed to get record from MySQL table: {}".format(error))
            pass

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print(list_lab)
                print("MySQL connection is closed")
                return list_lab, ids
    def Get_details_from_divar(self, token):
        #token = 'QZtffJ7L'
        self.Link_Address_for_req = self.Link_Address_for_token_details + token
        resp = requests.get(self.Link_Address_for_req)
        print(resp)
        resp = json.loads(resp.text)
        return resp
    def Desc_verification(self, desk):
        list_str_not_valid = ['مشاور', 'همکار']
        for i in list_str_not_valid:
            if i in desk:
                return False
        return True

    def Laboratory_of_details(self, details, token):
        desk = ''
        section_map = ''
        section_listdata = ''
        try:
            # Find desk and verify it
            for i in details['sections']:
                if i['section_name'] == 'DESCRIPTION':
                    for z in i['widgets']:
                        if z['widget_type'] == "DESCRIPTION_ROW":
                            desk = z['data']['text']
                elif i['section_name'] == 'LIST_DATA':
                    section_listdata = i
                elif i['section_name'] == 'MAP':
                    section_map = i
            print(f'DESCRIPTION Of Token : {desk}')
            #print(section_map)
            # End

            if self.Desc_verification(desk):
                return_list_of_details = []
                # ------------------------------------- webengage section of deatils
                # image_count, business_ref, category, city, credit, district, gender, originality, price, rent, status  these are parameter of this section

                image_count = details['webengage']['image_count']
                price = details['webengage']['price']
                rent = details['webengage']['rent']
                district = details['webengage']['district'] # mahal
                city = details['webengage']['city']

                # ------------------------------------- end
                # ------------------------------------- seo section of deatils
                # title, description, android_package_name, web_info, credit, unavailable_after these are parameter of this section

                title = details['seo']['title']
                district_persian = details['seo']['web_info']['district_persian']
                city_persian = details['seo']['web_info']['city_persian']
                unavailable_after = details['seo']['unavailable_after']


                # ------------------------------------- end
                # ------------------------------------- sections Map section of deatils
                # latitude, longitude, image_url these are parameter of this section
                latitude = 0
                longitude = 0
                image_url = 0
                if len(section_map) > 0:
                    latitude = section_map['widgets'][0]['data']['location']['exact_data']['point']['latitude']
                    longitude = section_map['widgets'][0]['data']['location']['exact_data']['point']['longitude']
                    image_url = section_map['widgets'][0]['data']['image_url']

                # ------------------------------------- end
                # ------------------------------------- sections LIST_DATA section of deatils
                # GROUP_INFO_ROW, .... these are parameter of this section
                room = 0
                meter = 0
                time_make = 0
                price_total = 0
                price_meter = 0
                tabagheh = 0
                asansor = 0
                parking = 0
                anbariy = 0
                balkon = 0
                kooler = 0
                shofazh = 0
                kaf_seramik = 0
                if len(section_listdata['widgets']) > 0:
                    for i in section_listdata['widgets']:
                        if i['widget_type'] == "GROUP_INFO_ROW":
                            for z in i['data']['items']:
                                if z['title'] == 'متراژ':
                                    meter = z['value']
                                elif z['title'] == 'ساخت':
                                    time_make = z['value']
                                elif z['title'] == 'اتاق':
                                    room = z['value']
                        elif i['widget_type'] == "UNEXPANDABLE_ROW":
                            if i['data']['title'] == "قیمت کل":
                                price_total = i['data']['value']
                            elif i['data']['title'] == "قیمت هر متر":
                                price_meter = i['data']['value']
                            elif i['data']['title'] == "طبقه":
                                tabagheh = i['data']['value']
                        elif i['widget_type'] == "GROUP_FEATURE_ROW":
                            try:
                                for z in i['data']['action']['payload']['modal_page']['widget_list']:
                                    if z['widget_type'] == 'FEATURE_ROW':
                                        if z['data']['title'] == 'آسانسور':
                                            asansor = 1
                                        elif z['data']['title'] == 'پارکینگ':
                                            parking = 1
                                        elif z['data']['title'] == 'انباری':
                                            anbariy = 1
                                        elif z['data']['title'] == 'جنس کف سرامیک':
                                            kaf_seramik = 1
                                        elif z['data']['title'] == 'سرمایش کولر آبی':
                                            kooler = 1
                                        elif z['data']['title'] == 'بالکن':
                                            balkon = 1
                                        elif z['data']['title'] == 'گرمایش شوفاژ':
                                            balkon = 1
                            except:
                                for z in i['data']['items']:
                                    if z['title'] == 'آسانسور':
                                        asansor = 1
                                    elif z['title'] == 'پارکینگ':
                                        parking = 1
                                    elif z['title'] == 'انباری':
                                        anbariy = 1
                                    elif z['title'] == 'جنس کف سرامیک':
                                        kaf_seramik = 1
                                    elif z['title'] == 'سرمایش کولر آبی':
                                        kooler = 1
                                    elif z['title'] == 'بالکن':
                                        balkon = 1
                                    elif z['title'] == 'گرمایش شوفاژ':
                                        balkon = 1
                print('-----------------------------\n')
                return_list_of_details.append(None)
                return_list_of_details.append(token[0])
                print(f'mahal of token is : {district}')
                return_list_of_details.append(district)
                print(f'image count of token is : {image_count}')
                return_list_of_details.append(image_count)
                print(f'rent of token is : {rent}')
                return_list_of_details.append(rent)
                print(f'price of token is : {price}')
                return_list_of_details.append(price)
                print(f'city of token is : {city}')
                return_list_of_details.append(city)
                print(f'title of token is : {title}')
                return_list_of_details.append(title)
                print(f'city of token is : {city_persian}')
                return_list_of_details.append(city_persian)
                print(f'mahal of token is : {district_persian}')
                return_list_of_details.append(district_persian)
                print(f'time unvalibale of token is : {unavailable_after}')
                return_list_of_details.append(unavailable_after)
                print(f'latitude of this token is : {latitude}')
                return_list_of_details.append(latitude)
                print(f'longitude of this token is : {longitude}')
                return_list_of_details.append(longitude)
                print(f'Metrazh is : {meter}')
                return_list_of_details.append(meter)
                print(f'Time make is : {time_make}')
                return_list_of_details.append(time_make)
                print(f'Room of number is : {room}')
                return_list_of_details.append(room)
                print(f'price total is : {price_total}')
                return_list_of_details.append(price_total)
                print(f'price meter : {price_meter}')
                return_list_of_details.append(price_meter)
                print(f'tabeghe number is : {tabagheh}')
                return_list_of_details.append(tabagheh)
                print(f'asansor number is : {asansor}')
                return_list_of_details.append(asansor)
                print(f'parking number is : {parking}')
                return_list_of_details.append(parking)
                print(f'balkon number is : {balkon}')
                return_list_of_details.append(balkon)
                print(f'shofazh number is : {shofazh}')
                return_list_of_details.append(shofazh)
                print(f'kooler number is : {kooler}')
                return_list_of_details.append(kooler)
                print(f'kaf_seramik number is : {kaf_seramik}')
                return_list_of_details.append(kaf_seramik)
                print('-----------------------------\n')
                    #print(section_listdata['widgets'][0])
                return_list_of_details.append(0)
                return_list_of_details.append(desk)
                # ------------------------------------- end
                return tuple(return_list_of_details)
            else:
                print('HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRRRR')
                return -1
        except Exception as e:
            print(e)
            return -1
    def Insert_detials(self, tupel_data:tuple):
        res = 0
        try:
            print(tupel_data)
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()

            sql_select_query = """INSERT INTO Aparteman_buy_details (id, token, mahal_english, image_count, rent, price, city,title,city_persian,mahal_persian,time_unavailabe,lat_map,long_map,meter,time_make,room,price_total,price_meter,tabagheh,asansor,parking,balkon,shofazh,kooler,kafe_seramick,is_phone_add,desck) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            # set variable in query
            cursor.execute(sql_select_query, tupel_data)

            # fetch result
            connection.commit()
            print(f"Record inserted successfully into Tokens_alredy_have table And token was : {tupel_data[1]}")
            res = 1
        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))
            res = -1
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return res
    def Update_tokens_status(self, ids):
        res_update = 0
        try:
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()
            sql_update_query = """Update Tokens_alredy_have set is_details = 1 WHERE id = %s"""
            # print(str(data[5]))

            cursor.execute(sql_update_query, (ids,))
            connection.commit()
            print(f"Record Updated successfully : {ids}")
            res_update = 1
        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))
            res_update = -1
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return res_update

    def Start(self):
        while True:
            token, ids = self.Get_one_token()
            print('Get token')
            if len(token)>0:
                details = self.Get_details_from_divar(token[0])
                print('Get details')
                Tupel_details_procced = self.Laboratory_of_details(details, token)
                print('Get Laboratory_of_details')
                if Tupel_details_procced != -1:
                    res = self.Insert_detials(Tupel_details_procced)
                    if res == 1:
                        res_update = self.Update_tokens_status(ids)
                        if res_update != 1:
                            print('!!!!!!!!!!!!!!!!!!!!!!!')
                            print('error in update')
                            print('!!!!!!!!!!!!!!!!!!!!!!!')
                            time.sleep(200)
                    else:
                        print('!!!!!!!!!!!!!!!!!!!!!!!')
                        print('error in insert')
                        print('!!!!!!!!!!!!!!!!!!!!!!!')
                else:
                    print('!!!!!!!!!!!!!!!!!!!!!!!')
                    print('error in get details')
                    print('!!!!!!!!!!!!!!!!!!!!!!!')
                    res_update = self.Update_tokens_status(ids)
                    if res_update != 1:
                        print('!!!!!!!!!!!!!!!!!!!!!!!')
                        print('error in update')
                        print('!!!!!!!!!!!!!!!!!!!!!!!')
                        time.sleep(200)
            else:
                time.sleep(200)
            time.sleep(2)

class Buy_melk_New_phone_number():
    def __init__(self):
        self.link_get_req = 'https://api.divar.ir/v8/postcontact/web/contact_info/'
    def Get_token_from_db(self):
        try:
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()
            sql_select_query = """select * from Aparteman_buy_details WHERE is_phone_add = 0 ORDER BY id DESC LIMIT 1"""
            cursor.execute(sql_select_query)
            record = cursor.fetchall()
            #list_lab = []
            ids = 0
            tokens = ''
            for i in range(0, len(record)):
                # list_lab_lab = []
                # list_lab_lab.append(record[i][0])
                # list_lab_lab.append()
                ids = record[i][0]
                tokens = record[i][1]

                #list_lab.append(record[i][1])
        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))
            pass

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return tokens, ids
    def Send_req(self, token):
        self.Link_Address_for_req = self.link_get_req + token
        headers = {
            'Authorization':'Basic eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJlMWEzMTUwOS01NjM2LTQ3OTUtODdiMS03M2VkMjUwZTlmMjciLCJ1c2VyLXR5cGUiOiJwZXJzb25hbCIsInVzZXItdHlwZS1mYSI6Ilx1MDY3ZVx1MDY0Nlx1MDY0NCBcdTA2MzRcdTA2MmVcdTA2MzVcdTA2Y2MiLCJ1c2VyIjoiMDkyMDA5ODkyMDIiLCJpc3MiOiJhdXRoIiwidmVyaWZpZWRfdGltZSI6MTcxMDM1ODUyNywiaWF0IjoxNzEwMzU4NTI3LCJleHAiOjE3MTU1NDI1Mjd9.tSQmMQwc6sKTJJSREG1JtnhjV03rzvYs_0WtmChRXf8',
        }
        resp = requests.get(self.Link_Address_for_req, headers=headers)
        print(resp.text)
        resp = json.loads(resp.text)
        return resp
    def insert_phone_number(self, token, ids, english_number, persian_number):
        try:
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()

            sql_select_query = """INSERT INTO phone_buy_apartment (id, token_details, id_details, e_phone, p_phone) VALUES(%s, %s, %s, %s, %s)"""
            # set variable in query
            cursor.execute(sql_select_query, (None, token, ids, english_number, persian_number,))

            # fetch result
            connection.commit()
            print(f"Record inserted successfully into phone_buy_apartment table And token was : {token}")
        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    def update_details_token(self, ids):
        res_update = 0
        try:
            connection = mysql.connector.connect(host="localhost",
                                                 user='root',
                                                 password='ya mahdi',
                                                 database="SHARPI_HOME")
            cursor = connection.cursor()
            sql_update_query = """Update Aparteman_buy_details set is_phone_add = 1 WHERE id = %s"""
            # print(str(data[5]))

            cursor.execute(sql_update_query, (ids,))
            connection.commit()
            print(f"Record Updated successfully : {ids}")
            res_update = 1
        except mysql.connector.Error as error:
            print("Failed to get record from MySQL table: {}".format(error))
            res_update = -1
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return res_update
    def Start(self):
        counter = 170
        while counter>0:
            token, ids = self.Get_token_from_db()
            if ids != 0:
                print(token)
                try:
                    mobile_data = self.Send_req(token)
                    persian_mobile = mobile_data['widget_list'][0]['data']['value']
                    english_mobile = mobile_data['widget_list'][0]['data']['action']['payload']['phone_number']
                    self.insert_phone_number(token, ids, english_mobile, persian_mobile)
                    self.update_details_token(ids)
                except Exception as e:
                    print('EEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRR')
                    print(e)
                    self.update_details_token(ids)
                    #break
            else:
                print(ids)
                print(token)
                break
            counter = counter - 1
            print(f'Counter is  ----------------------- {counter}')
            #time.sleep(200)


'''
x = Buy_melk_New_data()
x.Start()

z = Buy_melk_New_details()
z.Start()
'''
'''
y = Buy_melk_New_phone_number()
y.Start()
'''

'''
CREATE TABLE Tokens_alredy_have(id INT AUTO_INCREMENT PRIMARY KEY, token VARCHAR(20));
ALTER TABLE Tokens_alredy_have ADD is_details int;
describe Tokens_alredy_have;
+------------+-------------+------+-----+---------+----------------+
| Field      | Type        | Null | Key | Default | Extra          |
+------------+-------------+------+-----+---------+----------------+
| id         | int         | NO   | PRI | NULL    | auto_increment |
| token      | varchar(20) | YES  |     | NULL    |                |
| is_details | int         | YES  |     | NULL    |                |
+------------+-------------+------+-----+---------+----------------+
3 rows in set (0.01 sec)

--------------------------------------------------------------------------------
CREATE TABLE Aparteman_buy_details(id INT AUTO_INCREMENT PRIMARY KEY, token VARCHAR(20), mahal_english VARCHAR(255),image_count int,rent VARCHAR(255),price int, city VARCHAR(255),title VARCHAR(255),city_persian VARCHAR(255),mahal_persian VARCHAR(255),time_unavailabe VARCHAR(255),lat_map VARCHAR(255),long_map VARCHAR(255),meter VARCHAR(255),time_make VARCHAR(255),room VARCHAR(255),price_total VARCHAR(255),price_meter VARCHAR(255),tabagheh VARCHAR(255),asansor int,parking int,balkon int,shofazh int,kooler int,kafe_seramick int);
mysql> DESCRIBE Aparteman_buy_details;
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int          | NO   | PRI | NULL    | auto_increment |
| token           | varchar(20)  | YES  |     | NULL    |                |
| mahal_english   | varchar(255) | YES  |     | NULL    |                |
| image_count     | int          | YES  |     | NULL    |                |
| rent            | varchar(255) | YES  |     | NULL    |                |
| price           | int          | YES  |     | NULL    |                |
| city            | varchar(255) | YES  |     | NULL    |                |
| title           | varchar(255) | YES  |     | NULL    |                |
| city_persian    | varchar(255) | YES  |     | NULL    |                |
| mahal_persian   | varchar(255) | YES  |     | NULL    |                |
| time_unavailabe | varchar(255) | YES  |     | NULL    |                |
| lat_map         | varchar(255) | YES  |     | NULL    |                |
| long_map        | varchar(255) | YES  |     | NULL    |                |
| meter           | varchar(255) | YES  |     | NULL    |                |
| time_make       | varchar(255) | YES  |     | NULL    |                |
| room            | varchar(255) | YES  |     | NULL    |                |
| price_total     | varchar(255) | YES  |     | NULL    |                |
| price_meter     | varchar(255) | YES  |     | NULL    |                |
| tabagheh        | varchar(255) | YES  |     | NULL    |                |
| asansor         | int          | YES  |     | NULL    |                |
| parking         | int          | YES  |     | NULL    |                |
| balkon          | int          | YES  |     | NULL    |                |
| shofazh         | int          | YES  |     | NULL    |                |
| kooler          | int          | YES  |     | NULL    |                |
| kafe_seramick   | int          | YES  |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
25 rows in set (0.02 sec)
SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'Aparteman_buy_details'
ALTER TABLE Aparteman_buy_details MODIFY price BIGINT;
ALTER TABLE Aparteman_buy_details ADD is_phone_add int;
ALTER TABLE Aparteman_buy_details ADD desck VARCHAR(255);
ALTER TABLE Aparteman_buy_details MODIFY desck text;
CREATE TABLE phone_buy_apartment(id INT AUTO_INCREMENT PRIMARY KEY, token_details VARCHAR(20), id_details INT, e_phone VARCHAR(20), p_phone VARCHAR(20));
mysql> describe phone_buy_apartment;
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| id            | int         | NO   | PRI | NULL    | auto_increment |
| token_details | varchar(20) | YES  |     | NULL    |                |
| id_details    | int         | YES  |     | NULL    |                |
| e_phone       | varchar(20) | YES  |     | NULL    |                |
| p_phone       | varchar(20) | YES  |     | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+

'''