import datetime
import os


def add_write(context, file_name):
    with open(file_name, 'a') as f:
        f.write(context)


class Logs():

    def __init__(self):
        self.this_file_path = os.path.dirname(os.path.abspath(__file__))
        self.file_name = "run_log.log"
        self.log_file_path = os.path.join(self.this_file_path, self.file_name)

    def write_start(self):
        now_time = datetime.datetime.now()
        context = "取得開始時間 :" + str(now_time) + "\n"
        with open(self.log_file_path, 'w') as f:
            f.write(context)

    def write_message(self, message):
        add_write(message, self.log_file_path)

    def write_children_horse_info(self, name, gender, birth, url):
        now_time = datetime.datetime.now()
        context = "\n取得時間: {} \n" \
                  "仔馬名: {} \n" \
                  "性別: {} \n" \
                  "出生日: {} \n" \
                  "URL: {}\n".format(now_time,
                                     name,
                                     gender,
                                     birth,
                                     url)
        add_write(context, self.log_file_path)

    def write_male_horse_info(self, name, gender, birth, url):
        now_time = datetime.datetime.now()
        context = "\n取得時間: {} \n" \
                  "親馬名: {} \n" \
                  "性別: {} \n" \
                  "出生日: {} \n" \
                  "URL: {}\n".format(now_time,
                                     name,
                                     gender,
                                     birth,
                                     url)
        add_write(context, self.log_file_path)

    def write_race_url(self, url):
        context = "レースURL:  {}".format(url)
        add_write(context, self.log_file_path)

    def write_error(self, error, row):
        context = "{}行目で{}が発生しました".format(row, error)
        add_write(context, self.log_file_path)

    def write_secret_error(self, object):
        context = "\n \n 対象馬URL: {}\n" \
                  "対象馬の親のURLをページを確認して方がいいです".format(object.url)
        add_write(context, self.log_file_path)
