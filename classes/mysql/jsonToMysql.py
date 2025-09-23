from classes.filePaths import FilePaths
import json
import time
from classes.mysql.queries import Queries

class JsonToMysql:

    def __init__(self):
        self.filePath = FilePaths()
        self.queries  = Queries()

    # insert League data + insert Tournament data
    def insertLeagueAndTournament(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonTournamentPath())
        
        for line in jsonContent:
            if self.isLeagueIdExcluded(line['idLeague']) != True:
                # extra info
                leagueName = self.exceptionLeagueNames(line['idLeague'], line['name'])
                idLeague   = self.exceptionLeagueId(line['idLeague'], leagueName)
                year       = self.getYear(leagueName)

                # league add or update data
                self.queries.insertLeagueQuery(idLeague, year, leagueName)
                # print("    -- League added or updated: %s" %leagueName)

                # tournament add data
                self.queries.insertTournamentQuery(line, idLeague)
                print("    -- Tournament added: %s" %line['name'])

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
                    players = self.queries.saveTournamentPlayersList(tournamentPlayers)
                    self.queries.insertMultipleTournamentPlayerQuery(players)
                    print("    -- Top Players Added Tournament: %s" %previousTournament)

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
                    decks = self.queries.saveDecksList(tournamentDecks)
                    self.queries.insertMultipleDeckQuery(decks)
                    print("    -- Top Player Decks Added Tournament: %s" %previousTournament)

                # reset previousTournament
                previousTournament = line['idTournament']
                tournamentDecks  = []

            result = self.queries.getPlayerIdDeckOnDB(line['player'], line['idTournament'])
            # excludes 2024 and 2025 tournaments
            if len(result) != 0:
                item = {
                    'id'       : result[0][0],
                    'name'     : line['name'],
                    'idPlayer' : result[0][1]
                }
                tournamentDecks.append(item)

    # insert deck cards
    def insertCardsDeck(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonCardsPath())

        deckListCards = []
        previousDeck = None

        # bypass to recover broken connection
        # recoverInsert = False
        recoverInsert = True
        # idDeck  8514
        for line in jsonContent:
            # bypass to recover broken connection
            # if int(line['idDeck']) == 8514:
            #     recoverInsert = True

            if recoverInsert == True:
                # start loop
                if previousDeck is None:
                    previousDeck = line['idDeck']

                # change idDeck
                if previousDeck != line['idDeck']:
                    if len(deckListCards) > 0:
                        cards = self.queries.saveDeckCardsList(deckListCards)
                        self.queries.insertMultipleCardsQuery(cards)
                        print("    -- Cards added - idDeck: %s" %previousDeck)
                        time.sleep(2)
                    
                    # reset previousDeck
                    previousDeck = line['idDeck']
                    deckListCards = []

                result = self.queries.existsIdDeck(line['idDeck'])
                if len(result) > 0:
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
