import pandas as pd

class Mysql:
    def __init__(self):
        self.tournamentExcelFilePath = 'data/access/tournaments.xlsx'
        self.decksExcelFilePath      = 'data/access/decks.xlsx'
        self.cardsExcelFilePath      = 'data/access/cards.xlsx'
        self.playersExcelFilePath    = 'data/access/players.xlsx'

        self.tournamentTextFilePath  = 'data/text/tournaments.txt'
        self.decksTextFilePath       = 'data/text/decks.txt'
        self.playersTextFilePath     = 'data/text/players.txt'


    # get top8 player deck
    def getTop8PlayerDeck(self):
        df = pd.read_excel(self.decksExcelFilePath)
    
        itemList = []

        for index, row in df.iterrows():
            itemList.append(row.to_list())

        with open(self.decksTextFilePath, 'a', encoding='utf-8') as file:
            for item in itemList:
                value    = "INSERT INTO `deck` (`id`, `name`) VALUES (%s, %s);\r" %(str(item[0]), str(item[1]))
                file.write(value)


    # get Top8 players
    def getTop8Players(self):
        df = pd.read_excel(self.playersExcelFilePath)
    
        itemList = []

        for index, row in df.iterrows():
            itemList.append(row.to_list())

        position = None
        with open(self.playersTextFilePath, 'a', encoding='utf-8') as file:
            for item in itemList:
                # allways first row is 1st player
                previous = self.getPreviousPosition(item[1], position)
                position = self.getPosition(item[1], previous)

                value    = "INSERT INTO `player` (`name`, `position`, `idTournament`, `idDeck`) VALUES (%s, %s, '%s', '%s');\r" %(item[0], str(position), item[2], str(item[3]))
                file.write(value)

    # get previous position number
    def getPreviousPosition(self, item, position):
        if item == 1:
            return item
        else:
            return position

    # conversion position number
    def getPosition(self, position, previousValue):
        if int(position) == 1 or int(position) == 2:
            return int(position)
        
        if int(position) == 3:
            return int(position)-1
       
        if int(position) == 4:
            if int(previousValue) == 2:
                return int(previousValue)+1
            else:
                return int(position)
        
        if int(position) == 5:
            if int(previousValue) == 4:
                return int(position)
            else:
                return int(previousValue)+1
        
        if int(position) == 100: 
            return int(previousValue)+1


    # get tournament insert data
    def getTournamentInserts(self):
        df = pd.read_excel(self.tournamentExcelFilePath)
    
        itemList = []

        for index, row in df.iterrows():
            itemList.append(row.to_list())

        with open(self.tournamentTextFilePath, 'a', encoding='utf-8') as file:
            for item in itemList:
                idLeague = self.getIdLeague(item[1])
                value    = "INSERT INTO `tournament` (`id`, `idTournament`, `name`, `date`, `idLeague`, players) VALUES (%s, %s, '%s', '%s', %s, %s);\r" %(str(item[0]), str(item[0]), item[1], item[2], str(idLeague), str(item[3]))
                file.write(value)


    # get tournament idLeague
    def getIdLeague(self, item):
        if '2019' in item:
            idLeague = 19
        if '2020' in item:
            idLeague = 20
        if '2021' in item:
            idLeague = 21
        if '2022' in item:
            idLeague = 22
        if '2023' in item:
            idLeague = 23
        if '2024' in item:
            idLeague = 24
        if '2025' in item:
            idLeague = 25

        return idLeague