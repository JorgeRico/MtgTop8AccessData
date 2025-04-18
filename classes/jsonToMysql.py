from classes.filePaths import FilePaths
from classes.db import Db
import json
import time
class JsonToMysql:
    def __init__(self):
        self.filePath = FilePaths()
        self.db       = Db()

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
                self.insertLeagueQuery(idLeague, year, leagueName)
                # print("    -- League added or updated: %s" %leagueName)

                # tournament add data
                self.insertTournamentQuery(line, idLeague)
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
                    players = self.saveTournamentPlayersList(tournamentPlayers)
                    self.insertMultipleTournamentPlayerQuery(players)
                    print("    -- Top Players Added Tournament: %s" %previousTournament)

                # reset previousTournament
                previousTournament = line['idTournament']
                tournamentPlayers  = []

            # excludes 2024 and 2025 tournaments
            if len(self.existsTournamentOnDB(line['idTournament'])) != 0:
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
                    decks = self.saveDecksList(tournamentDecks)
                    self.insertMultipleDeckQuery(decks)
                    print("    -- Top Player Decks Added Tournament: %s" %previousTournament)

                # reset previousTournament
                previousTournament = line['idTournament']
                tournamentDecks  = []

            result = self.getPlayerIdDeckOnDB(line['player'], line['idTournament'])
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
                        cards = self.saveDeckCardsList(deckListCards)
                        self.insertMultipleCardsQuery(cards)
                        print("    -- Cards added - idDeck: %s" %previousDeck)
                        time.sleep(2)
                    
                    # reset previousDeck
                    previousDeck = line['idDeck']
                    deckListCards = []

                result = self.existsIdDeck(line['idDeck'])
                if len(result) > 0:
                    deckListCards.append(line)
    
    # tournament insert query
    def insertTournamentQuery(self, line, idLeague):
        query = 'INSERT INTO tournament (id, idTournament, name, date, idLeague, players) VALUES ( "%s", "%s", "%s", "%s", "%s", "%s" );' %(line['idTournament'], line['idTournament'], line['name'], line['date'], idLeague, line['players'])
        self.db.executeInsertQuery(self.db.connection(), query)
    
    # league insert or update query
    def insertLeagueQuery(self, idLeague, year, leagueName):
        query = 'INSERT INTO league (id, name, year, active) VALUES ( "%s", "%s", "%s", 1 ) ' %(idLeague, leagueName, year)
        query += 'ON DUPLICATE KEY UPDATE id="%s", name="%s", year="%s", active=1;' %(idLeague, leagueName, year)
        self.db.executeInsertQuery(self.db.connection(), query)

    # tournament top8 - top16 multiple players insert query
    def insertMultipleTournamentPlayerQuery(self, line):
        query = 'INSERT INTO `player` ( `name`, `position`, `idTournament`, `idDeck` ) VALUES %s' %line
        self.db.executeInsertQuery(self.db.connection(), query)

    # top8 players query values
    def saveTournamentPlayersList(self, tournamentPlayers):
        query = ''
        for player in tournamentPlayers:
            query += ' ( "%s", "%s", "%s", "%s" ),' %(player['name'], player['position'], player['idTournament'], player['idDeck'])

        return self.replaceLastQueryChar(query)

    # tournament multiple deck insert query
    def insertMultipleDeckQuery(self, line):
        query = 'INSERT INTO `deck` (`id`, `name`, `idPlayer`) VALUES %s' %line
        self.db.executeInsertQuery(self.db.connection(), query)

    # tournament deck values query
    def saveDecksList(self, decks):
        query = ''
        for deck in decks:
            query += ' ( "%s", "%s", "%s" ),' %(deck['id'], deck['name'], deck['idPlayer'])

        return self.replaceLastQueryChar(query)

    # deck cards insert query
    def insertMultipleCardsQuery(self, line):
        query = 'INSERT INTO `cards` (`name`, `num`, `idDeck`, `board`, `cardType`) VALUES %s' %line
        self.db.executeInsertQuery(self.db.connection(), query)

    # multiple card query values
    def saveDeckCardsList(self, deckListCards):
        query = ''
        for card in deckListCards:
            query += ' ( "%s", "%s", "%s", "%s", "%s" ),' %(card['name'], card['num'], card['idDeck'], card['board'], card['cardType'])

        return self.replaceLastQueryChar(query)

    # get year from tournament name string
    def getYear(self, name):
        nameSplitted = name.split(' ')
        
        return nameSplitted[1]
    
    # get list of excluded decks
    def existsIdDeck(self, idDeck):
        query = 'SELECT id FROM player WHERE idDeck = %s' %idDeck 

        return self.db.selectQuery(self.db.connection(), query)

    # check if Tournament exists
    def existsTournamentOnDB(self, idTournament):
        query = 'SELECT id as id FROM tournament WHERE idTournament = %s;' %(idTournament)
        
        return self.db.selectQuery(self.db.connection(), query)
    
    # get player id - keep alive old ids
    def getPlayerIdDeckOnDB(self, name, idTournament):
        query = 'SELECT idDeck as idDeck, id as idPlayer FROM player WHERE name = "%s" AND idTournament = %s;' %(name, idTournament)
        
        return self.db.selectQuery(self.db.connection(), query)

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
        
    # change last "," by ";"
    def replaceLastQueryChar(self, query):
        query = query[:-1] + ';'

        return query
           