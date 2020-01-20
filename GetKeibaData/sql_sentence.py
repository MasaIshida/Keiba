import mysql.connector
from DataBase.BaseSQL import BaseSQL
from GetKeibaData.sqls import SelectRaceDataFromRaces
from GetKeibaData.sqls import SelectHorseDataFromHorses
from GetKeibaData.sqls import SelectJockeyIDFromRiders


class ExecuteQuery(BaseSQL):

    def __init__(self, object_sql):
        super(ExecuteQuery, self).__init__(object_sql)
        self.select_keiba_data = SelectKeibaData()

    def get_race_data(self, race_id):
        return self.execute_select(self.select_keiba_data.where_race_id, race_id)

    def get_horse_data(self, horse_url):
        return self.execute_select(self.select_keiba_data.where_horse_url, horse_url)

    def get_jockey_data(self, jockey_url):
        return self.execute_select(self.select_keiba_data.where_jockey_url, jockey_url)


class SelectKeibaData():

    def where_race_id(self, race_id):
        return SelectRaceDataFromRaces.sql, [race_id]

    def where_horse_url(self, url):
        return SelectHorseDataFromHorses.sql, [url]

    def where_jockey_url(self, url):
        return SelectJockeyIDFromRiders.sql, [url]
