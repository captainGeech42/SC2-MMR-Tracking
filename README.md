# StarCraft II MMR Tracker

This Python program uses the SC2 API to pull MMR data from a list of players

### Dependencies

 * Python3
 * requests

### Usage

 1. Put a list of Battletags in `battletags` (one per line)
 2. Put your API access token in `access_token`
    * To get this token, go [here](https://dev.battle.net/io-docs) and register an application to get a client ID/secret. Then, use that data on `Game Data APIs - US` in the `Authorization Code / Web Server` form to generate the Authorization Code
 3. Run the Python program
 4. MMR and player data will be placed in `mmr data [timestamp].txt`

### Data format in `mmr data [timestamp].txt`

Data is CSV. Example: `asphyxa#1933,Zerg,3784,Diamond,24`
 * `asphyxa#1933` = Battletag
 * `Zerg` = Race for this entry
 * `3784` = MMR as this race
 * `Diamond` = League
 * `24` = Games played as this race

Notes:
 * Data from Masters and Grandmaster leagues are unapplicable to the intended use of this application, so if you are wanting to pull in data from higher leagues, change the value of `MAX_LEAGUE_ID` at the beginning of the program (it's already declard there).
 * Timestamp format: `YYYY-MM-DD HHMMSS`