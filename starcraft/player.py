from .team import Team


class Player:
    def __init__(self, battletag: str):
        self.battletag = battletag
        self.ladders = []

    def add_race(self, race: str, league_id: int, division: int, games_played: int, mmr: int):
        leagues = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]

        team = Team(race, leagues[league_id], division, games_played, mmr)
        self.ladders.append(team)

    def add_ladder(self, ladder: Team):
        self.ladders.append(ladder)
