import mysql.connector


class BaseSQL(object):
    """
    SQL実行の為のベースオブジェクト
    """
    def __init__(self, object_sql):
        self.object_sql = object_sql
        self.cursor = object_sql.cursor()

    def execute_insert(self, insert_values_func, *args):
        c = self.cursor
        o = self.object_sql

        def execute():
            try:
                sql, data = insert_values_func(args)
                c.execute(sql, data)
                o.commit()
            except mysql.connector.errors.IntegrityError as e:
                pass
        return execute()

    def execute_select(self, select_func, para):
        c = self.cursor

        def execute():
            sql, data = select_func(para)
            c.execute(sql, data)
            # list type
            return c.fetchall()
        return execute()
