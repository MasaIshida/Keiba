from Race.web_scraping import RaceScraping
from Race.web_scraping import RaceDetailsScraping
from Race.get_race_data import Races
from Race.get_race_data import RaceDetails
from Race.sql_sentence import Insert
from Race.sql_sentence import SelectFromJockeys
from Horse.sql_sentence import SelectFromHorses
from Race.sql_sentence import SelectFromRaces


class BaseRaceProcess(object):

    def __init__(self, url, class_mysql):
        self.class_set(url)

    def class_set(self, url):
        pass

    def get_data(self):
        pass


class SearchRacesProcess(BaseRaceProcess):

    def __init__(self, url, class_mysql):
        super(SearchRacesProcess, self).__init__(url, class_mysql)

    def class_set(self, url):
        self.race_scraping = RaceScraping(url)

    def set_search_info(self, start_year, end_year, jyo):
        """
        検索パラメーターのセット
        :param start_year: str
        :param end_year: str
        :param jyo: str
        """
        self.start_year = start_year
        self.end_year = end_year
        self.jyo = jyo

    def get_data(self):
        """
        POSTメゾットでレース情報の取得
        :return: list: Races URL
        """
        self.race_scraping.create_header_data(
                                        self.start_year,
                                        self.end_year,
                                        self.jyo
                                        )
        html_data = self.race_scraping.request_post_method()
        self.search_race = Races(html_data)
        urls = self.search_race.get_target_races()
        return urls


