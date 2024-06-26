# # db_connection.py
#
# import jaydebeapi
# import os
#
# # Parameterize the connection details at the top of the script
# server = 'FSI-FSQL3-PROD'
# database = 'FlinnWebPriceDW'
# username = 'svc_webscrape'
# password = 'A9wCQKVPNLzm!d$AC$fY'
# domain = 'fsi'
#
# jdbc_driver_dir = r'C:\Users\G6\Downloads\sqljdbc_12.6\enu\jars'
# jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
# jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
# jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
#
# # JDBC connection URL
# connection_url = f'jdbc:sqlserver://FSI-FSQL3-PROD;databaseName={database};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'
#
# # Additional connection properties
# connection_properties = {
#     'user': f'{username}',
#     'password': password,
#     'integratedSecurity': 'true',
#     'authenticationScheme': 'NTLM',
#     'domain': domain
# }
#
#
# def get_connection():
#     try:
#         connection = jaydebeapi.connect(
#             jdbc_driver_class,
#             connection_url,
#             connection_properties,
#             [jdbc_driver_path]
#         )
#         return connection
#     except jaydebeapi.DatabaseError as e:
#         print("Error connecting to the database: ", e)
#         return None
#
#
# def test_connection():
#     connection = get_connection()
#     if connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT @@version;")
#         row = cursor.fetchone()
#         while row:
#             print(row[0])
#             row = cursor.fetchone()
#         cursor.close()
#         connection.close()
#         print("Connection successful!")
#
#
# if __name__ == "__main__":
#     test_connection()


import os
import jaydebeapi


# Function to read connection details from a text file
def read_connection_details(file_path):
    connection_details = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            connection_details[key.strip()] = value.strip()
    return connection_details


# Main function to connect to SQL Server
def connect_to_sql_server(connection_file):
    try:
        connection_details = read_connection_details(connection_file)

        username = connection_details.get('Username')
        password = connection_details.get('Password')
        schema = connection_details.get('Schema')

        jdbc_driver_dir = r'C:\Users\G6\Downloads\sqljdbc_12.6\enu\jars'
        jdbc_driver_jar = 'mssql-jdbc-12.6.3.jre8.jar'
        jdbc_driver_path = os.path.join(jdbc_driver_dir, jdbc_driver_jar)
        jdbc_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
        #
        # JDBC connection URL
        server = 'FSI-FSQL3-PROD'
        connection_url = f'jdbc:sqlserver://{server};databaseName={schema};encrypt=true;trustServerCertificate=true;integratedSecurity=true;'

        # Additional connection properties
        connection_properties = {
            'user': username,
            'password': password,
            'integratedSecurity': 'true',
            'authenticationScheme': 'NTLM',
            'domain': 'fsi'
        }

        # Connect to the database
        connection = jaydebeapi.connect(
            jdbc_driver_class,
            connection_url,
            connection_properties,
            [jdbc_driver_path]
        )

        # Test connection by executing a query
        cursor = connection.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()

        cursor.close()
        connection.close()
        print("Connection successful!")

    except Exception as e:
        print(f"Error connecting to the database: {e}")


if __name__ == "__main__":
    connection_file = 'database_credentials.txt'
    connect_to_sql_server(connection_file)

