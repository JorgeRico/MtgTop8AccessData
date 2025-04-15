from access_parser import AccessParser
import pandas as pd
from classes.filePaths import FilePaths

class MSAccessToExcel:
    def __init__(self, file):
        self.db       = AccessParser(file)
        self.filePath = FilePaths()

    # get tournament info
    def getTournaments(self):
        self.parseTableToExcel("Tournaments", ['IdTournament', 'NameTournament', 'DateTournament', 'Observacions'], self.filePath.getExcelTournamentPath(), True)

    # get decks info
    def getDecks(self):
        self.parseTableToExcel("DecksLegacy", ['DeckPlayer', 'IdTop', 'IdTournament', 'IdDeck'], self.filePath.getExcelPlayersPath())
        self.parseTableToExcel("DecksLegacy", ['IdDeck', 'DeckName', 'DeckPlayer', 'IdTournament'], self.filePath.getExcelDecksPath())
    
    # get deck cards
    def getCards(self):
        self.parseTableToExcel("CardsPerDeck", ['CardName', 'IdDeck', 'QuantityInMaindeck', 'QuantityInSideboard'], self.filePath.getExcelCardsPath())
        
    # parse table and convert
    def parseTableToExcel(self, tableName, cols, filePath, isTournamentException = False):
        table = self.db.parse_table(tableName)
        df    = pd.DataFrame(table, columns=cols)

        # modify values
        if isTournamentException == True:
            df['DateTournament'] = df['DateTournament'].apply(self.modifyTournamentDate)
            df['Observacions']   = df['Observacions'].apply(self.modifyTournamentPlayervalues)

        self.convertToExcel(df, filePath)

    # convert to excel
    def convertToExcel(self, df, fileName):
        df.to_excel(fileName, sheet_name='Results', index=False)
        print('  -- File saved %s' %fileName)

    # modify tournament date
    def modifyTournamentDate(self, value):
        value         = value.replace(' 00:00:00', '')
        splittedValue = value.split('-')
        dateValue     = splittedValue[2] + '/' + splittedValue[1] + '/' + splittedValue[0][2] + splittedValue[0][3] 

        return dateValue

    # parse only number of players
    def modifyTournamentPlayervalues(self, value):
        value = value.replace('torneig de la LCL 2019', '')
        value = value.replace('torneig de la LCL 2020', '')
        value = value.replace('torneig de la LCL 2022', '')
        value = value.replace('torneig de la LIL 2023', '')
        value = value.replace('torneig LCL 2023', '')
        value = value.replace('La Farinera', '')
        value = value.replace('inGenio Games', '')
        value = value.replace('inGenio', '')
        value = value.replace('-2024', '')
        value = value.replace('-24', '')
        value = value.replace('Darrer torneig de la LCL 2023', '')
        value = value.replace('jugadors', '')
        value = value.replace('Torneig invitacional final de la LCL 2019', '')
        value = value.replace('Torneig invitacional', '')
        value = value.replace(' torneig de la LCL 2025', '')
        value = value.replace("La LIL es converteix en LCL a partir d'aquest torneig", '')
        value = value.replace('1r', '')
        value = value.replace('2r', '')
        value = value.replace('2n', '')
        value = value.replace('3r', '')
        value = value.replace('4t', '')
        value = value.replace('5è', '')
        value = value.replace('6è', '')
        value = value.replace('7è', '')
        value = value.replace('8è', '')
        value = value.replace('9è', '')
        value = value.replace('10è', '')
        value = value.replace('11è', '')
        value = value.replace('\n', '')
        value = value.replace('\r', '')
        value = value.replace('participants', '')
        value = value.replace('classificats', '')
        value = value.replace('presentats', '')

        # final tournament exceptions
        valueSplitted = value.split(',')
        if len(valueSplitted) == 2:
            return valueSplitted[1].strip()

        return value.strip()

    # Print DB tables
    def printTableList(self):
        print(self.db.catalog)

    # Pretty print all tables
    def printDatabase(self):
        self.db.print_database()
