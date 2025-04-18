from classes.msAccessToExcel import MSAccessToExcel
from classes.excelToJson import ExcelToJson
from classes.jsonToMysql import JsonToMysql
from classes.filePaths import FilePaths

class Menu:
    def __init__(self):
        self.filePath = FilePaths()

    # 1st step - Get mdb file data and transform to excel
    def accessToExcel(self):
        data = MSAccessToExcel(self.filePath.getOriginalAccessFile())

        print(' -- Access DB export Starting!!!')
        data.getTournaments()
        data.getDecks()
        data.getCards()
        print(' -- Access DB export Finished!!!\n')

    # 2nd step - Transform info from excel to json
    def excelToJson(self):
        data = ExcelToJson()

        print(' -- Generate Insert Files Start!!!')
        data.getTournamentInserts()
        data.getTop8Players()
        data.getTop8PlayerDeck()
        data.getDeckCards()
        print(' -- Generate Insert Files Finished!!!\n')

    # 3rd step - Add json info to database
    def jsonToMysqlDatabase(self):
        data = JsonToMysql()
        print(' -- Insert values on DB Start!!!')
        data.insertLeagueAndTournament()
        data.insertTournamentPlayers()
        data.insertTournamentDecks()
        data.insertCardsDeck()
        print(' -- Insert values on DB Finished!!!')