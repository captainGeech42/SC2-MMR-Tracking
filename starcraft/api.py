import requests

from exceptions import RequestError
from log import Log
from .ladder import Ladder
from .player import Player


class API:
    @staticmethod
    def get_current_season_id(params: dict) -> int:
        r = requests.get("https://us.api.battle.net/data/sc2/season/current", params)
        if r.status_code != 200:
            raise RequestError(r, "{} returned error code {}, exiting...".format(r.url, r.status_code))
        return r.json()["id"]

    @staticmethod
    def get_all_ladders(region_code: str, max_league_id: int, season_id: int, params: dict) -> """List of ladders""":
        ladders = []
        for league_id in range(max_league_id + 1):
            try:
                r = requests.get("https://{}.api.battle.net/data/sc2/league/{}/201/0/{}".format(region_code, season_id,
                                                                                                league_id), params)
                if r.status_code != 200:
                    raise RequestError(r, "{} returned error code {}, skipping...".format(r.url, r.status_code))
                Log.write_log_message("League {} Status: {}".format(league_id, r.status_code))
                json = r.json()
                for tier in json["tier"]:
                    division = tier["id"]
                    min_mmr = tier["min_rating"]
                    max_mmr = tier["max_rating"]
                    for ladder in tier["division"]:
                        ladder_id = ladder["ladder_id"]
                        obj = Ladder(region_code, ladder_id, league_id, division, min_mmr, max_mmr)
                        ladders.append(obj)
            except RequestError as e:
                Log.write_log_message(e.__str__(), True)
        return ladders

    @staticmethod
    def get_players_in_ladder(region_code: str, ladder: Ladder, params: dict) -> """List of players""":
        players = []
        r = requests.get("https://{}.api.battle.net/data/sc2/ladder/{}".format(region_code, ladder.id), params)
        if r.status_code != 200:
            raise RequestError(r, "{} returned error code {}, skipping...".format(r.url, r.status_code))
        json = r.json()
        for player in json["team"]:
            try:
                bnet = player["member"][0]["character_link"]["battle_tag"]
                mmr = player["rating"]
                games_played = player["member"][0]["played_race_count"][0]["count"]
                race = player["member"][0]["played_race_count"][0]["race"]

                found_player = False
                for p_obj in players:
                    if p_obj.battletag == bnet:
                        p_obj.add_race(region_code, race, ladder.league_id, ladder.division, games_played, mmr)
                        found_player = True
                if not found_player:
                    obj = Player(bnet)
                    # ladder.division + 1 is due to API having d1 be 0, d2 be 1, etc.
                    obj.add_race(region_code, race, ladder.league_id, ladder.division + 1, games_played, mmr)
                    players.append(obj)
            except KeyError:
                continue
        return players
