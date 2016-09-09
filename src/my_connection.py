import pymysql

host = '192.168.23.43'
database = 'NewsDb'
user = 'tamnt'
# password = 'Psb89JRyWsXwm9C' # from server
password = 'NkoCb3ReeOXu8a0' # from vpn

def getConnection():
    connection = pymysql.connect(host=host, db=database, user=user, passwd=password, charset='utf8')
    return connection

def closeConnection(connection):
    if connection != None:
        connection.close()