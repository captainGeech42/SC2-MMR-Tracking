import os
import time

import requests

from exceptions import RequestError
from log import Log


# program constants
WRITE_DEBUG_LOG = True
MAX_LEAGUE_ID = 4
BATTLETAG_FILE_PATH = "battletags"
ACCESS_TOKEN_PATH = "access_token"

# instantiate the log
log = Log()


def verify_files_exists()->bool:
    if not os.path.exists(BATTLETAG_FILE_PATH):
        log.write_log_message("Battletag file does not exist, exiting...", True)
        raise FileNotFoundError()

    if not os.path.exists(ACCESS_TOKEN_PATH):
        log.write_log_message("Access token file does not exist, exiting...", True)
        raise FileNotFoundError()

    return True


def get_auth_param()->dict:
    access_token_handle = open(ACCESS_TOKEN_PATH, "r")
    access_token = access_token_handle.readline().strip()
    access_token_handle.close()

    return {"access_token": access_token}


def get_current_season_id(params: dict)->int:
    r = requests.get("https://us.api.battle.net/data/sc2/season/current", params)
    if r.status_code != 200:
        raise RequestError(r, "{} returned error code {}, exiting...".format(r.url, r.status_code))
    return r.json()["id"]


def get_ladder_ids(params: dict)->list:
    ladders = []
    for leagueID in range(MAX_LEAGUE_ID + 1):
        r = requests.get("https://us.api.battle.net/data/sc2/league/{}/201/0/{}".format(seasonID, leagueID), params)
        if r.status_code != 200:
            print("{} returned error code {}, skipping...".format(r.url, r.status_code))
            continue
        if WRITE_DEBUG_LOG:
            print("League {} Status: {}".format(leagueID, r.status_code))
        json = r.json()
        for tier in json["tier"]:
            division = tier["id"]
            min_mmr = tier["min_rating"]
            max_mmr = tier["max_rating"]
            if WRITE_DEBUG_LOG:
                print("Division: {}".format(division))
                print("Minimum MMR: {}".format(min_mmr))
                print("Maximum MMR: {}".format(max_mmr))
            for ladder in tier["division"]:
                ladder_id = ladder["ladder_id"]
                if WRITE_DEBUG_LOG:
                    print("Ladder ID: {}".format(ladder_id))
                data = {"league": leagueID, "division": division, "min_mmr": min_mmr, "ceiling_mmr": max_mmr,
                        "id": ladder_id}
                ladders.append(data)
                if WRITE_DEBUG_LOG:
                    print(data)
    return ladders


def get_battletags()->list:
    file = open(BATTLETAG_FILE_PATH, "r")
    return [btag.strip() for btag in file.readlines()]


if __name__ == "__main__":
    # verify that the necessary files exist
    try:
        verify_files_exists()
    except FileNotFoundError:
        exit(1)

    # get the API access token
    authParams = get_auth_param()

    # get the current season ID
    seasonID = -1
    try:
        seasonID = get_current_season_id(authParams)
    except RequestError as e:
        print(e)
        exit(1)

    if WRITE_DEBUG_LOG:
        print("Current Season ID: {}".format(seasonID))

    # get ladder IDs
    # league IDs we care about are 0-4 (bronze-diamond)
    ladders = get_ladder_ids(authParams)
    print("Total Ladders Found: {}".format(len(ladders)))

    # read in btags to a list
    battletags = get_battletags()
    numBtags = len(battletags)
    if WRITE_DEBUG_LOG:
        print("Battletags Read In: {} [Sample: {}]".format(numBtags, battletags[0]))

    # go through every ladder looking for one of our players
    playerDict = []
    numFound = 0
    for ladder in ladders:
        r = requests.get("https://us.api.battle.net/data/sc2/ladder/{}".format(ladder["id"]), authParams)
        if r.status_code != 200:
            print("{} returned error code {}, skipping...".format(r.url, r.status_code))
            continue
        json = r.json()
        for player in json["team"]:
            bnet = player["member"][0]["character_link"]["battle_tag"]
            if [btag.lower() for btag in battletags].__contains__(bnet.lower()):
                mmr = player["rating"]
                gamesPlayed = player["member"][0]["played_race_count"][0]["count"]
                race = player["member"][0]["played_race_count"][0]["race"]["en_US"]

                btagAlreadyFound = any(p["bnet"] == bnet for p in playerDict)

                playerDict.append({"bnet": bnet, "league": ladder["league"], "mmr": mmr, "games": gamesPlayed,
                                   "race": race})
                if not btagAlreadyFound:
                    numFound += 1

                if WRITE_DEBUG_LOG:
                    print("Found player: [{}] {} ({} left)".format(race, bnet, numBtags - numFound))

    # write mmr data to file
    file_timestamp = time.strftime("%Y-%m-%d %H%M%S")
    mmrFile = open("mmr data {}.txt".format(file_timestamp), "w")
    if WRITE_DEBUG_LOG:
        print("Writing player MMR data to file ({})".format(mmrFile.name))
    for player in playerDict:
        mmrFile.write("{},{},{},{},{}\n".format(player["bnet"], player["race"], player["mmr"], player["league"],
                                                player["games"]))
    mmrFile.close()
