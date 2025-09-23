from classes.filePaths import FilePaths
from classes.supabase.queries import Queries
import json
import time

class JsonToSupabase:
    def __init__(self):
        self.filePath = FilePaths()
        self.queries  = Queries()

    # insert League data + insert Tournament data
    def insertLeagues(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonTournamentPath())

        leagues = []
        
        for line in jsonContent:
            if self.isLeagueIdExcluded(line['idLeague']) != True:
                # extra info
                leagueName = self.exceptionLeagueNames(line['idLeague'], line['name'])
                idLeague   = self.exceptionLeagueId(line['idLeague'], leagueName)
                year       = self.getYear(leagueName)

                item = {
                    "leagueName" : leagueName,
                    "idLeague"   : idLeague,
                    "year"       : year
                }

                if item not in leagues:
                    leagues.append(item)

        for league in leagues:
            result = self.queries.existsLeague(league['idLeague'])
            if len(result) == 0:
                self.queries.insertLeagueQuery(league['idLeague'], league['year'], league['leagueName'])
                print("    -- League added or updated: %s" %league['leagueName'])
            else:
                print("    -- League is on DB: %s" %league['leagueName'])

    # insert League data + insert Tournament data
    def insertTournaments(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonTournamentPath())
        
        for line in jsonContent:
            if self.isLeagueIdExcluded(line['idLeague']) != True:
                # extra info
                leagueName = self.exceptionLeagueNames(line['idLeague'], line['name'])
                idLeague   = self.exceptionLeagueId(line['idLeague'], leagueName)

                # tournament add data
                res = self.queries.existsTournament(line['id'], line['idTournament'], idLeague)
                if len(res) == 0:
                    self.queries.insertTournamentQuery(line, idLeague)
                    print("      -- Tournament added: %s" %line['name'])
                else:
                    print("      -- Tournament is on DB: %s" %line['name'])

    # insert tournament players
    def insertTournamentPlayers(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonPlayersPath())

        tournamentPlayers  = []
        previousTournament = None
        for line in jsonContent:
            # start loop
            if previousTournament is None:
                previousTournament = line['idTournament']

            if previousTournament != line['idTournament']:
                if len(tournamentPlayers) > 0: 
                    self.queries.insertMultipleTournamentPlayerQuery(tournamentPlayers, previousTournament)

                # reset previousTournament
                previousTournament = line['idTournament']
                tournamentPlayers  = []

            # excludes 2024 and 2025 tournaments
            if len(self.queries.existsTournamentOnDB(line['idTournament'])) != 0:
                tournamentPlayers.append(line)

    # insert tournament decks
    def insertTournamentDecks(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonDecksPath())

        tournamentDecks  = []
        previousTournament = None
        for line in jsonContent:
            # start loop
            if previousTournament is None:
                previousTournament = line['idTournament']

            if previousTournament != line['idTournament']:
                if len(tournamentDecks) > 0:
                    print("\n      !! Top Decks Tournament: %s" %previousTournament)
                    self.queries.insertMultipleDeckQuery(tournamentDecks)

                # reset previousTournament
                previousTournament = line['idTournament']
                tournamentDecks    = []

            item = {
                'id'   : line['id'],
                'name' : line['name'],
            }

            tournamentDecks.append(item)

    # insert deck cards
    def insertCardsDeck(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonCardsPath())

        deckListCards = []
        previousDeck = None
          
        print("\n      !! Adding cards:")

        # bypass to recover broken connection
        # recoverInsert = False
        recoverInsert = True
        # idDeck  8514
        for line in jsonContent:
            # bypass to recover broken connection
            # if int(line['idDeck']) == 8761:
            #     recoverInsert = True

            if int(line['idDeck']) >= 9034:
                break

            if recoverInsert == True:
                # start loop
                if previousDeck is None:
                    previousDeck = line['idDeck']

                # change idDeck
                if previousDeck != line['idDeck']:
                    if len(deckListCards) > 0:
                        self.queries.insertMultipleCardsQuery(deckListCards, previousDeck)
                        time.sleep(2)
                    
                    # reset previousDeck
                    previousDeck = line['idDeck']
                    deckListCards = []

                deckListCards.append(line)
    
    # get year from tournament name string
    def getYear(self, name):
        nameSplitted = name.split(' ')
        
        return nameSplitted[1]

    # read json file
    def getJsonFileContent(self, filePath):        
        with open(filePath, 'r') as openfile:
            jsonObject = json.load(openfile)

        return jsonObject['data']

    # Tournament exception names - change names from old data
    def exceptionLeagueNames(self, idLeague, leagueName):
        if int(idLeague) == 19:
            return 'LCL 2019'
        if int(idLeague) == 20:
            return 'LCL 2020'
        if int(idLeague) == 22:
            return 'LCL 2022'
        if int(idLeague) == 23 and 'LIL' in leagueName:
            return 'LIL 2023'
        if int(idLeague) == 23 and 'LCL' in leagueName:
            return 'LCL 2023'
    
    # exception league id - old data keep alive
    def exceptionLeagueId(self, idLeague, leagueName):
        if leagueName == 'LIL 2023':
            return 230000
        else:
            return int(idLeague)
        
    # exclude new leagues - They are added throught mtgtop8 scrapper
    def isLeagueIdExcluded(self, idLeague):
        if int(idLeague) == 24 or int(idLeague) == 25:
            return True
        else:
            return False
