from DataBase.db_by_python import ToMysqlByPython
from StringWords.ather import Message
from ExcuteProcess.horse import process as process
from StringWords.error import MaleUrlsMessage
from StringWords.error import ProcessMessage
from logs.log_write import Logs
import time


def main():
    """
    Test main function

    DataBase = ToMysqlByPython()
    mysql_ob = DataBase.connect()
    i = Insert(mysql_ob)
    i.insert_into_horses('test', '牡', '2019-10-10')
"""

    logs = Logs()
    logs.write_start()
    # データベース接続
    sql = ToMysqlByPython()
    OBJECT_MYSQL, connection_result = sql.connects()
    if connection_result is True:
        print(Message.success_connection)
        logs.write_message(Message.success_connection)
    else:
        print(Message.error_connection)
        logs.write_message(Message.error_connection)
        return

    # 対象URL  作成しセット
    url = "https://db.netkeiba.com/horse/2017105092/"
    target_urls = []
    target_male_urls = []
    male_horse = None
    male_horse_dict = {}
    times = 1

    target_urls.append(url)

    while bool(target_urls):
        for url in target_urls:
            if url is None:
                continue
            if times % 1000:
                pass
            else:
                time.sleep(60)
            print("対象：", url)
            # 子馬処理セット
            children_horse = process.ChildrenHorse(url, OBJECT_MYSQL)
            # 仔馬の情報取得
            children_horse.get_info()
            # 仔馬情報表示
            children_horse.debug()
            # 調教師情報登録
            children_horse.sql_trainer_process()
            # 馬主登録
            children_horse.sql_owner_process()
            # 仔馬のデータ登録 ※あればしない
            children_horse.sql_process_horses()
            # 父馬と母馬のURLセット
            children_horse_male_urls = children_horse.get_male_horses()
            try:
                if children_horse_male_urls[0] is not None:
                    target_male_urls.append(children_horse_male_urls[0])
                if children_horse_male_urls[3] is not None:
                    target_male_urls.append(children_horse_male_urls[3])
            except IndexError as e:
                # URL作成へ
                if bool(target_male_urls[0]) is False:
                    logs.write_error(e, 62)
                else:
                    logs.write_error(e, 64)
            # 親を順番に登録済か確認して登録していく
            for index, male_url in enumerate(target_male_urls):
                # 親馬のURLをセット
                male_horse = process.MaleHorse(male_url, OBJECT_MYSQL)
                # 馬の情報取得
                male_horse.get_info()
                # 親馬情報表示
                male_horse.debug()
                # 調教師登録
                male_horse.sql_trainer_process()
                # 馬主登録
                male_horse.sql_owner_process()
                # 親馬の情報があるかデータベース確認
                # 親馬がなければ登録
                if bool(male_horse.male_only_process()) is False:
                    # 親馬登録
                    male_horse.sql_process_horses()
                    already_recorded_of_male_horses = False
                else:
                    already_recorded_of_male_horses = male_horse.find_male_horses()

                # 親馬の詳細情報をリストに格納
                male_horse_info = [male_horse.gender,               # 親馬の性別
                                   male_horse.url,                  # 親馬のURL
                                   already_recorded_of_male_horses  # 親馬の血統情報がすで登録されていたか
                                   ]
                # 親馬の情報を辞書に格納
                male_horse_dict[index] = male_horse_info
                # 変数空にする
                male_horse = None
                already_recorded_of_male_horses = None
                male_horse_already_recorded = None
                # 血統登録
                # 辞書の長さから何頭登録するか確認
                if len(male_horse_dict) == 2:
                    # gender情報が牡か牝かで引数を変える
                    if male_horse_dict[0][0] == 1 or male_horse_dict[1][0] == 2:
                        children_horse.sql_process_male(male_horse_dict[0][1],
                                                        male_horse_dict[1][1])
                    elif male_horse_dict[0][0] == 2 or male_horse_dict[1][0] == 1:
                        children_horse.sql_process_male(male_horse_dict[1][1],
                                                        male_horse_dict[0][1])
                    elif male_horse_dict[0][0] is None and male_horse_dict[1][0] is None:
                        children_horse.sql_process_male(male_horse_dict[0][1],
                                                        male_horse_dict[1][1])
                    else:
                        logs.write_secret_error(children_horse)
                    # 次の対象を親馬にURLを追加
                    if male_horse_dict[0][2] is not True:
                        target_urls.append(male_horse_dict[0][1])
                    if male_horse_dict[1][2] is not True:
                        target_urls.append(male_horse_dict[1][1])
                elif len(male_horse_dict) == 1:
                    if male_horse_dict[0][0] == 1:
                        children_horse.sql_process_male(male_horse_dict[0][1],
                                                        None)
                    elif male_horse_dict[0][0] == 2:
                        children_horse.sql_process_male(None,
                                                        male_horse_dict[0][1])
                    else:
                        logs.write_secret_error(children_horse)
                    if male_horse_dict[0][2] is not True:
                        target_urls.append(male_horse_dict[0][1])
                elif len(male_horse_dict) == 0:
                    children_horse.sql_process_male(None,
                                                    None)
                    print("最後まで行ったよ")
                else:
                    print(ProcessMessage.can_not_find_isue)
                male_horse_dict.clear()
                target_male_urls.clear()
                print("\n")
                times += 1

            target_urls.clear()
    print("終了だよ")


if __name__ == "__main__":
    main()
