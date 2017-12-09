import MySQLdb
from starcraft import Ladder, Player, Team


class MySQL:
    host = "192.168.102.128"
    port = 3306
    username = "starcraft"
    password = "1234asdf"
    database = "starcraft"

    def __init__(self):
        self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.username, passwd=self.password,
                                  db=self.database)
        self.cursor = self.db.cursor()

    def add_player(self, player: Player):
        query = "SELECT battletag FROM players WHERE battletag = \"{}\"".format(player.battletag)
        self.cursor.execute(query)
        num_rows = self.cursor.rowcount
        if num_rows > 0:
            return 0

        query = "INSERT INTO players (battletag, server) VALUES (%s, %s)"
        num_rows = self.cursor.execute(query, (player.battletag, player.region))
        self.db.commit()

        return num_rows

    def add_ladder(self, ladder: Ladder):
        leagues = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]

        query = (
            "INSERT INTO ladders (id, server, league, division, floor, ceiling) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )

        num_rows = self.cursor.execute(query, (ladder.id, ladder.region, leagues[ladder.league_id], ladder.division,
                                       ladder.min_mmr, ladder.max_mmr))

        self.db.commit()

        return num_rows

    def add_race(self, player: Player, team: Team):
        prefix = team.race[:1].lower()

        query = "UPDATE players SET {0}_mmr = %s, {0}_league = %s, {0}_games = %s WHERE battletag = %s".format(prefix)
        num_rows = self.cursor.execute(query, (team.mmr, team.league, team.games_played, player.battletag))
        self.db.commit()

        return num_rows

    def close(self):
        self.db.close()
