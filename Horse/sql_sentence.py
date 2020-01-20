import mysql.connector
from DataBase.BaseSQL import BaseSQL
from Horse.sqls import InsertSQL
from Horse.sqls import InsertMaleHorses
from Horse.sqls import InsertTrainers
from Horse.sqls import InsertOwners
from Horse.sqls import SelectUrlFromHorses
from Horse.sqls import SelectHorseIdFromHorse
from Horse.sqls import SelectHorseIdFromMaleHorses
from Horse.sqls import SelectTrainerIdFromTrainers
from Horse.sqls import SelectTrainerIdFromTrainers
from Horse.sqls import SelectTrainerIdFromOwner
from StringWords.error import InsertMessage


class InsertIntoHorses(BaseSQL):
    """
    This Class is Insert processes
        Target Mysql tables
            ・HORSES
            ・MALE_HORSES
            ・RACES
    """

    def __init__(self, object_sql):
        """
        There processes needs __init__()
        :param object_sql: object: connected mysql object
                           This param needs commit() and cursor()
        """
        super(InsertIntoHorses, self).__init__(object_sql)

    def into_horses_values(self, *args):
        """
        :param args: 馬名 性別 出生日 URL 調教師
        :return: SQL文, values
        """
        return InsertSQL.sql, args[0]

    def into_male_horses_values(self, *args):
        """
        :param 仔馬のID 父馬のID 母馬のID
        :return: SQL文, values
        """
        return InsertMaleHorses.sql, args[0]


class InsertIntoTrainers(BaseSQL):

    def __init__(self, object_sql):
        super(InsertIntoTrainers, self).__init__(object_sql)

    def into_trainers_values(self, *args):
        """
        :param 調教師名 URL
        :return: SQL文, values
        """
        return InsertTrainers.sql, args[0]


class InsertIntoOwners(BaseSQL):

    def __init__(self, object_sql):
        super(InsertIntoOwners, self).__init__(object_sql)

    def into_owners_value(self, *args):
        """
        :param 馬主名 URL
        :return: SQL文, values
        """
        return InsertOwners.sql, args[0]


class SelectFromHorses(BaseSQL):

    def __init__(self, object_sql):
        """
        There processes needs __init__()
        :param object_sql: object: connected mysql object
                           This param needs commit() and cursor()
        """
        super(SelectFromHorses, self).__init__(object_sql)

    def where_url(self, url):
        """
        :return: SQL文 検索対象URL
        """
        return SelectUrlFromHorses.sql, [self.create_target_url(url)]

    def where_horse_id(self, url):
        """
        :return: SQL文 検索対象URL
        """
        return SelectHorseIdFromHorse.sql, [url]

    def create_target_url(self, url):
        if "https://db.netkeiba.com/" in url:
            return url
        else:
            return "https://db.netkeiba.com" + url


class SelectFromMaleHorses(BaseSQL):

    def __init__(self, object_sql):
        """
        There processes needs __init__()
        :param object_sql: object: connected mysql object
                           This param needs commit() and cursor()
        """
        super(SelectFromMaleHorses, self).__init__(object_sql)

    def where_horse_id(self, horse_id):
        return SelectHorseIdFromMaleHorses.sql, [horse_id]


class SelectFromTrainers(BaseSQL):
    def __init__(self, object_sql):
        super(SelectFromTrainers, self).__init__(object_sql)

    def where_trainer_id(self, url):
        return SelectTrainerIdFromTrainers.sql, [url]


class SelectFromOwners(BaseSQL):
    def __init__(self, object_sql):
        super(SelectFromOwners, self).__init__(object_sql)

    def where_owner_id(self, url):
        return SelectTrainerIdFromOwner.sql, [url]
