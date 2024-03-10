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

x = Buy_melk_New_data()
x.Start()

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

'''