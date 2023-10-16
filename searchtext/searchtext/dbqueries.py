import pyodbc


sql_credentials = {
    "server": 'yoursever.database.windows.net',
    "database": 'DB',
    "username": 'youruser',
    "password": 'yourpassword$',
    "driver": '{ODBC Driver 17 for SQL Server}'
}

# available_drivers = pyodbc.drivers()
# for driver in available_drivers:
#             print(driver)

def dml_run_update(sql_query):
    with pyodbc.connect('DRIVER='+sql_credentials['driver']+';SERVER=tcp:'+sql_credentials['server']+';PORT=1433;DATABASE='+sql_credentials['database']+';UID='+sql_credentials['username']+';PWD='+ sql_credentials['password']) as conn:
        with conn.cursor() as cursor:

            print('Executig...')
            print(sql_query)

            cursor.execute(sql_query)
        
            print("Messages: ", cursor.messages)
            # [('[01000] (50000)', '[Microsoft][ODBC SQL Server Driver][SQL Server]Test Message')]

            conn.commit()
            print('Commited!')


def dml_run_select(sql_query):
    with pyodbc.connect('DRIVER='+sql_credentials['driver']+';SERVER=tcp:'+sql_credentials['server']+';PORT=1433;DATABASE='+sql_credentials['database']+';UID='+sql_credentials['username']+';PWD='+ sql_credentials['password']) as conn:
        with conn.cursor() as cursor:

            print('Executig...')
            print(sql_query)

            # cursor.execute('SELECT * FROM websites_data')
            cursor.execute(sql_query)

            sql_output = [i for i in cursor]
                
            print("Messages: ", cursor.messages)
            # [('[01000] (50000)', '[Microsoft][ODBC SQL Server Driver][SQL Server]Test Message')]

            conn.commit()
            print('Commited!')
            return sql_output
        

