import re
import decimal
import datetime

from StringWords import tags


class BaseRaceObject(object):

    def __init__(self, html_data):
        self.html_data = html_data


class Races(BaseRaceObject):

    def __init__(self, html_data):
        super(Races, self).__init__(html_data)

    def get_target_races(self):
        """
        検索結果からレースのURLを返す
        :return: レースURL
        """
        urls = []
        pattern_hankakusuti = re.compile(r'[0-9]+$')
        table = self.html_data.find(class_=tags.Target.race_list_table)
        try:
            for td in table:
                if td.find('a') is not -1:
                    for t in td.find_all('a'):
                        href = t.get('href')
                        href_text = href.replace('/', '').replace('race', '')
                        is_race_url = pattern_hankakusuti.match(href_text)
                        if is_race_url:
                            url = "https://db.netkeiba.com" + href
                            urls.append(url)
            return urls

        except TypeError as e:
            return urls.append(None)


class RaceDetails(BaseRaceObject):

    def __init__(self, html_data):
        super(RaceDetails, self).__init__(html_data)

    def get_race_details(self):
        """
        レースの詳細情報を取得
        :return: 着順..etcのリスト
        """
        race_details_list = []
        table = self.html_data.find(class_=tags.Target.race_result_table)
        try:
            for i, tr in enumerate(table):
                if i == 0:
                    continue
                race_detail_list = []
                if tr.find("td") is not -1 and tr.find_all("td"):
                    for di, td in enumerate(tr.find_all("td")):
                        if self.is_ather_column(di):  # その他の値
                            race_detail_list.append(td.string)
                        elif self.is_horse_column(di):  # 馬名
                            race_detail_list.append(td.a.get("href"))
                        elif self.is_jockey_column(di):  # 騎手
                            race_detail_list.append(td.a.get("href"))
                    race_details_list.append(race_detail_list)
            return race_details_list
        except TypeError as e:
            pass

    def is_horse_column(self, index):
        return index == 3

    def is_jockey_column(self, index):
        return index == 6

    def is_ather_column(self, i):
        return i == 0 or i == 2 or i == 5 or i == 7 or i == 8 or i == 10 or i == 11 or i == 12 or i == 13 or i == 14

    def string_to_integer(self, string):
        """
        StringをIntegerへ変換する
        :param string:
        :return: Integerに型変換された数値
        """
        if string is None:
            return None
        pattern_hankakusuti = re.compile(r'[0-9]+$')
        if pattern_hankakusuti.match(string):
            return int(string)
        else:
            return None

    def arrival_to_integer(self, string):
        """
        着順をIntegerへ変換
        :param string:
        :return: Integerに型変換された数値
        """
        if string == "取" or string == "中" or string == "失" or string == "除":
            return 99
        elif "(再)" in string:
            return int(string.replace("(再)", ""))
        elif "(降)" in string:
            return int(string.replace("(降)",  ""))
        return int(string)

    def time_to_integer(self, time):
        """
        到着timeを数列に置き換える
        :param time:
        :return: 1:20:0 → 1200
        """
        if time is None:
            return None
        pattern_hankakusuti = re.compile(r'[0-9]+$')
        string_list = []
        for char in time:
            if pattern_hankakusuti.match(char):
                string_list.append(char)
        return int(','.join(string_list).replace(",", ""))

    def string_to_float(self, string):
        """
        文字列をデシマル型へ変換する
        :param string:
        :return: Decimal型の数値
        """
        if string is None:
            return None
        pattern_hankakusuti = re.compile(r'[0-9]+$')
        if pattern_hankakusuti.match(string.replace(".", "")):
            return float(string)
        return None

    def through_to_list(self, throughs):
        """
        通過順位を数値型のリストへ変換
        :param throughs:
        :return: [通過順位]
        """
        if throughs is None:
            return None
        elif "-" not in throughs:
            return None
        return [int(through) for through in throughs.split("-")]

    def horse_wight_and_gain_and_loss_to_integer(self, horse_wight):
        """
        馬体重を増減と分離してInteger型で返す
        :param horse_wight:
        :return: [馬体重 [増減]]
        """
        pattern_hankakusuti = re.compile(r'[0-9]+$')
        for char in horse_wight:
            if pattern_hankakusuti.match(char):
                wight_info = horse_wight.replace(")", "").split("(")
                return [int(wight_info[0]), int(wight_info[1])]
        if "計不" in horse_wight:
            return [None, None]
        return [None, None]

    def close_dictant(self, dictant):
        """
        着差を数値型に置き換える
        :param dictant:
        :return:数値
        """
        if dictant is None:
            return None
        if dictant == "ハナ":
            return 0.0625
        elif dictant == "アタマ":
            return 0.125
        elif dictant == "クビ":
            return 0.25
        elif dictant == "1/2":
            return 0.5
        elif dictant == "3/4":
            return 0.75
        elif dictant == "1":
            return 1
        elif "." in dictant and "+" in dictant:
            sum = 0
            re_dictant = dictant.replace(".", ",").replace("+", ",")
            dictant_split = re_dictant.split(",")
            for dic in dictant_split:
                sum += float(self.close_dict_replace(dic))
            return sum
        elif "."in dictant:
            dictant_split = dictant.split(".")
            if dictant_split[1] == "1/4":
                dictant_split[1] = 0.25
            elif dictant_split[1] == "1/2":
                dictant_split[1] = 0.5
            elif dictant_split[1] == "3/4":
                dictant_split[1] = 0.75
            return int(dictant_split[0]) + dictant_split[1]
        elif dictant == "大":
            return 8
        elif dictant == "同着":
            return 0
        elif dictant == "計不":
            return None
        elif "+" in dictant:
            re_dictant = self.close_dict_replace(dictant)
            sum = 0
            for num in re_dictant.split("+"):
                sum += float(num)
            return sum
        else:
            return int(dictant)

    def close_dict_replace(self, dictant):
        return dictant.replace("ハナ", "0.0625").replace("アタマ", "0.125").replace("クビ", "0.25").replace("1/2", "0.5").replace("1/4", "0.25").replace("3/4", "0.75")

    def get_horse_urls(self):
        """
        出走した馬のURLを返す
        :return: URL
        """
        urls = []
        table = self.html_data.find(class_=tags.Target.race_details_table)
        try:
            for td in table:
                if td.find('a') is not -1:
                    for t in td.find_all('a'):
                        href = t.get('href')
                        if '/horse/' in href:
                            url = "https://db.netkeiba.com" + href
                            urls.append(url)
            return urls

        except TypeError as e:
            return urls.append(None)

    def get_refund(self):
        """
        払い戻し情報を取得する
        :return: 辞書型の払い戻し情報
        """
        tables = self.html_data.find_all(class_=tags.Target.refund_table)
        tan = []
        huku = []
        waku = []
        uma_ren = []
        wide = []
        uma_tan = []
        sanren_puhu = []
        sanren_tan = []
        try:
            for tbody in tables:
                if tbody.find('tr') is not -1:
                    for tr in tbody.find_all('tr'):
                        if '単勝' in tr.find('th'):
                            for td in tr.find_all('td'):
                                tan.append(self.refund_string_to_integer(td.string))
                        elif '複勝' in tr.find('th'):
                            for td in tr.find_all('td'):
                                td_strings = list(td.strings)
                                for string in td_strings:
                                    huku.append(self.refund_string_to_integer(string))
                        elif '枠連' in tr.find('th'):
                            for td in tr.find_all('td'):
                                waku.append(self.refund_string_to_integer(td.string))
                        elif '馬連' in tr.find('th'):
                            for td in tr.find_all('td'):
                                uma_ren.append(self.refund_string_to_integer(td.string))
                        elif 'ワイド' in tr.find('th'):
                            for td in tr.find_all('td'):
                                td_strings = list(td.strings)
                                for string in td_strings:
                                    wide.append(self.refund_string_to_integer(string))
                        elif '馬単' in tr.find('th'):
                            for td in tr.find_all('td'):
                                uma_tan.append(self.refund_string_to_integer(td.string))
                        elif '三連複' in tr.find('th'):
                            for td in tr.find_all('td'):
                                sanren_puhu.append(self.refund_string_to_integer(td.string))
                        elif '三連単' in tr.find('th'):
                            for td in tr.find_all('td'):
                                sanren_tan.append(self.refund_string_to_integer(td.string))
        except TypeError as e:
            pass
        return {"単勝": tan, "複勝": huku, "枠連": waku, "馬連": uma_ren, "ワイド": wide, "馬単": uma_tan, "三連複": sanren_puhu, "三連単": sanren_tan}

    def refund_string_to_integer(self, string):
        """
        払い戻し情報を数値型に置き換える
        :param string:
        :return: 数値型の払い戻し情報
        """
        pattern_hankakusuti = re.compile(r'[0-9]+$')
        if pattern_hankakusuti.match(string):
            return int(string)
        elif "円" in string:
            if "," in string:
                return int(string.replace("円", "").replace(",",  ""))
            return int(string.replace("円", ""))
        elif "人気" in string:
            return int(string.replace("人気", ""))
        elif " - " in string:
            return [int(result) for result in string.replace(" ",  "").split("-")]
        elif " → " in string:
            return [int(result) for result in string.replace(" ",  "").split("→")]
        else:
            if "," in string:
                return int(string.replace(",", ""))

    def get_race_info(self):
        """
        レース情報取得
        :return: 開催日, 会場ID, 何回目, 何日目, レース名
        """
        places = ['札幌', '函館', '福島', '新潟', '東京', '中山', '中京', '京都', '阪神', '小倉']
        data = self.html_data.find(class_=tags.Target.race_info).string.split(" ")
        for place in places:
            if place in data[1]:
                place_id = places.index(place) + 1
                break
        r = data[1].split("回")
        return self.edit_date(data[0]), place_id, int(r[0]), int(r[1].replace(place, "").replace("日目", "")), data[2].replace("\xa0", "")

    def edit_date(self, date_data):
        if "年" in date_data and "月" in date_data and "日" in date_data:
            return datetime.datetime.strptime(date_data.replace("年", "-").replace("月", "-").replace("日", ""),
                                              '%Y-%m-%d').date()

    def get_race_class(self):
        grades = ["G3", "G2", "G1"]
        grade_info = self.html_data.find(class_=tags.Target.grade_info).h1
        for grade in grades:
            if grade in grade_info:
                return grades.index(grade) + 8
        flats = ["未出走", "未勝利", "新馬", "500万", "1000万", "1600万", "オープン"]
        data = self.html_data.find(class_=tags.Target.race_info).string.split(" ")
        for flat in flats:
            if flat in data[2]:
                return flats.index(flat) + 1
        if "1勝" in data[2]:
            return 4
        if "2勝" in data[2]:
            return 5
        return None

    def get_race_status(self):
        """
        レースステータス取得
        :return: 開催タイプ(芝、ダート), 距離, 天気
        """
        string = self.html_data.find(tags.Target.status_info).span.string
        status = string.replace("\xa0", "").split("/")
        type_id = self.find_type_id(status[0])
        distance_id = self.find_distance_id(status[0])
        weather_id = self.find_weather_id(status[1])
        return type_id, distance_id, weather_id

    def find_type_id(self, type_data):
        if "芝" in type_data:
            return 1
        elif "ダ" in type_data:
            return 2
        else:
            return None

    def find_distance_id(self, distance_data):
        distances = ["1000", "1100", "1150", "1200", "1300", "1400", "1500", "1600",
                     "1700", "1800", "1900", "2000", "2100", "2200", "2300", "2400",
                     "2500", "2600", "3000", "3200", "3400", "3600"]
        for distance in distances:
            if distance in distance_data:
                return distances.index(distance) + 1
        return None

    def find_weather_id(self, weather_data):
        weathers = ["晴", "曇", "雨", "小雨"]
        for weather in weathers:
            if weather in weather_data:
                return weathers.index(weather) + 1
        return None


class Jockey(BaseRaceObject):

    def __init__(self,  html_data):
        super(Jockey, self).__init__(html_data)

    def get_jocky_name_and_url(self):
        h = self.html_data.find(class_=tags.Target.jockey_name).h1.string
        if "\n" in h:
            return h.replace("\n", "")
        else:
            return h