class RaceDetailsProcess(BaseRaceProcess):

    def __init__(self, url, class_mysql):
        super(RaceDetailsProcess, self).__init__(url, class_mysql)
        self.url = url
        self.insert = Insert(class_mysql)
        self.select_from_jockeys = SelectFromJockeys(class_mysql)
        self.select_from_horses = SelectFromHorses(class_mysql)
        self.select_from_races = SelectFromRaces(class_mysql)

    def class_set(self, url):
        self.race_details_scraping = RaceDetailsScraping(url)

    def get_data(self):
        html_data = self.race_details_scraping.request_get_method()
        self.race_details = RaceDetails(html_data)

    def get_horses(self):
        return self.race_details.get_horse_urls()

    def get_race_detail(self):
        return self.race_details.get_race_details()

    def edit_race_details(self, race_details):
        self.details = []
        for race_detail in race_details:
            race_detail[0] = self.race_details.arrival_to_integer(race_detail[0])
            race_detail[1] = self.race_details.string_to_integer(race_detail[1])
            race_detail[3] = self.race_details.string_to_float(race_detail[3])
            race_detail[5] = self.race_details.time_to_integer(race_detail[5])
            race_detail[6] = self.race_details.close_dictant(race_detail[6])
            race_detail[7] = self.race_details.through_to_list(race_detail[7])
            race_detail[8] = self.race_details.string_to_float(race_detail[8])
            race_detail[9] = self.race_details.string_to_float(race_detail[9])
            race_detail[10] = self.race_details.string_to_integer(race_detail[10])
            race_detail[11] = self.race_details.horse_wight_and_gain_and_loss_to_integer(race_detail[11])
            self.details.append(race_detail)
        return self.details

    def get_refund(self):
        return self.race_details.get_refund()

    def get_race_info(self):
        return self.race_details.get_race_info()

    def get_race_status(self):
        return self.race_details.get_race_status()

    def get_class(self):
        return self.race_details.get_race_class()

    def sql_process_race(self, race_name, class_id, day_at_race, place_id, day, weather_id, distance_id, type_id):
        self.insert.execute_insert(self.insert.into_races_values, race_name,
                                   self.url, class_id, day_at_race, place_id, day,
                                   weather_id, distance_id, type_id)

    def sql_process_race_details(self, detail):
        # レースIDを探す
        self.sql_process_get_race_id()
        # 馬IDを探す
        self.sql_process_get_horse_id("https://db.netkeiba.com" + detail[2])
        # 騎手IDを探す
        self.sql_process_get_jockey_id(detail[4])
        # 騎手IDがない場合は登録
        if bool(self.jockey_id) is False:
            self.sql_process_jockey(detail[4])
            self.sql_process_get_jockey_id(detail[4])
        if detail[5] is None:
            self.insert.execute_insert(self.insert.into_race_details_values,
                                       self.race_id[0][0], self.horse_id[0][0],
                                       self.jockey_id[0][0], None, None,
                                       None, None, None, None,
                                       None, None, None, None,
                                       None, None, None, None)
        elif detail[7] is None:
            self.insert.execute_insert(self.insert.into_race_details_values,
                                       self.race_id[0][0], self.horse_id[0][0],
                                       self.jockey_id[0][0], detail[11][0], detail[11][1],
                                       detail[3], detail[1], detail[0], detail[5],
                                       detail[6], detail[8], detail[10], detail[9],
                                       None, None, None, None)
        elif len(detail[7]) == 1:
            self.insert.execute_insert(self.insert.into_race_details_values,
                                       self.race_id[0][0], self.horse_id[0][0],
                                       self.jockey_id[0][0], detail[11][0], detail[11][1],
                                       detail[3], detail[1], detail[0], detail[5],
                                       detail[6], detail[8], detail[10], detail[9],
                                       detail[7][0], None, None, None)
        elif len(detail[7]) == 2:
            self.insert.execute_insert(self.insert.into_race_details_values,
                                       self.race_id[0][0], self.horse_id[0][0],
                                       self.jockey_id[0][0], detail[11][0], detail[11][1],
                                       detail[3], detail[1], detail[0], detail[5],
                                       detail[6], detail[8], detail[10], detail[9],
                                       detail[7][0], detail[7][1], None, None)
        elif len(detail[7]) == 3:
            self.insert.execute_insert(self.insert.into_race_details_values,
                                       self.race_id[0][0], self.horse_id[0][0],
                                       self.jockey_id[0][0], detail[11][0], detail[11][1],
                                       detail[3], detail[1], detail[0], detail[5],
                                       detail[6], detail[8], detail[10], detail[9],
                                       detail[7][0], detail[7][1], detail[7][2], None)
        elif len(detail[7]) == 4:
            self.insert.execute_insert(self.insert.into_race_details_values,
                                       self.race_id[0][0], self.horse_id[0][0],
                                       self.jockey_id[0][0], detail[11][0], detail[11][1],
                                       detail[3], detail[1], detail[0], detail[5],
                                       detail[6], detail[8], detail[10], detail[9],
                                       detail[7][0], detail[7][1], detail[7][2], detail[7][3])

    def sql_process_betting_detail(self, detail):

        if bool(detail["複勝"]) is not False:
            if len(detail["複勝"]) > 9:
                return
        print(detail)
        if bool(detail["単勝"]) is not False:
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 1, detail["単勝"][2], detail["単勝"][1],
                                       detail["単勝"][0], None, None)
        if bool(detail["枠連"]) is not False:
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 3, detail["枠連"][2], detail["枠連"][1],
                                       detail["枠連"][0][0], detail["枠連"][0][1], None)
        if bool(detail["馬連"]) is not False:
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 4, detail["馬連"][2], detail["馬連"][1],
                                       detail["馬連"][0][0], detail["馬連"][0][1], None)
        if bool(detail["馬単"]) is not False:
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 6, detail["馬単"][2], detail["馬単"][1],
                                       detail["馬単"][0][0], detail["馬単"][0][1], None)
        if bool(detail["三連複"]) is not False:
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 7, detail["三連複"][2], detail["三連複"][1],
                                       detail["三連複"][0][0], detail["三連複"][0][1], detail["三連複"][0][2])
        if bool(detail["三連単"]) is not False:
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 8, detail["三連単"][2], detail["三連単"][1],
                                       detail["三連単"][0][0], detail["三連単"][0][1], detail["三連単"][0][2])
        if bool(detail["複勝"]) is not False:
            if len(detail["複勝"]) == 9:
                self.insert.execute_insert(self.insert.into_betting_details_values,
                                           self.race_id[0][0], 2, detail["複勝"][6], detail["複勝"][3],
                                           detail["複勝"][0], None, None)
                self.insert.execute_insert(self.insert.into_betting_details_values,
                                           self.race_id[0][0], 2, detail["複勝"][7], detail["複勝"][4],
                                           detail["複勝"][1], None, None)
                self.insert.execute_insert(self.insert.into_betting_details_values,
                                           self.race_id[0][0], 2, detail["複勝"][8], detail["複勝"][5],
                                           detail["複勝"][2], None, None)
            if len(detail["複勝"]) == 6:
                self.insert.execute_insert(self.insert.into_betting_details_values,
                                           self.race_id[0][0], 2, detail["複勝"][4], detail["複勝"][2],
                                           detail["複勝"][0], None, None)
                self.insert.execute_insert(self.insert.into_betting_details_values,
                                           self.race_id[0][0], 2, detail["複勝"][5], detail["複勝"][3],
                                           detail["複勝"][1], None, None)
        if bool(detail["ワイド"]) is not False and len(detail["ワイド"]) < 9:
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 5, detail["ワイド"][6], detail["ワイド"][3],
                                       detail["ワイド"][0][0], detail["ワイド"][0][1], None)
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 5, detail["ワイド"][7], detail["ワイド"][4],
                                       detail["ワイド"][1][0], detail["ワイド"][1][1], None)
            self.insert.execute_insert(self.insert.into_betting_details_values,
                                       self.race_id[0][0], 5, detail["ワイド"][8], detail["ワイド"][5],
                                       detail["ワイド"][2][0], detail["ワイド"][2][1], None)

    def sql_process_jockey(self, url):
        self.insert.execute_insert(self.insert.into_jockeys_values, None, url)

    def sql_process_get_horse_id(self, url):
        self.horse_id = self.select_from_horses.execute_select(self.select_from_horses.where_horse_id,
                                                               url)

    def sql_process_get_race_id(self):
        self.race_id = self.select_from_races.execute_select(
            self.select_from_races.where_url, self.url
        )

    def sql_process_get_jockey_id(self, url):
        self.jockey_id = self.select_from_jockeys.execute_select(self.select_from_jockeys.where_url,
                                                                 url)
