from .team import Team


class Player:
    def __init__(self, battletag: str):
        self.battletag = battletag
        self.ladders = []

    def add_race(self, region: str, race: str, league_id: int, division: int, games_played: int, mmr: int):
        leagues = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]

        team = Team(region, race, leagues[league_id], division, games_played, mmr)
        self.ladders.append(team)

    def add_ladder(self, ladder: Team):
        race_already_exists = False
        for team in self.ladders:
            if ladder.race == team.race:
                # if a player has multiple characters on a server, it's possible to have multiple 1v1 ladders for the
                # same race. if so, we want to keep the highest mmr one
                race_already_exists = True
                if ladder.mmr > team.mmr:
                    team.region = ladder.region
                    team.mmr = ladder.mmr
                    team.league = ladder.league
                    team.divison = ladder.divison
                    team.games_played = ladder.games_played
        if not race_already_exists:
            self.ladders.append(ladder)
