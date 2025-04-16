from classes.filePaths import FilePaths
from classes.db import Db
import json

class JsonToMysql:
    def __init__(self):
        self.filePath   = FilePaths()
        self.db         = Db()

    # insert League data + insert Tournament data
    def insertLeagueAndTournament(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonTournamentPath())
        
        for line in jsonContent:
            if self.isLeagueIdExcluded(line['idLeague']) != True:
                # extra info
                leagueName = self.exceptionLeagueNames(line['idLeague'], line['name'])
                idLeague   = self.exceptionLeagueId(line['idLeague'], leagueName)
                year       = self.getYear(line['name'])

                # league add or update data
                self.insertLeagueQuery(self, idLeague, year, leagueName)
                print("  -- League added or updated: %s" %leagueName)

                # tournament add data
                self.insertTournamentQuery(self, line, idLeague)
                print("    -- Tournament added: %s" %line['name'])

    # insert tournament players
    def insertTournamentPlayers(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonPlayersPath())

        for line in jsonContent:
            # excludes 2024 and 2025 tournaments
            if len(self.existsTournamentOnDB(line['idTournament'])) != 0:
                self.insertTournamentPlayerQuery(line)
                print("    -- Top Player added: %s - %s" %(line['position'],line['name']))

    # insert tournament decks
    def insertTournamentDecks(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonDecksPath())

        for line in jsonContent:
            result = self.getPlayerIdDeckOnDB(line['player'], line['idTournament'])
            # excludes 2024 and 2025 tournaments
            if len(result) != 0:
                self.insertDeckQuery(result, line)
                print("    -- Top Player Deck added: %s" %line['name'])

    # insert deck cards
    def insertCardsDeck(self):
        print("    -- Cards adding . . . .")
        jsonContent = self.getJsonFileContent(self.filePath.getJsonCardsPath())

        for line in jsonContent:
            self.insertCardsQuery(line)
        print("    -- Cards added")

    # tournament insert query
    def insertTournamentQuery(self, line, idLeague):
        query = 'INSERT INTO tournament (id, idTournament, name, date, idLeague, players) VALUES ( "%s", "%s", "%s", "%s", "%s", "%s" );' %(line['idTournament'], line['idTournament'], line['name'], line['date'], idLeague, line['players'])
        self.db.executeInsertQuery(self.db.connection(), query)
    
    # league insert or update query
    def insertLeagueQuery(self, idLeague, year, leagueName):
        query = 'INSERT INTO league (id, name, year, active) VALUES ( "%s", "%s", "%s", 1 ) ' %(idLeague, year, leagueName)
        query += 'ON DUPLICATE KEY UPDATE id="%s", name="%s", year="%s", active=1;' %(idLeague, year, leagueName)
        self.db.executeInsertQuery(self.db.connection(), query)
    
    # tournament top8 - top16 players insert query
    def insertTournamentPlayerQuery(self, line):
        query = 'INSERT INTO `player` ( `name`, `position`, `idTournament`, `idDeck` ) VALUES ( "%s", "%s", "%s", "%s" );' %(line['name'], line['position'], line['idTournament'], line['idDeck'])
        self.db.executeInsertQuery(self.db.connection(), query)
    
    # tournament deck insert query
    def insertDeckQuery(self, result, line):
        query = 'INSERT INTO `deck` (`id`, `name`, `idPlayer`) VALUES ( "%s", "%s", "%s");' %(result[0][0], line['name'], result[0][1])
        self.db.executeInsertQuery(self.db.connection(), query)

    # deck cards insert query
    def insertCardsQuery(self, line):
        query = 'INSERT INTO `cards` (`name`, `num`, `idDeck`, `board`, `cardType`) VALUES ( "%s", "%s", "%s", "%s", "%s" );' %(line['name'], line['num'], line['idDeck'], line['board'], line['cardType'])
        self.db.executeInsertQuery(self.db.connection(), query)

    # get year from tournament name string
    def getYear(self, name):
        nameSplitted = name.split(' ')
        
        return nameSplitted[1]
    
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
        

           