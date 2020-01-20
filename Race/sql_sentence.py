import mysql.connector

from DataBase.BaseSQL import BaseSQL
from Horse.sqls import InsertSQL
from Race.sqls import InsertRaces
from Race.sqls import InsertRaceDetails
from Race.sqls import InsertBettingDetails
from Race.sqls import InsertJockeys
from Race.sqls import SelectJockeyIdFromJockeys
from Race.sqls import SelectRaceIdFromRaces


class Insert(BaseSQL):

    def __init__(self, object_sql):
        super(Insert, self).__init__(object_sql)

    def into_races_values(self, *args):
        """

        :param args:
        :return:
        """
        return InsertRaces.sql, args[0]

    def into_race_details_values(self, *args):
        """

        :param args:
        :return:
        """
        return InsertRaceDetails.sql, args[0]

    def into_betting_details_values(self, * args):
        """

        :param args:
        :return:
        """
        return InsertBettingDetails.sql, args[0]

    def into_jockeys_values(self, *args):
        """

        :param args:
        :return:
        """
        return InsertJockeys.sql, args[0]


class SelectFromJockeys(BaseSQL):

    def __init__(self, object_sql):
        super(SelectFromJockeys, self).__init__(object_sql)

    def where_url(self, url):
        return SelectJockeyIdFromJockeys.sql, [url]


class SelectFromRaces(BaseSQL):

    def __init__(self, object_sql):
        super(SelectFromRaces, self).__init__(object_sql)

    def where_url(self, url):
        return SelectRaceIdFromRaces.sql, [url]
