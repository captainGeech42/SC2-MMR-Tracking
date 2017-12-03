from datetime import datetime
import os
import requests

debug = True

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
    seasonID = r.json()["id"]
    if debug:
        print("Current Season ID: {}".format(seasonID))

    # get ladder IDs
    # league IDs we care about are 0-4 (bronze-diamond)
    ladders = []
    for leagueID in range(5):
        r = requests.get("https://us.api.battle.net/data/sc2/league/{}/201/0/{}".format(seasonID, leagueID), authParams)
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
        if numFound > 5:
            break
        r = requests.get("https://us.api.battle.net/data/sc2/ladder/{}".format(ladder["id"]), authParams)
        json = r.json()
        for player in json["team"]:
            if numFound > 5:
                break
            bnet = player["member"][0]["character_link"]["battle_tag"]
            if btags.__contains__(bnet):
                mmr = player["rating"]
                # we only want the player's highest mmr
                if len(playerDict) == 0:
                    playerDict.append({"bnet": bnet, "mmr": mmr})
                    numFound += 1
                else:
                    for i in range(len(playerDict)):
                        if playerDict[i]["bnet"] == bnet and playerDict[i]["mmr"] < mmr:
                            playerDict[i]["mmr"] = mmr
                        else:
                            playerDict.append({"bnet": bnet, "mmr": mmr})
                            numFound += 1
                if debug:
                    print("Found player: {} ({} left)".format(bnet, numBtags - numFound))

    # write mmr data to file
    timestamp = datetime.now()
    mmrFile = open("mmr data {}.txt".format(timestamp), "a")
    if debug:
        print("Writing player MMR data to file ({})".format(mmrFile.name))
    for player in playerDict:
        mmrFile.write("{},{}\n".format(player["bnet"], player["mmr"]))
    mmrFile.close()
