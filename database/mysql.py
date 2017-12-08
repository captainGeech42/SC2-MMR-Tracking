import MySQLdb
from starcraft import Ladder, Player


class MySQL:
    host = "localhost"
    port = 3306
    username = "root"
    password = "1234asdf"
    database = "starcraft"

    def __init__(self):
        self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.username, passwd=self.password,
                                  db=self.database)
        self.cursor = self.db.cursor()

    def add_player(self, player: Player):
        ladders = {"protoss": ["", 0], "random": ["", 0], "terran": ["", 0], "zerg": ["", 0]}
        for team in player.ladders:
            ladders[team.race.lower()] = [team.league, team.mmr]

        query = (
            "INSERT INTO players (battletag, server, p_league, p_mmr, r_league, r_mmr, t_league, t_mmr, z_league,"
            "z_mmr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        num_rows = self.cursor.execute(query, player.battletag, player.region,
                                       ladders["protoss"][0], ladders["protoss"][1],
                                       ladders["random"][0], ladders["random"][1],
                                       ladders["terran"][0], ladders["terran"][1],
                                       ladders["zerg"][0], ladders["zerg"][1])

        self.db.commit()

        return num_rows

    def add_ladder(self, ladder: Ladder):
        leagues = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]

        query = (
            "INSERT INTO ladders (id, server, league, division, floor, ceiling) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )

        num_rows = self.cursor.execute(query, ladder.id, ladder.region, leagues[ladder.league_id], ladder.division,
                                       ladder.min_mmr, ladder.max_mmr)

        self.db.commit()

        return num_rows

    def close(self):
        self.db.close()
