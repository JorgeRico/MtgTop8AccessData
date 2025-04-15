class FilePaths:
    def __init__(self):
        self.accessPath = 'data/access/'
        self.textPath   = 'data/text/'

    def getExcelTournamentPath(self):
        return self.accessPath + 'tournaments.xlsx'

    def getExcelDecksPath(self):
        return self.accessPath + 'decks.xlsx'

    def getExcelCardsPath(self):
        return self.accessPath + 'cards.xlsx'

    def getExcelPlayersPath(self):
        return self.accessPath + 'players.xlsx'

    def getTextTournamentPath(self):
        return self.textPath + 'tournaments.txt'

    def getTextDecksPath(self):
        return self.textPath + 'decks.txt'

    def getTextCardsPath(self):
        return self.textPath + 'cards.txt'

    def getTextPlayersPath(self):
        return self.textPath + 'players.txt'
