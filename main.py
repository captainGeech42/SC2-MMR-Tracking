import os
import time

import requests

from exceptions import RequestError
from log import Log
from starcraft import API, Player


# program constants
WRITE_DEBUG_LOG = True
MAX_LEAGUE_ID = 4
BATTLETAG_FILE_PATH = "battletags"
ACCESS_TOKEN_PATH = "access_token"


def verify_files_exists()->bool:
    if not os.path.exists(BATTLETAG_FILE_PATH):
        Log.write_log_message("Battletag file does not exist, exiting...", True)
        raise FileNotFoundError()

    if not os.path.exists(ACCESS_TOKEN_PATH):
        Log.write_log_message("Access token file does not exist, exiting...", True)
        raise FileNotFoundError()

    return True


def get_auth_param()->dict:
    access_token_handle = open(ACCESS_TOKEN_PATH, "r")
    access_token = access_token_handle.readline().strip()
    access_token_handle.close()

    return {"access_token": access_token}


def get_battletags()->list:
    file = open(BATTLETAG_FILE_PATH, "r")
    return [btag.strip() for btag in file.readlines()]


def write_data_to_file(players: list):
    file_timestamp = time.strftime("%Y-%m-%d %H%M%S")
    mmr_file = open("mmr data {}.txt".format(file_timestamp), "w")
    if WRITE_DEBUG_LOG:
        print("Writing player MMR data to file ({})".format(mmr_file.name))
    for player in players:
        for team in player.ladders:
            mmr_file.write("{},{},{},{},{}\n".format(player.battletag, team.race, team.mmr, team.league, team.mmr))
    mmr_file.close()


def main():
    # verify that the necessary files exist
    try:
        verify_files_exists()
    except FileNotFoundError:
        exit(1)

    # get the API access token
    auth_params = get_auth_param()

    # get the current season ID
    season_id = -1
    try:
        season_id = API.get_current_season_id(auth_params)
    except RequestError as e:
        print(e)
        exit(1)
    Log.write_log_message("Current Season ID: {}".format(season_id))

    # get ladders
    ladders = API.get_all_ladders(MAX_LEAGUE_ID, season_id, auth_params)
    Log.write_log_message("Total Ladders Found: {}".format(len(ladders)))

    # read in btags to a list
    battletags = get_battletags()
    num_battletags = len(battletags)
    Log.write_log_message("Battletags Read In: {}".format(num_battletags))

    # go through every ladder looking for one of our players
    jsl_players = []
    num_found = 0
    for ladder in ladders:
        # loop through every ladder between bronze and diamond

        players = API.get_players_in_ladder(ladder, auth_params)

        for player in players:
            # loop through every player in the ladder

            if [battletag.lower() for battletag in battletags].__contains__(player.battletag):
                # a JSL contestant was found

                # look to see if this player already is in the jsl_players list
                found_player = False
                for contestant in jsl_players:
                    if contestant.battletag == player.battletag:
                        # the JSL contestant was found in the list, add the new teams

                        found_player = True
                        for team in player.ladders:
                            # add every team in this ladder for this player
                            contestant.add_ladder(team)
                if not found_player:
                    # the JSL contestant was not found
                    jsl_players.append(player)
                    num_found += 1

                for team in player.ladders:
                    Log.write_log_message("Found player: {} [{} {} {}] ({} left)".format(player.battletag, team.league,
                                                                                         team.divison, team.race,
                                                                                         num_battletags - num_found))

    # write mmr data to file
    write_data_to_file(jsl_players)


if __name__ == "__main__":
    main()
