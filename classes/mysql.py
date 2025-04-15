import pandas as pd
from classes.scrapping import Scrapping
from classes.filePaths import FilePaths
class Mysql:
    def __init__(self):
        self.filePath = FilePaths()

    # get deck cards
    def getDeckCards(self):
        df       = pd.read_excel(self.filePath.getExcelCardsPath())
        itemList = self.getItemListFromExcel(df)

        for item in itemList:
            cardType = self.getCardType(item[0])

            # main cards
            if int(item[2]) > 0:
                value = "INSERT INTO cards (name, num, idDeck, board, cardType) VALUES ( %s, %s, %s, %s, %s );\r" %(str(item[0]), item[2], item[1], 'md', cardType)
                self.writeFile(value, self.filePath.getTextCardsPath())

            # sideboard cards
            if int(item[3]) > 0:
                value = "INSERT INTO cards (name, num, idDeck, board, cardType) VALUES ( %s, %s, %s, %s, %s );\r" %(str(item[0]), item[3], item[1], 'sb', cardType)
                self.writeFile(value, self.filePath.getTextCardsPath())  

    # get top8 player deck
    def getTop8PlayerDeck(self):
        df       = pd.read_excel(self.filePath.getExcelDecksPath())
        itemList = self.getItemListFromExcel(df)

        for item in itemList:
            value = "INSERT INTO `deck` (`id`, `name`) VALUES (%s, %s);\r" %(str(item[0]), str(item[1]))
            self.writeFile(value, self.filePath.getTextDecksPath())

    # get top8 player deck
    def getTop8PlayerDeck(self):
        df       = pd.read_excel(self.filePath.getExcelDecksPath())
        itemList = self.getItemListFromExcel(df)

        for item in itemList:
            value = "INSERT INTO `deck` (`id`, `name`) VALUES (%s, %s);\r" %(str(item[0]), str(item[1]))
            self.writeFile(value, self.filePath.getTextDecksPath())

    # get Top8 players
    def getTop8Players(self):
        df       = pd.read_excel(self.filePath.getExcelPlayersPath())
        itemList = self.getItemListFromExcel(df)
        position = None

        for item in itemList:
            # allways first row is 1st player
            previous = self.getPreviousPosition(item[1], position)
            position = self.getPosition(item[1], previous)

            value    = "INSERT INTO `player` (`name`, `position`, `idTournament`, `idDeck`) VALUES (%s, %s, '%s', '%s');\r" %(item[0], str(position), item[2], str(item[3]))
            self.writeFile(value, self.filePath.getTextPlayersPath())

    # get tournament insert data
    def getTournamentInserts(self):
        df = pd.read_excel(self.filePath.getExcelTournamentPath())
    
        itemList = []

        for index, row in df.iterrows():
            itemList.append(row.to_list())

        with open(self.filePath.getTextTournamentPath(), 'a', encoding='utf-8') as file:
            for item in itemList:
                idLeague = self.getIdLeague(item[1])
                value    = "INSERT INTO `tournament` (`id`, `idTournament`, `name`, `date`, `idLeague`, players) VALUES (%s, %s, '%s', '%s', %s, %s);\r" %(str(item[0]), str(item[0]), item[1], item[2], str(idLeague), str(item[3]))
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

    # get item list values
    def getItemListFromExcel(self, df):
        itemList = []

        for index, row in df.iterrows():
            itemList.append(row.to_list())

        return itemList

    # write to file
    def writeFile(self, value, filePath):
        with open(filePath, 'a', encoding='utf-8') as file:
            file.write(value)
    
    # get cardType
    def getCardType(self, cardName):
        soup     = Scrapping()
        cardName = soup.convertCardName(cardName)

        try:
            soup = soup.getJsonSoup(soup.getScryfallUrlCardData(cardName))
        except Exception:
            print(soup.getScryfallUrlCardData(cardName))
            return ''
        
        if 'planeswalker' in soup['type_line'].lower():
            return 'planeswalker'
        if 'creature' in soup['type_line'].lower():
            return 'creature'
        if 'land' in soup['type_line'].lower():
            return 'land'
        if 'artifact' in soup['type_line'].lower():
            return 'artifact'
        if 'enchantment' in soup['type_line'].lower():
            return 'enchantment'
        if 'sorcery' in soup['type_line'].lower():
            return 'sorcery'
        if 'instant' in soup['type_line'].lower():
            return 'instant'