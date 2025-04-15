from classes.msAccessToExcel import MSAccessToExcel
from classes.excelToJson import ExcelToJson
from classes.jsonToMysql import JsonToMysql
from classes.filePaths import FilePaths

class Menu:
    def __init__(self):
        self.filePath = FilePaths()

    def accessToExcel(self):
        # data from 2019 to 2025
        data = MSAccessToExcel(self.filePath.getOriginalAccessFile())

        print(' -- Access DB export Starting!!!')
        data.getTournaments()
        data.getDecks()
        data.getCards()
        print(' -- Access DB export Finished!!!\n')

    def excelToJson(self):
        data = ExcelToJson()

        print(' -- Generate Insert Files Start!!!')
        data.getTournamentInserts()
        data.getTop8Players()
        data.getTop8PlayerDeck()
        data.getDeckCards()
        print(' -- Generate Insert Files Finished!!!\n')

    def jsonToMysqlDatabase(self):
        data = JsonToMysql()
        print(' -- Read File Start!!!')
        data.readFile()
        print(' -- Read File Finished!!!')