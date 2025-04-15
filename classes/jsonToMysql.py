from classes.filePaths import FilePaths
from classes.db import Db
import json

class JsonToMysql:
    def __init__(self):
        self.filePath = FilePaths()

    def insertLeagueAndTournament(self):
        jsonContent = self.getJsonFileContent(self.filePath.getJsonTournamentPath())
        db          = Db()
        connection  = db.connection()

        for line in jsonContent:
            if self.isLeagueIdExcluded(line['idLeague']) != True:
                leagueName = self.exceptionLeagueNames(line['idLeague'], line['name'])
                idLeague   = self.exceptionLeagueId(line['idLeague'], leagueName)
                query      = 'INSERT INTO league (id, name, active) VALUES ( "%s", "%s", 1 ) ' %(idLeague, leagueName)
                query      += 'ON DUPLICATE KEY UPDATE id="%s", name="%s", active=1;' %(idLeague, leagueName)
                db.executeInsertQuery(connection, query)
                print("  -- League added or updated: %s" %leagueName)

                query = 'INSERT INTO tournament (idTournament, name, date, idLeague, players) VALUES ( "%s", "%s", "%s", "%s", "%s" );' %(line['idTournament'], line['name'], line['date'], idLeague, line['players'])
                db.executeInsertQuery(connection, query)
                print("    -- Tournament added: %s" %line['name'])

    def getJsonFileContent(self, filePath):        
        with open(filePath, 'r') as openfile:
            jsonObject = json.load(openfile)

        return jsonObject['data']

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
    
    def exceptionLeagueId(self, idLeague, leagueName):
        if leagueName == 'LIL 2023':
            return 230000
        else:
            return int(idLeague)
        
    def isLeagueIdExcluded(self, idLeague):
        if int(idLeague) == 24 or int(idLeague) == 25:
            return True
        else:
            return False
        

           