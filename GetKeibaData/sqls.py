

class SelectRaceDataFromRaces():
    sql = "SELECT           " \
          "              *  " \
          "  FROM           " \
          "          RACES  " \
          " WHERE           " \
          "    race_id=(%s);"


class SelectHorseDataFromHorses():
    sql = "SELECT           " \
          "              *  " \
          "  FROM           " \
          "         HORSES  " \
          " WHERE           " \
          "        url=(%s);"


class SelectJockeyIDFromRiders():
    sql = "SELECT           " \
          "       rider_id  " \
          "  FROM           " \
          "        JOCKEYS  " \
          " WHERE           " \
          "        url=(%s);"
