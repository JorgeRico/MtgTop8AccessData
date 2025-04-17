import pandas as pd
from classes.scrapping import Scrapping
from classes.filePaths import FilePaths
import json
class ExcelToJson:
    def __init__(self):
        self.filePath = FilePaths()

    # get deck cards
    def getDeckCards(self):
        print('    -- Cards takes a lot of time . . . .')
        df       = pd.read_excel(self.filePath.getExcelCardsPath())
        itemList = self.getItemListFromExcel(df)
        values   = []

        for item in itemList:
            cardType = self.getCardType(item[0])

            # main cards
            if int(item[2]) > 0:
                value = {
                    "name"     : item[0],
                    "num"      : item[2],
                    "idDeck"   : item[1],
                    "board"    : 'md',
                    "cardType" : cardType
                }
                values.append(value)

            # sideboard cards
            if int(item[3]) > 0:
                value = {
                    "name"     : item[0],
                    "num"      : item[3],
                    "idDeck"   : item[1],
                    "board"    : 'sb',
                    "cardType" : cardType
                }
                values.append(value)

        self.writeJsonFile(values, self.filePath.getJsonCardsPath())

    # get top8 player deck
    def getTop8PlayerDeck(self):
        df       = pd.read_excel(self.filePath.getExcelDecksPath())
        itemList = self.getItemListFromExcel(df)
        values   = []

        for item in itemList:
            value = {
                "id"           : item[0],
                "name"         : item[1],
                "player"       : item[2],
                "idTournament" : item[3]
            }

            values.append(value)
        self.writeJsonFile(values, self.filePath.getJsonDecksPath())

    # get Top8 players
    def getTop8Players(self):
        df       = pd.read_excel(self.filePath.getExcelPlayersPath())
        itemList = self.getItemListFromExcel(df)
        values   = []

        # allways first row is 1st player
        position             = 1
        previousIdTournament = 0
        newTournament        = False

        for item in itemList:
            if int(previousIdTournament) != int(item[2]) and previousIdTournament != 0:
                newTournament = True
            else:
                newTournament = False

            exceptionPosition = self.setTournamentPositionException(item[2], position, newTournament)
            if exceptionPosition is not None:
                position = exceptionPosition
            else:
                previous = self.getPreviousPosition(item[1], position)
                position = self.getPosition(item[1], previous)

            value = {
                "name"         : item[0],
                "position"     : position, 
                "idTournament" : item[2],
                "idDeck"       : item[3]
            }

            values.append(value)

            previousIdTournament = item[2]
        self.writeJsonFile(values, self.filePath.getJsonPlayersPath())

    # 2023 tournaments position exceptions
    def setTournamentPositionException(self, idTournament, position, newTournament):
        exceptions = [ 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209 ]
        if int(idTournament) in exceptions:
            if newTournament == True:
                return 1
            else:
                return int(position) + 1
            
        return None

    # get tournament insert data
    def getTournamentInserts(self):
        df       = pd.read_excel(self.filePath.getExcelTournamentPath())
        itemList = self.getItemListFromExcel(df)
        values   = []

        for item in itemList:
            idLeague = self.getIdLeague(item[1])

            value = {
                "id"           : str(item[0]),
                "idTournament" : str(item[0]), 
                "name"         : item[1], 
                "date"         : item[2], 
                "idLeague"     : str(idLeague),
                "players"      : str(item[3])
            }

            values.append(value)
        self.writeJsonFile(values, self.filePath.getJsonTournamentPath())

    # get previous position number
    def getPreviousPosition(self, item, position):
        if item == 1:
            return item
        else:
            return position

    # conversion position number
    def getPosition(self, position, previousValue):
        if int(position) == 0:
            return int(position)+1
        
        if int(position) == 1:
            return int(position)
    
        if int(position) == 2:
            return int(previousValue)+1
            
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
    def writeJsonFile(self, values, filePath):
        with open(filePath, 'w', encoding='utf-8') as outfile:
            json.dump({"data": values}, outfile)
            outfile.write('\n')
        print('  -- File saved %s' %filePath)
    
    # get cardType - get info from scryfall website
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