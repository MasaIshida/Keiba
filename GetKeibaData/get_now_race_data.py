import datetime
import re

from StringWords.data_words import Gender
from StringWords import tags


class NowRacesObject(object):

    def __init__(self, html_data):
        self.html_data = html_data


class HoldRaces(NowRacesObject):

    def __init__(self, html_data):
        super(HoldRaces, self).__init__(html_data)

    def get_hold_date(self):
        urls = []
        date_list = self.html_data.find(id=tags.Target.hold_date_list)
        for dd in date_list.find_all("dd"):
            if is_now_race(dd.a.get("title")):
                urls.append(dd.a.get("href"))
        return urls


def is_now_race(string_date):
    split_date = string_date.split("(")
    datetime_data = datetime.datetime.strptime(split_date[0], "%m/%d")
    days = (datetime.date(2019, datetime_data.month, datetime_data.day) - datetime.date(
        datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)).days
    if days < 0:
        return 0
    return 1


class TargetRaces(NowRacesObject):

    def __init__(self, html_data):
        super(TargetRaces, self).__init__(html_data)

    def get_this_day_races(self):
        urls = []
        race_list_area = self.html_data.find(class_=tags.Target.this_day_races)
        for races in race_list_area.find_all(class_=tags.Target.this_races_list):
            for race in races.find_all("li"):
                urls.append("https://race.netkeiba.com" + race.find(class_="racename").a.get("href"))
        return urls


class ThisMomentRace(NowRacesObject):

    def __init__(self, html_data):
        super(ThisMomentRace, self).__init__(html_data)

    def get_type_id_and_distance_id_and_class_id(self):
        # 芝ダと距離情報取得
        dd = self.html_data.find(class_="racedata fc").dd
        self.distance_id = find_distance_id(dd.p)
        self.type_id = find_type_id(dd.p)
        title = self.html_data.find("title")
        self.class_is = get_race_class(title)


def find_distance_id(distance_data):
    distances = ["1000", "1100", "1150", "1200", "1300", "1400", "1500", "1600",
                 "1700", "1800", "1900", "2000", "2100", "2200", "2300", "2400",
                 "2500", "2600", "3000", "3200", "3400", "3600"]
    for distance in distances:
        if distance in distance_data.string:
            return distances.index(distance) + 1
    return None


def get_race_class(class_data):
    grades = ["OP", "G3", "G2", "G1"]
    grade_info = class_data.string
    for grade in grades:
        if grade in class_data:
            return grades.index(grade) + 8
    flats = ["未出走", "未勝利", "新馬", "500万", "1000万", "1600万", "オープン"]

    for flat in flats:
        if flat in grade_info:
            return flats.index(flat) + 1
    if "１勝" in grade_info:
        return 4
    if "２勝" in grade_info:
        return 5
    return None


def find_type_id(type_data):
    if "芝" in type_data.string:
        return 1
    elif "ダ" in type_data.string:
        return 2
    else:
        return None


def get_race_info(info_data):
    """
    レース情報取得
    :return: 開催日, 会場ID, 何回目, 何日目, レース名

    places = ['札幌', '函館', '福島', '新潟', '東京', '中山', '中京', '京都', '阪神', '小倉']
    for place in places:
        if place in data[1]:
            place_id = places.index(place) + 1
            break
    r = data[1].split("回")
    return self.edit_date(data[0]), place_id, int(r[0]), int(r[1].replace(place, "").replace("日目", "")), data[2].replace("\xa0", "")
    """


class ArimaKinen(NowRacesObject):

    def __init__(self, html_data):
        super(ArimaKinen, self).__init__(html_data)

    def get_race_detail(self):
        detail = []
        table = self.html_data.find(class_="race_table_old nk_tb_common")
        for t in table.find_all(class_="bml1"):
            uma_num = t.find(class_="umaban").string
            horse_url = t.find(class_="txt_l horsename").div.a.get("href")
            dreging = t.find_all("td")[5].string
            rider_url = t.find_all("td")[6].a.get("href")
            detail.append([uma_num, horse_url, dreging, rider_url])
        return detail
