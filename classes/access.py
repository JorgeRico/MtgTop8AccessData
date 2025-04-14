from access_parser import AccessParser
import pandas as pd

class MSAccess:
    def __init__(self, file):
        # .mdb or .accdb file
        self.db                 = AccessParser(file)
        self.tournamentFilePath = 'data/access/tournaments.xlsx'
        self.decksFilePath      = 'data/access/decks.xlsx'
        self.cardsFilePath      = 'data/access/cards.xlsx'

    # get tournament info
    def getTournaments(self):
        # new database fields
        # (idTournament, name, date, idLeague)
        
        # parse table
        table = self.db.parse_table("Tournaments")
        df    = pd.DataFrame(table, columns=['IdTournament', 'NameTournament', 'DateTournament'])
        self.convertToExcel(df, self.tournamentFilePath)

    # get decks info
    def getDecks(self):
        # new database fields
        # deck (name, idPlayer)
        # player (name, position, idTournament)
        
        # parse table
        table = self.db.parse_table("DecksLegacy")
        df    = pd.DataFrame(table, columns=['IdDeck', 'DeckName', 'DeckPlayer', 'IdTournament', 'IdTop'])
        self.convertToExcel(df, self.decksFilePath)

    def getCards(self):
        # new database fields
        # cards (name, num, idDeck, board, cardType) 
        table = self.db.parse_table("CardsPerDeck")
        df    = pd.DataFrame(table, columns=['IdDeck', 'CardName', 'QuantityInMaindeck', 'QuantityInSideboard'])
        self.convertToExcel(df, self.cardsFilePath)
        
    # convert to excel
    def convertToExcel(self, df, fileName):
        df.to_excel(fileName, sheet_name='Results', index=False)


    # Print DB tables
    def printTableList(self):
        print(self.db.catalog)

    # Pretty print all tables
    def printDatabase(self):
        self.db.print_database()
