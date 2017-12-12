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
        query = "SELECT battletag FROM players WHERE battletag = \"{}\" AND server = \"{}\"".format(player.battletag,
                                                                                                    player.region)
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
        prefix = team.race[:1].lower()  # "Protoss" => "p"

        query = "UPDATE players SET {0}_mmr = %s, {0}_league = %s, {0}_games = %s WHERE battletag = %s AND server = %s"\
            .format(prefix)
        num_rows = self.cursor.execute(query, (team.mmr, team.league, team.games_played, player.battletag,
                                               player.region))
        self.db.commit()

        return num_rows

    def get_all_valid_players(self) -> list:
        query = (
            "SELECT * FROM `players` where (p_league != 'Diamond' and r_league != 'Diamond' and t_league != 'Diamond' "
            "and z_league != 'Diamond') and (p_games >=  25 or r_games >= 25 or t_games >= 25 or z_games >= 25)"
        )

        num_rows = self.cursor.execute(query)

        players = []
        for x in range(num_rows):
            row = self.cursor.fetchone()
            btag = row[1]

            valid_races = []
            if type(row[5]) == int and row[5] >= 25:
                valid_races.append("Protoss")
            if type(row[8]) == int and row[8] >= 25:
                valid_races.append("Random")
            if type(row[11]) == int and row[11] >= 25:
                valid_races.append("Terran")
            if type(row[14]) == int and row[14] >= 25:
                valid_races.append("Zerg")

            mmrs = [row[4], row[7], row[10], row[13]]
            mmr = 0
            for i in mmrs:
                if i is None:
                    continue
                if i > mmr:
                    mmr = i

            players.append({"battletag": btag, "mmr": mmr, "valid_races": valid_races})

        return players

    def close(self):
        self.db.close()
