import os
import requests
import time

debug = True

MAX_LEAGUE_ID = 4

if __name__ == "__main__":
    # verify that the necessary files exist
    btagPath = "battletags"
    if not os.path.exists(btagPath):
        print("Battletag file does not exist, exiting...")
        exit(1)

    accessTokenPath = "access_token"
    if not os.path.exists(accessTokenPath):
        print("Access token file does not exist, exiting...")
        exit(1)

    # get the API access token
    accessTokenHandle = open(accessTokenPath, "r")
    accessToken = accessTokenHandle.readline().strip()
    accessTokenHandle.close()

    authParams = {"access_token": accessToken}

    # get the current season ID
    r = requests.get("https://us.api.battle.net/data/sc2/season/current", authParams)
    if r.status_code != 200:
        print("{} returned error code {}, exiting...".format(r.url, r.status_code))
        exit(1)
    seasonID = r.json()["id"]
    if debug:
        print("Current Season ID: {}".format(seasonID))

    # get ladder IDs
    # league IDs we care about are 0-4 (bronze-diamond)
    ladders = []
    for leagueID in range(MAX_LEAGUE_ID + 1):
        r = requests.get("https://us.api.battle.net/data/sc2/league/{}/201/0/{}".format(seasonID, leagueID), authParams)
        if r.status_code != 200:
            print("{} returned error code {}, skipping...".format(r.url, r.status_code))
            continue
        if debug:
            print("League {} Status: {}".format(leagueID, r.status_code))
        json = r.json()
        for tier in json["tier"]:
            division = tier["id"]
            minMMR = tier["min_rating"]
            maxMMR = tier["max_rating"]
            if debug:
                print("Division: {}".format(division))
                print("Minimum MMR: {}".format(minMMR))
                print("Maximum MMR: {}".format(maxMMR))
            for ladder in tier["division"]:
                ladderID = ladder["ladder_id"]
                if debug:
                    print("Ladder ID: {}".format(ladderID))
                data = {"league": leagueID, "division": division, "min_mmr": minMMR, "ceiling_mmr": maxMMR,
                        "id": ladderID}
                ladders.append(data)
                if debug:
                    print(data)
    print("Total Ladders Found: {}".format(len(ladders)))

    # read in btags to a list
    btagFile = open(btagPath, "r")
    btags = [btag.strip() for btag in btagFile.readlines()]
    numBtags = len(btags)
    if debug:
        print("Battletags Read In: {} [Sample: {}]".format(numBtags, btags[0]))

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
            if [btag.lower() for btag in btags].__contains__(bnet.lower()):
                mmr = player["rating"]
                gamesPlayed = player["member"][0]["played_race_count"][0]["count"]
                race = player["member"][0]["played_race_count"][0]["race"]["en_US"]

                btagAlreadyFound = any(p["bnet"] == bnet for p in playerDict)

                playerDict.append({"bnet": bnet, "league": ladder["league"], "mmr": mmr, "games": gamesPlayed,
                                   "race": race})
                if not btagAlreadyFound:
                    numFound += 1

                if debug:
                    print("Found player: [{}] {} ({} left)".format(race, bnet, numBtags - numFound))

    # write mmr data to file
    timestamp = time.strftime("%Y-%m-%d %H%M%S")
    mmrFile = open("mmr data {}.txt".format(timestamp), "w")
    if debug:
        print("Writing player MMR data to file ({})".format(mmrFile.name))
    for player in playerDict:
        mmrFile.write("{},{},{},{},{}\n".format(player["bnet"], player["race"], player["mmr"], player["league"],
                                                player["games"]))
    mmrFile.close()
