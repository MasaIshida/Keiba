from DataBase.db_by_python import ToMysqlByPython
from StringWords.ather import Message
from GetKeibaData.sql_sentence import ExecuteQuery
from GetKeibaData.web_scraping import NowRaceScraping
from GetKeibaData.get_now_race_data import HoldRaces
from GetKeibaData.get_now_race_data import TargetRaces
from GetKeibaData.get_now_race_data import ThisMomentRace
from GetKeibaData.get_now_race_data import ArimaKinen
from GetKeibaData.sqls import SelectHorseDataFromHorses
from LearningJsonData.sql_sentence import Select
import datetime
import numpy as np
import os

import pickle

import zipfile

import shutil



def main():
    sql = ToMysqlByPython()
    OBJECT_MYSQL, connection_result = sql.connects()
    if connection_result is True:
        print(Message.success_connection)
    else:
        print(Message.error_connection)
        return
    execute_query = ExecuteQuery(OBJECT_MYSQL)

    # htmlデータを取得
    now_race_scraping = NowRaceScraping("https://race.netkeiba.com/?pid=race_list")
    html_data = now_race_scraping.request_get_method()

    hold_races = HoldRaces(html_data)
    urls = hold_races.get_hold_date()
    print(urls)
    for url in urls:
        now_race_scraping = NowRaceScraping("https://race.netkeiba.com" + url)
        target_races = TargetRaces(now_race_scraping.request_get_method())
        target_races_urls = target_races.get_this_day_races()
        for target_url in target_races_urls:
            now_race_scraping = NowRaceScraping(target_url)
            this_moment_race = ThisMomentRace(now_race_scraping.request_get_method())
            this_moment_race.get_type_id_and_distance_id_and_class_id()

    result = execute_query.get_race_data(1)


