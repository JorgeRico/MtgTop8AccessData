class FilePaths:
    def __init__(self):
        self.excelPath  = 'data/excel/'
        self.jsonPath   = 'data/json/'
        self.originPath = 'data/origin/'

    # origin - data from year 2019 to 2025
    def getOriginalAccessFile(self):
        return self.originPath + 'data.mdb'

    # excel files
    def getExcelTournamentPath(self):
        return self.excelPath + 'tournaments.xlsx'

    def getExcelDecksPath(self):
        return self.excelPath + 'decks.xlsx'

    def getExcelCardsPath(self):
        return self.excelPath + 'cards.xlsx'

    def getExcelPlayersPath(self):
        return self.excelPath + 'players.xlsx'
    
    # json files
    def getJsonTournamentPath(self):
        return self.jsonPath + 'tournaments.json'
    
    def getJsonDecksPath(self):
        return self.jsonPath + 'decks.json'

    def getJsonCardsPath(self):
        return self.jsonPath + 'cards.json'

    def getJsonPlayersPath(self):
        return self.jsonPath + 'players.json'
