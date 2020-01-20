from Horse.web_scraping import HorseScraping
from Horse.get_horse_data import Horse
from Horse.sql_sentence import SelectFromHorses
from Horse.sql_sentence import SelectFromMaleHorses
from Horse.sql_sentence import SelectFromTrainers
from Horse.sql_sentence import SelectFromOwners
from Horse.sql_sentence import InsertIntoHorses
from Horse.sql_sentence import InsertIntoTrainers
from Horse.sql_sentence import InsertIntoOwners
from StringWords.error import InsertMessage
from logs.log_write import Logs


class BaseHorseProcess(object):

    def __init__(self, url, class_mysql):
        # 処理に必要な情報をインスタンス変数へ格納
        self.select_from_horse = SelectFromHorses(class_mysql)
        self.select_from_male_horses = SelectFromMaleHorses(class_mysql)
        self.select_from_trainers = SelectFromTrainers(class_mysql)
        self.select_from_owners = SelectFromOwners(class_mysql)
        self.insert = InsertIntoHorses(class_mysql)
        self.insert_trainer = InsertIntoTrainers(class_mysql)
        self.insert_owner = InsertIntoOwners(class_mysql)
        self.horse_scraping = HorseScraping(url)
        self.url = self.horse_scraping.create_target_url()
        self.log = Logs()

    def get_info(self):
        """
        対象馬の情報取得
            self.horse_name: 馬名
            self.gender    : 性別
            self.birth     : 出生日
        """
        html_data = self.horse_scraping.request_get_method()
        self.horse = Horse(html_data)
        self.horse_name, self.gender = self.horse.get_name_and_gender()
        self.birth = self.horse.get_birth()

    def get_male_horses(self):
        """
        対象馬の親馬の情報取得
            self.urls
            :return list: 親馬のURL
        """
        return self.horse.get_blood()

    def sql_process_horses(self):
        """
        対象馬の情報をMySQLへ登録
            対象テーブル: HORSES
            SQL       : Insert Into HORSES values(馬名, 性別, 出生日, 対象馬のURL)
        """

        if bool(self.select_from_horse.execute_select(self.select_from_horse.where_url, self.url)) is False:
            self.insert.execute_insert(
                                      self.insert.into_horses_values,
                                      self.horse_name,
                                      self.gender,
                                      self.birth,
                                      self.url,
                                      self.trainer_id,
                                      self.owner_id
                                      )

    def sql_process_male(self, male_url, female_url):
        if self.url is None:
            print("対象馬のURLがNoneです")
            print("備考", male_url, female_url)
            return
        self.main_horse_id = self.select_from_horse.execute_select(self.select_from_horse.where_horse_id, self.url)
        # listで返される
        if bool(self.select_from_male_horses.execute_select(
                self.select_from_male_horses.where_horse_id,
                self.main_horse_id[0][0])) \
                is not True:
            # list内にタプルで返される [(data,)]
            male_id = self.select_from_horse.execute_select(self.select_from_horse.where_horse_id, male_url)
            female_id = self.select_from_horse.execute_select(self.select_from_horse.where_horse_id, female_url)
            # 父馬と母馬ともに登録がある場合
            if male_url is not None and female_url is not None:
                self.insert.execute_insert(
                                           self.insert.into_male_horses_values,
                                           self.main_horse_id[0][0],
                                           male_id[0][0],
                                           female_id[0][0]
                                           )
            # 父馬のみ登録がある場合
            elif male_url is not None and female_url is None:
                self.insert.execute_insert(
                                            self.insert.into_male_horses_values,
                                            self.main_horse_id[0][0],
                                            male_id[0][0],
                                            None
                                           )
            # 母馬のみ登録がある場合
            elif male_url is None and female_url is not None:
                self.insert.execute_insert(
                                            self.insert.into_male_horses_values,
                                            self.main_horse_id[0][0],
                                            None,
                                            female_id[0][0]
                                           )
            # 両親馬ともに登録がない場合
            elif male_url is None and female_url is None:
                self.insert.execute_insert(
                                            self.insert.into_male_horses_values,
                                            self.main_horse_id[0][0],
                                            None,
                                            None
                                           )
            else:
                print(InsertMessage.insert_error_male)

    def sql_trainer_process(self):
        self.trainer_url, trainer_name = self.horse.get_trainer()
        result = bool(
            self.select_from_trainers.execute_select(
                self.select_from_trainers.where_trainer_id,
                self.trainer_url
            )
        )
        if result is False and self.trainer_url is not None and trainer_name is not None:
            self.insert_trainer.execute_insert(
                self.insert_trainer.into_trainers_values,
                trainer_name,
                self.trainer_url
            )
        trainer_result = self.select_from_trainers.execute_select(
                self.select_from_trainers.where_trainer_id,
                self.trainer_url
            )
        if bool(trainer_result):
            self.trainer_id = trainer_result[0][0]
        else:
            self.trainer_id = None

    def sql_owner_process(self):
        self.owner_url, owner_name = self.horse.get_owner()
        result = bool(
            self.select_from_owners.execute_select(
                self.select_from_owners.where_owner_id,
                self.owner_url
            )
        )
        if result is False and self.owner_url is not None and owner_name is not None:
            self.insert_owner .execute_insert(
                self.insert_owner.into_owners_value,
                owner_name,
                self.owner_url
            )
        owner_result = self.select_from_trainers.execute_select(
            self.select_from_owners.where_owner_id,
            self.owner_url
        )
        if bool(owner_result):
            self.owner_id = owner_result[0][0]
        else:
            self.owner_id = None

    def debug(self):
        self.log.write_children_horse_info(self.horse_name,
                                           self.gender,
                                           self.birth,
                                           self.url)
        print('馬名：',
              self.horse_name,
              '性別：',
              self.gender,
              '出生日：',
              self.birth)


class MaleHorse(BaseHorseProcess):

    def __init__(self, url, class_mysql):
        super(MaleHorse, self).__init__(url, class_mysql)
        self.url = self.horse_scraping.create_target_url()

    def male_only_process(self):
        self.horse_id = self.select_from_horse.execute_select(self.select_from_horse.where_url, self.url)
        # list[tuple()]
        return self.horse_id

    def find_male_horses(self):
        return bool(self.select_from_male_horses.execute_select(self.select_from_horse.where_horse_id, self.horse_id[0][0]))

    def debug(self):
        self.log.write_male_horse_info(self.horse_name,
                                       self.gender,
                                       self.birth,
                                       self.url)
        print('親馬名：',
              self.horse_name,
              '性別：',
              self.gender,
              '出生日：',
              self.birth)


class ChildrenHorse(BaseHorseProcess):
    
    def __init__(self, url, class_mysql):
        super(ChildrenHorse, self).__init__(url, class_mysql)