def main_2():
    # race_table_old nk_tb_common
    # 有馬記念のみ対応

    np.set_printoptions(precision=100, suppress=True, formatter={'float': '{: 0.3f}'.format})

    label_dict = {}

    sql = ToMysqlByPython()
    OBJECT_MYSQL, connection_result = sql.connects()

    execute_query = ExecuteQuery(OBJECT_MYSQL)
    select = Select(OBJECT_MYSQL)

    if connection_result is True:
        print(Message.success_connection)
    else:
        print(Message.error_connection)
        return

    # フォルダ作成の為のここのパス取得
    arima_dir_path = os.getcwd() + "/Arima_data/"

    now_race_scraping = NowRaceScraping("https://race.netkeiba.com/?pid=race_old&id=c201906050811")
    html_data = now_race_scraping.request_get_method()
    arima_kinen = ArimaKinen(html_data)

    # 出走馬の情報取得
    details = arima_kinen.get_race_detail()

    # 有馬用のarryセット
    arima_arr = np.zeros([1, 28], dtype=np.float32)

    arima_syusou_list = []

    for detail in details:

        horse_data = execute_query.get_horse_data(detail[1])

        jockey_id = execute_query.get_jockey_data(detail[3].replace("https://db.netkeiba.com", ""))

        data = create_arima_predict_list(horse_data, jockey_id, detail)

        #  後に見やすくする為辞書作成
        label_dict[horse_data[0][0]] = horse_data[0][1]

        # 出走馬のデータを一時保管
        arima_syusou_list.append(horse_data[0])

        # 有馬のデータを作成
        arima_arr = np.r_['0', arima_arr, np.array([data])]

    arima_arr = np.delete(arima_arr, 0, 0)

    # 出走馬が18頭に満たない分をダミーで補う
    for _ in range(2):
        # ダミーデータ作成
        result_detail_record = [0 for i in range(28)]
        result_horse_record = [0 for i in range(18)]

        data = create_arima_predict_list([result_horse_record], [["0"]], result_detail_record)
        arima_arr = np.r_['0', arima_arr, np.array([data])]

    print(arima_arr.shape)

    # 出走馬のこれまで出走履歴作成
    for horse_data in arima_syusou_list:

        print(horse_data)
        race_arr = np.zeros([1, 18, 28])

        # 出走馬のこれまでの出走したレースのIDを取得
        result_race_id_records = select.execute_select(select.get_races_details_records_horse_id, horse_data[0])
        not_enough_race = 80 - len(result_race_id_records)
        if not_enough_race < 0:
            print("出走レース数", not_enough_race)
            return

        # レースごとに詳細を作成
        for cnt, race_id in enumerate(result_race_id_records):

            # レースレコード取得
            result_race_record = select.execute_select(select.get_race_record, race_id[0])

            # レース詳細レコード取得
            result_race_details_records = select.execute_select(select.get_races_details_records, race_id[0])

            not_enough_detail = 18 - len(result_race_details_records)

            detail_arr = np.zeros([1, 28], dtype=np.float32)

            for detail_record in result_race_details_records:

                race_detail_list = []

                result_horse_record = select.execute_select(select.get_horse_record, detail_record[2])
                data_list = create_data_list(result_race_record, detail_record, result_horse_record)
                race_detail_list.append(data_list)

                # 詳細行列に結合する
                detail_arr = np.r_['0', detail_arr, np.array(race_detail_list)]

            # 出走数が18頭に満たない分を作成する
            for _ in range(0, not_enough_detail):

                race_detail_list = []

                result_detail_record = [0 for i in range(28)]
                result_horse_record = [0 for i in range(28)]
                data_list = create_data_list(result_race_record, result_detail_record, [result_horse_record])
                race_detail_list.append(data_list)

                # 満たない分を結合
                detail_arr = np.r_['0', detail_arr, np.array(race_detail_list)]

            detail_arr = np.delete(detail_arr, 0, 0)

            # 詳細ができた為レースの行列に挿入（結合）
            race_arr = np.r_['0, 3', race_arr, detail_arr]

        # 出走履歴が60回に満たない分をダミーで作成
        for _ in range(0, not_enough_race - 1):

            detail_arr = np.zeros([1, 28])

            for __ in range(18):
                race_detail_list = []

                dummy_detail_record = [0 for i in range(28)]
                race_detail_list.append(dummy_detail_record)

                detail_arr = np.r_['0', detail_arr, np.array(race_detail_list)]

            detail_arr = np.delete(detail_arr, 0, 0)

            race_arr = np.r_['0, 3', race_arr, detail_arr]

        race_arr = np.delete(race_arr, 0, 0)

        race_arr = np.r_['0, 3', race_arr, arima_arr]

        pred_arr = np.zeros([1, 80, 18, 28])

        pred_arr = np.delete(pred_arr, 0, 0)

        pred_arr = np.r_['0, 4', pred_arr, race_arr]

        # バイナリーデータを保存するパス作成
        target_path = arima_dir_path + "horse_" + str(horse_data[0])

        # 保存する為のディレクトリ作成
        try:
            os.mkdir(target_path)
        except FileExistsError:
            pass

        # バイナリーデータ作成
        create_binary_file(target_path + "/", "pred" + str(horse_data[0]), pred_arr)

    create_dict_file(arima_dir_path, label_dict)

    print("終了しました")


