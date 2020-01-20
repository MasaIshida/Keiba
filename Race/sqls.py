

class InsertRaces():
    sql = " INSERT                    " \
          "   INTO                    " \
          "             RACES         " \
          "       (                   " \
          "         race_name,        " \
          "               url,        " \
          "          class_id,        " \
          "       day_at_race,        " \
          "          place_id,        " \
          "               day,        " \
          "        weather_id,        " \
          "       distance_id,        " \
          "           type_id         " \
          "        )                  " \
          "  VALUES                   " \
          "      (%s, %s, %s,         " \
          "       %s, %s, %s,         " \
          "       %s, %s, %s);        "


class InsertRaceDetails():
    sql = "  INSERT                  " \
          "    INTO                  " \
          "          RACES_DETAILS   " \
          "       (                  " \
          "                race_id,  " \
          "               horse_id,  " \
          "               rider_id,  " \
          "            horse_wight,  " \
          "          gain_and_loss,  " \
          "               dredging,  " \
          "           entry_number,  " \
          "                arrival,  " \
          "           arrival_time,  " \
          "          close_distant,  " \
          "              last_time,  " \
          "                popular,  " \
          "                   odds,  " \
          "               through1,  " \
          "               through2,  " \
          "               through3,  " \
          "               through4  " \
          "        )                 " \
          "  VALUES                  " \
          "        (%s, %s, %s,      " \
          "         %s, %s, %s,      " \
          "         %s, %s, %s,      " \
          "         %s, %s, %s,      " \
          "         %s, %s, %s,      " \
          "         %s, %s);         "


class InsertBettingDetails():
    sql = "  INSERT                  " \
          "    INTO                  " \
          "         BETTINGS_DETAILS " \
          "       (                  " \
          "                race_id,  " \
          "             betting_id,   " \
          "           betting_rank,  " \
          "           refund_price,  " \
          "               result_1,  " \
          "               result_2,  " \
          "               result_3   " \
          "        )                 " \
          "  VALUES                  " \
          "        (%s, %s, %s, %s,  " \
          "         %s, %s, %s);     "


class InsertJockeys():
    sql = "  INSERT                  " \
          "    INTO                  " \
          "                JOCKEYS   " \
          "       (                  " \
          "             rider_name,  " \
          "                    url   " \
          "        )                 " \
          "  VALUES                  " \
          "        (%s, %s);         "


class SelectJockeyIdFromJockeys():
    sql = " SELECT                   " \
          "              RIDER_ID   " \
          "   FROM                   " \
          "                JOCKEYS   " \
          "  WHERE                   " \
          "                URL=(%s); "


class SelectRaceIdFromRaces():
    sql = " SELECT                   " \
          "                RACE_ID   " \
          "   FROM                   " \
          "                  RACES   " \
          " WHERE                    " \
          "                 URL=(%s);"
