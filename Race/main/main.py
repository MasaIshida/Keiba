from DataBase.db_by_python import ToMysqlByPython
from Race.get_race_data import Races
from ExcuteProcess.race.data import Datas
from ExcuteProcess.race.process import SearchRacesProcess
from ExcuteProcess.race.process import RaceDetailsProcess
from StringWords.ather import Message
from logs.log_write import Logs


def main():

    logs = Logs()
    logs.write_start()
    sql = ToMysqlByPython()
    OBJECT_MYSQL, connection_result = sql.connects()

    if connection_result is True:
        print(Message.success_connection)
        logs.write_message(Message.success_connection)
    else:
        print(Message.error_connection)
        logs.write_message(Message.error_connection)
        return

    year_1986_to_2020 = Datas.year_range_1986_to_2020
    print(year_1986_to_2020)
    month_1_to_12 = Datas.month_range_1_to_12
    print(month_1_to_12)
    jyo_1_to_10 = Datas.jyo_range_1_to_10
    print(jyo_1_to_10)
    url = "https://db.netkeiba.com/?pid=race_search_detail"
    race_list = SearchRacesProcess(url, OBJECT_MYSQL)
    for year in year_1986_to_2020:
        for month in month_1_to_12:
            for jyo in jyo_1_to_10:
                race_list.set_search_info(year, month, jyo)
                race_urls = race_list.get_data()
                # テストprint
                if race_urls is not None:
                    for url in race_urls:
                        if url is not None:
                            print(url)
                            race_details_process = RaceDetailsProcess(url, OBJECT_MYSQL)
                            race_details_process.get_data()
                            #  Racesへ登録処理
                            day_at_race, place_id, times, day, name = race_details_process.get_race_info()
                            class_id = race_details_process.get_class()
                            type_id, distance_id, weather_id = race_details_process.get_race_status()
                            race_details_process.sql_process_race(
                                name, class_id, day_at_race,
                                place_id, day, weather_id, distance_id, type_id)

                            for horse_url in race_details_process.get_horses():
                                print(horse_url)
                            details = race_details_process.edit_race_details(
                                race_details_process.get_race_detail()
                            )
                            for detail in details:
                                race_details_process.sql_process_race_details(detail)
                            refund_detail = race_details_process.get_refund()
                            race_details_process.sql_process_betting_detail(refund_detail)


if __name__ == "__main__":
    main()