def create_data_list(result_race_record, result_detail_record, result_horse_record):
    data_list = [float(0) for i in range(28)]
    data_list[0] = float(add_data(result_race_record[0][0]))  # race_id
    data_list[1] = float(add_data(result_detail_record[2]))   # horse_id
    data_list[2] = float(add_data(result_detail_record[3]))   # rider_id
    data_list[3] = float(add_data(result_detail_record[4]))   # horse_wight
    data_list[4] = float(normalization(result_detail_record[5],
                                       result_detail_record[4]))  # gain_and_loss
    data_list[5] = float(add_data(result_detail_record[6]))  # dreging
    data_list[6] = float(add_data(result_detail_record[7]))  # entry_number
    data_list[7] = float(add_data(result_detail_record[8]))  # arrival
    data_list[8] = float(add_data(result_detail_record[9]))  # arrival_time
    data_list[9] = float(add_data(result_detail_record[10]))  # close_distant
    data_list[10] = float(add_data(result_detail_record[11]))  # lats_time
    data_list[11] = float(add_data(result_detail_record[12]))  # popular
    data_list[12] = float(add_data(result_detail_record[13]))  # odds
    data_list[13] = float(add_data(result_detail_record[14]))  # thorough1
    data_list[14] = float(add_data(result_detail_record[15]))  # thorough2
    data_list[15] = float(add_data(result_detail_record[16]))  # thorough3
    data_list[16] = float(add_data(result_detail_record[17]))  # thorough4
    data_list[17] = float(add_data(result_race_record[0][1]))  # class_id
    data_list[18] = float(add_data(result_race_record[0][3]))  # place_id
    data_list[19] = float(add_data(result_race_record[0][5]))  # weather_id
    data_list[20] = float(add_data(result_race_record[0][2]).month)  # month
    data_list[21] = float(add_data(result_race_record[0][4]))  # day
    data_list[22] = float(add_data(result_race_record[0][6]))  # distance_id
    data_list[23] = float(add_data(result_race_record[0][7]))  # type_id
    data_list[24] = float(add_data(result_horse_record[0][0]))  # gender_id
    data_list[25] = float(add_data(result_horse_record[0][2]))  # trainer_id
    data_list[26] = float(add_data(result_horse_record[0][3]))  # owner_id
    data_list[27] = float(how_old(result_horse_record[0][1], result_race_record[0][2]))  # old
    return data_list


def create_arima_predict_list(horse_data, rider_id, detail):
    data_list = [float(0) for i in range(28)]
    data_list[0] = float(30000)  # race_id
    data_list[1] = float(horse_data[0][0])  # horse_id
    data_list[2] = float(rider_id[0][0])  # rider_id
    data_list[3] = float(0)
    data_list[4] = float(0)
    data_list[5] = float(detail[2])  # dreging
    data_list[6] = float(detail[0])  # entry_number
    data_list[7] = float(0)
    data_list[8] = float(0)
    data_list[9] = float(0)
    data_list[10] = float(0)
    data_list[11] = float(0)
    data_list[12] = float(0)
    data_list[13] = float(0)
    data_list[14] = float(0)
    data_list[15] = float(0)
    data_list[16] = float(0)
    data_list[17] = float(10)  # class_id
    data_list[18] = float(6)  # place_id
    data_list[19] = float(0)
    data_list[20] = float(12)  # month
    data_list[21] = float(8)  # day
    data_list[22] = float(17)  # distance_id
    data_list[23] = float(1)  # type_id
    data_list[24] = float(horse_data[0][2])  # gender_id
    data_list[25] = float(horse_data[0][5])  # trainer_id
    data_list[26] = float(horse_data[0][6])  # owner_id
    data_list[27] = float(how_old(horse_data[0][3], datetime.datetime.now()))  # old
    return data_list


def add_data(data):
    if data is None:
        return 0
    return data


def normalization(data1, data2):
    if data1 is None or data2 is None or data1 == 0 or data2 == 0:
        return 0
    return 1 + (data1/data2)


def how_old(birth, at_race):
    if birth is None or at_race is None:
        return 0
    elif birth == 0 or at_race == 0:
        return 0
    return int(at_race.year) - int(birth.year)


def create_binary_file(path, pred_file_name, pred_data):
    with open(path + pred_file_name + ".binaryfile", "wb") as fout:
        pickle.dump(pred_data, fout)


def create_dict_file(path, dict_data):
    with open(path + "horse_dict.binaryfile", "wb") as fout:
        pickle.dump(dict_data, fout)


def create_zip_file(file_path):
    shutil.make_archive(file_path, 'zip', root_dir='data/temp/dir')


if __name__ == "__main__":
    main_2()
