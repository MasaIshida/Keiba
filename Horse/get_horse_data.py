import datetime
import re


from StringWords.data_words import Gender
from StringWords import tags


class BaseHorseObject(object):

    def __init__(self, html_data):
        self.html_data = html_data


class Horse(BaseHorseObject):

    def __init__(self, html_data):
        super(Horse, self).__init__(html_data)

    def get_name_and_gender(self):
        """
        名前と性別取得
        :return: String: name : 馬名 or None
                 String : gender : 性別 or None
        """
        # 正規表現パターンセット ※カタカナ
        pattern_katakana = re.compile(r'[\u30A0-\u30FF]+')
        pattern_abc = re.compile('[a-zA-Z]+')

        name = None
        gender = None

        try:
            # 馬名が記載されているエリアを文字列だけセット
            horse_data = list(self.html_data.find(class_=tags.Target.horse_name).strings)

        except AttributeError as e:
            return None, None
        # 一文字づつカタカナがあるか確認
        for character in horse_data[1]:
            in_katakana = pattern_katakana.match(character)
            in_abc = pattern_abc.match(character)
            if in_katakana:
                # カタカナがあればnameに馬名をセット
                name = get_horse_name(horse_data)
                break
            if in_abc:
                name = get_horse_name(horse_data)
                break
        for data in horse_data:
            gender = find_gender(data)
            if gender is not None:
                break
        return name, gender

    def get_birth(self):
        """
        出生日の取得
        :return: datetime: 出生日
        """
        # 出生日が記載されているエリアを文字列でセット
        try:
            data_list = list(self.html_data.find(class_=tags.Target.prof_table).strings)

        except AttributeError as e:
            return None

        # 出生日が入っていなかった場合に備えて
        try:
            birth_data = datetime.datetime.strptime(data_list[4], "%Y年%m月%d日")

        except ValueError as e:
            return None

        if birth_data is not None:
            return datetime.date(year=birth_data.year,
                                 month=birth_data.month,
                                 day=birth_data.day)
        else:
            return None

    def get_blood(self):
        """
        直近3血統を取得
        :return: list: urls: 計6頭分のURL
        """
        urls = []
        blood_table = self.html_data.find(class_=tags.Target.blood)
        try:
            for tr in blood_table:
                if tr.find('a') is not -1:
                    for t in tr.find_all('a'):
                        url = t.get('href')
                        # ダミーではないか確認
                        if url != "/horse/ped//":
                            urls.append(url)
                        # ない又はダミーだった場合はNone
                        else:
                            urls.append(None)
            return urls

        except TypeError:
            return urls.append(None)

    def get_trainer(self):
        tables = self.html_data.find(class_=tags.Target.prof_table)
        for p in tables.find_all('td'):
            if p.a is not None:
                if 'trainer' in p.a.get('href'):
                    url = "https://db.netkeiba.com" + p.a.get('href')
                    trainer_name = p.a.get('title')
                    return url, trainer_name
        return None, None

    def get_owner(self):
        tables = self.html_data.find(class_=tags.Target.prof_table)
        for p in tables.find_all('td'):
            if p.a is not None:
                if 'owner' in p.a.get('href'):
                    url = "https://db.netkeiba.com" + p.a.get('href')
                    owner_name = p.a.get('title')
                    return url, owner_name
        return None, None


def get_horse_name(horse_datas):
    return horse_datas[1].replace('\u3000', '')


def find_gender(data):
    if Gender.male in data:
        return 1
    elif Gender.female in data:
        return 2
    elif Gender.kurama in data:
        return 3
    else:
        return None
