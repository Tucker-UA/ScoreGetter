#!/usr/bin/env python3

import requests, json, os
import tui
from datetime import datetime, timedelta

### Default values

SPORT = "football"
LEAGUE = "college-football"
TEAMSFILE = "dataTeams.json"
CHOSENTEAMS = "chosenTeams.json"
URLV2 = f"https://site.api.espn.com/apis/site/v2/sports/{SPORT}/{LEAGUE}/"
CDNURL = f"https://cdn.espn.com/core/{SPORT}/"

def clear():
    '''
    Clears text from screen
    '''
    os.system('cls' if os == 'nt' else 'clear')

def saveData(data, dataFile):
    '''
    Saves json data to file
    '''
    with open(dataFile, "w") as file:
        json.dump(data, file)
        print(f"Dumped to file: {dataFile}")

def loadData(dataFile):
    '''
    Returns a JSON decoded result of the given file
    '''

    with open(dataFile, "r") as file:
        data = json.load(file)

    return data

def dataRequest(url, params=None):
    '''
    Returns a json decoded result of the requested data
    '''
    try:
        if params is None:
            response = requests.get(url, timeout=30)
        else:
            response = requests.get(url, timeout=30, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Encounted Exception during request: {e}")
        data = dict()

    return data

def getCurrentTeams(sport=SPORT, league=LEAGUE):
    '''
    Returns a list with the current teams for the given sport and league
    '''
    url = URLV2 + f"teams"
    limit = 200
    currPage = 1
    params = {
            "page" : currPage,
            "limit" : limit,
            "active" : True
    }
   
    teams = []
    numTeams = 0

    try:
        done = False
        while not done:
            result = dataRequest(url, params)
            teams.extend([t["team"] for miniLeague in result["sports"][0]["leagues"] for t in miniLeague["teams"]])# Magic path to get each team according to published schema
            
            newTeams = len(teams)-numTeams
            numTeams = len(teams)

            done = newTeams == 0

            currPage += 1
            params["page"] = currPage
    except Exception as e:
        print(f"Encountered Exception during teams request: {e}")
    saveData(teams, TEAMSFILE) 
    return teams

def getTeams(sport=SPORT, league=LEAGUE):
    '''
    Gets the teams that are active in the league
    Returns a list of dicts containing that information
    '''
    try:
        file = open(TEAMSFILE, "r")
        teams = json.load(file)
    except:
        print("Need to get teams from website")
        teams = getCurrentTeams(sport, league)

    return teams

def pickTeam(teams):
    '''
    Picks a team to follow, prints the id, and returns the team
    '''
    clear()
    chosenTeams = []
    while (search := input("Search term --> ").lower()) != 'q':
        narrowedTeams = {t["displayName"] : t for t in teams if search in t["displayName"].lower()}
        team = tui.browseData(narrowedTeams)
        chosenTeams.append(team)

    saveData(chosenTeams, CHOSENTEAMS)

    return chosenTeams

def getTeamSchedule(team):
    '''
    Gets the team schedule for the season
    '''
    teamID = team["id"]
    url = URLV2 + f"teams/{teamID}/schedule"

    schedule = dataRequest(url)

    return schedule

def getGameSummary(event):
    '''
    Gets the summary for the given event
    '''
    gameID = event["id"]
    url = URLV2 + f"summary?event={gameID}"

    summary = dataRequest(url)

    return summary

def scores(summary):
    '''
    Gets the scores from a given game summary
    '''
    scoringPlays = summary["scoringPlays"]

    awayScore = scoringPlays[-1]["awayScore"]
    homeScore = scoringPlays[-1]["homeScore"]

    return awayScore, homeScore

def main(league, lastWeek = True):
    # Get weekend dates
    today = datetime.today() 
    if lastWeek:
        today = today - timedelta(days=7)

    t = today.weekday() # Integer from 0-6 representing weekday, starting on Monday
    weekendDates = []
    
    weekendDates = [(today + timedelta(days=4+i-t)).strftime("%Y%m%d") for i in range(3)] # Gets the three days of the weekend
    
    print(f"\n🏈 Weekend Games ({league.upper()} League)")
    print(f"📅 Dates: {', '.join(weekendDates)}")
    
    for date in weekendDates:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/{league}/scoreboard?dates={date}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'events' in data:
                events = data['events']
                for event in events:
                    game = event['competitions'][0]
                    score = ' vs. '.join([c["team"]["abbreviation"] + c["score"] for c in game['competitors']])
                    print(f"🏈 {event["name"]} with {score}")
            else:
                print(f"No games for {date}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    teams = loadData(CHOSENTEAMS)
    schedules = []
    for team in teams:
        schedules.append(getTeamSchedule(team))
    
    events = [schedule["events"] for schedule in schedules]

    firstGames = [games[0] for games in events]

    summaries = [getGameSummary(firstGame) for firstGame in firstGames]

    for summary in summaries:
        teamsPlaying = summary["boxscore"]["teams"]

        for team in teamsPlaying:
            if team["homeAway"] == "away":
                awayTeam = team["team"]
            else:
                homeTeam = team["team"]
        
        score = scores(summary)
        print(f"{awayTeam["abbreviation"]} @ {homeTeam["abbreviation"]} : {score[0]} - {score[1]}")

    #teams = getTeams()
    #for team in pickTeam(teams):
    #    print(team["displayName"])
    #main(league)

