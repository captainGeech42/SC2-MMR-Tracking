import MySQLdb
import os
import time
import sys

from exceptions import RequestError
from log import Log
from database import MySQL
from starcraft import API


# program constants
WRITE_DEBUG_LOG = True
MAX_LEAGUE_ID = 4
BATTLETAG_FILE_PATH_FORMAT = "battletags_{}"
ACCESS_TOKEN_PATH = "access_token"
REGION_CODES = ["us", "eu"]


def verify_files_exists(regions: list)->bool:
    for region in regions:
        if not os.path.exists(BATTLETAG_FILE_PATH_FORMAT.format(region)):
            Log.write_log_message("Battletag file for {} does not exist, exiting...".format(region.upper()), True)
            raise FileNotFoundError()

    if not os.path.exists(ACCESS_TOKEN_PATH):
        Log.write_log_message("Access token file does not exist, exiting...", True)
        raise FileNotFoundError()

    return True


def get_request_parameters()->dict:
    access_token_handle = open(ACCESS_TOKEN_PATH, "r")
    access_token = access_token_handle.readline().strip()
    access_token_handle.close()

    return {"access_token": access_token, "locale": "en_US"}


def get_battletags(region: str)->list:
    file = open(BATTLETAG_FILE_PATH_FORMAT.format(region), "r")
    return [btag.strip() for btag in file.readlines()]


def write_all_mmr_data(players: list):
    file_timestamp = time.strftime("%Y-%m-%d %H%M%S")
    mmr_file = open("mmr data {}.txt".format(file_timestamp), "w")
    if WRITE_DEBUG_LOG:
        print("Writing all player MMR data to file ({})".format(mmr_file.name))
    for player in players:
        for team in player.ladders:
            mmr_file.write("{},{},{},{},{},{}\n".format(player.battletag, player.region, team.race, team.mmr, team.league,
                                                        team.games_played))
    mmr_file.close()


def add_players_to_database(db: MySQL, players: list):
    for player in players:
        db.add_player(player)


def add_ladders_to_database(db: MySQL, ladders: list):
    for ladder in ladders:
        db.add_ladder(ladder)


def write_valid_players(players: list):
    file_timestamp = time.strftime("%Y-%m-%d %H%M%S")
    file = open("valid players {}.txt".format(file_timestamp), "w")
    for player in players:
        battletag = player["battletag"]
        mmr = player["mmr"]
        valid_races = player["valid_races"]
        valid_races_str = ""
        for valid_race in valid_races:
            valid_races_str += valid_race[:1]
        file.write("{} ({}),{}\n".format(battletag, valid_races_str, mmr))
    file.close()


def main():
    # verify that the necessary files exist
    battletag_from_cli = []
    if len(sys.argv) == 1:
        try:
            verify_files_exists(REGION_CODES)
        except FileNotFoundError:
            exit(1)
    elif len(sys.argv) == 2:
        if not os.path.exists(sys.argv[1]):
            Log.write_log_message("Specified file does not exist, exiting...", True)
        btags = open(sys.argv[1], "r")
        for btag in btags:
            battletag_from_cli.append(btag.strip())

    # get the API request parameters
    request_parameters = get_request_parameters()

    # get the current season ID
    season_id = -1
    try:
        season_id = API.get_current_season_id(request_parameters)
    except RequestError as e:
        print(e)
        exit(1)
    Log.write_log_message("Current Season ID: {}".format(season_id))

    db_handle = MySQL()

    for region in REGION_CODES:
        Log.write_log_message("Starting {} Region".format(region.upper()))

        # get ladders
        ladders = API.get_all_ladders(region, MAX_LEAGUE_ID, season_id, request_parameters)
        Log.write_log_message("Total Ladders Found: {}".format(len(ladders)))

        # add all of the ladders to the database
        try:
            add_ladders_to_database(db_handle, ladders)
        except MySQLdb.IntegrityError:
            Log.write_log_message("Ladders are already in database for {}".format(region.upper()))

        # read in btags to a list
        if len(battletag_from_cli) == 0:
            battletags = get_battletags(region)
        else:
            battletags = battletag_from_cli
        num_battletags = len(battletags)
        Log.write_log_message("Battletags Read In: {}".format(num_battletags))

        # go through every ladder looking for one of our players
        for ladder in ladders:
            # loop through every ladder between bronze and diamond

            # get all of the players in the ladder
            players = API.get_players_in_ladder(region, ladder, request_parameters)

            for player in players:
                # loop through every player in the ladder

                if [battletag.lower() for battletag in battletags].__contains__(player.battletag.lower()):
                    # a JSL contestant was found
                    db_handle.add_player(player)

                    for team in player.ladders:
                        db_handle.add_race(player, team)

                    for team in player.ladders:
                        Log.write_log_message(
                            "Found player: {} [{} {} {}]".format(player.battletag, team.league,
                                                                 team.divison, team.race))

    # get all players in database
    Log.write_log_message("Writing valid player data to disk")
    valid_players = db_handle.get_all_valid_players()
    write_valid_players(valid_players)

    # close database
    db_handle.close()


if __name__ == "__main__":
    main()
    # db = MySQL()
    # write_valid_players(db.get_all_valid_players())
