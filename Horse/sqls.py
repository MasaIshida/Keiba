

class InsertSQL():
    sql = " INSERT               " \
          "   INTO               " \
          "          HORSES      " \
          "     (                " \
          "          horse_name, " \
          "              gender, " \
          "               birth, " \
          "                 url, " \
          "          trainer_id, " \
          "            owner_id  " \
          "      )               " \
          " VALUES               " \
          "  (%s,%s,%s,%s,%s,%s);"


class InsertMaleHorses():
    sql = " INSERT               " \
          "   INTO               " \
          "        MALE_HORSES   " \
          "     (                " \
          "           horse_id,  " \
          "      sire_horse_id,  " \
          "       dam_horse_id   " \
          "      )               " \
          " VALUES               " \
          "      (%s,%s,%s);     "


class InsertTrainers():
    sql = " INSERT             " \
          "   INTO             " \
          "          TRAINERS  " \
          "       (            " \
          "      trainer_name, " \
          "               url  " \
          "        )           " \
          "  VALUES            " \
          "        (%s, %s);   "


class InsertOwners():
    sql = " INSERT             " \
          "   INTO             " \
          "            OWNERS  " \
          "       (            " \
          "        owner_name, " \
          "               url  " \
          "        )           " \
          "  VALUES            " \
          "        (%s, %s);   "


class SelectUrlFromHorses():
    sql = "SELECT              " \
          "               URL  " \
          "  FROM              " \
          "             HORSES " \
          " WHERE              " \
          "        URL = (%s); "


class SelectHorseIdFromHorse():
    sql = "SELECT              " \
          "          HORSE_ID  " \
          "  FROM              " \
          "            HORSES  " \
          " WHERE              " \
          "        URL = (%s); "


class SelectHorseIdFromMaleHorses():
    sql = "SELECT              " \
          "          HORSE_ID  " \
          "  FROM              " \
          "        MALE_HORSES " \
          " WHERE              " \
          "   HORSE_ID = (%s); "


class SelectTrainerIdFromTrainers():
    sql = "SELECT               " \
          "         TRAINER_ID  " \
          "  FROM               " \
          "           TRAINERS  " \
          " WHERE               " \
          "          URL= (%s); "


class SelectTrainerIdFromOwner():
    sql = "SELECT               " \
          "           OWNER_ID  " \
          "  FROM               " \
          "             OWNERS  " \
          " WHERE               " \
          "          URL= (%s); "
