import mysql.connector
def Show_Data_Melk_Buy_Section_FirstPage():
    try:
        connection = mysql.connector.connect(host="localhost",
                                             user='root',
                                             password='ya mahdi',
                                             database="SHARPI_HOME")
        cursor = connection.cursor()
        sql_select_query = """select * from Aparteman_buy_details ORDER BY ID DESC LIMIT 100"""
        cursor.execute(sql_select_query)
        record = cursor.fetchall()
        list_lab = []

        for i in range(0, len(record)):
            list_lab_lab = []
            for z in record[i]:
                list_lab_lab.append(z)

            list_lab.append(list_lab_lab)
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
#print(Show_Data_Melk_Buy_Section_FirstPage())