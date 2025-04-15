from classes.access import MSAccess
from classes.mysql import Mysql
from classes.filePaths import FilePaths

class Menu:
    def __init__(self):
        self.filePath = FilePaths()

    def accessToExcel(self):
        # data from 2019 to 2025
        data = MSAccess(self.filePath.getOriginalAccessFile())

        print(' -- Access DB export Starting!!!')
        data.getTournaments()
        data.getDecks()
        data.getCards()
        print(' -- Access DB export Finished!!!')

    def excelToInsertText(self):
        data = Mysql()

        print(' -- Generate Insert Files Start!!!')
        data.getTournamentInserts()
        data.getTop8Players()
        data.getTop8PlayerDeck()
        data.getDeckCards()
        print(' -- Generate Insert Files Finished!!!')