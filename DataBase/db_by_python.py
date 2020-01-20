import mysql.connector
from DataBase.settings.config import Mysql


class ToMysqlByPython(Mysql):
    """
    Only Connect to Mysql Class

    connection's param from config.py in settings module
    Please your mysql setting write to SettingMysql's param in config.py
    """
    def __init__(self):
        super(ToMysqlByPython, self).__init__()
        
    def connects(self):
        """
        To connect at mysql for function

        :return: object: after connect
        """
        try:
            mysql_relation = mysql.connector.connect(
                host=Mysql.HOST,
                port=Mysql.PORT,
                user=Mysql.USER,
                password=Mysql.PASSWORD,
                database=Mysql.DATABASE
            )
            result = mysql_relation.is_connected()
        except mysql.connector.errors.DatabaseError as e:
            mysql_relation = None
            result = None
        return mysql_relation, result
