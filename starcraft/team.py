class Team:
    def __init__(self, region: str, race: str, league: str, division: int, games_played: int, mmr: int):
        self.region = region
        self.race = race
        self.league = league
        self.divison = division
        self.games_played = games_played
        self.mmr = mmr
