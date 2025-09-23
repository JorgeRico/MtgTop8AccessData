from classes.mysql.db import Db

class Queries:

    def __init__(self):
        self.db = Db()
    
    # tournament insert query
    def insertTournamentQuery(self, line, idLeague):
        query = 'INSERT INTO tournament (id, idTournament, name, date, idLeague, players) VALUES ( "%s", "%s", "%s", "%s", "%s", "%s" );' %(line['idTournament'], line['idTournament'], line['name'], line['date'], idLeague, line['players'])
        self.db.executeInsertQuery(self.db.connection(), query)
    
    # league insert or update query
    def insertLeagueQuery(self, idLeague, year, leagueName):
        query = 'INSERT INTO league (id, name, year, active) VALUES ( "%s", "%s", "%s", 1 ) ' %(idLeague, leagueName, year)
        query += 'ON DUPLICATE KEY UPDATE id="%s", name="%s", year="%s", active=1;' %(idLeague, leagueName, year)
        self.db.executeInsertQuery(self.db.connection(), query)

    # tournament top8 - top16 multiple players insert query
    def insertMultipleTournamentPlayerQuery(self, line):
        query = 'INSERT INTO `player` ( `name`, `position`, `idTournament`, `idDeck` ) VALUES %s' %line
        self.db.executeInsertQuery(self.db.connection(), query)

    # top8 players query values
    def saveTournamentPlayersList(self, tournamentPlayers):
        query = ''
        for player in tournamentPlayers:
            query += ' ( "%s", "%s", "%s", "%s" ),' %(player['name'], player['position'], player['idTournament'], player['idDeck'])

        return self.replaceLastQueryChar(query)

    # tournament multiple deck insert query
    def insertMultipleDeckQuery(self, line):
        query = 'INSERT INTO `deck` (`id`, `name`, `cardsLoaded`) VALUES %s' %line
        self.db.executeInsertQuery(self.db.connection(), query)

    # tournament deck values query
    def saveDecksList(self, decks):
        query = ''
        for deck in decks:
            query += ' ( "%s", "%s", "%s" ),' %(deck['id'], deck['name'], True)

        return self.replaceLastQueryChar(query)

    # deck cards insert query
    def insertMultipleCardsQuery(self, line):
        query = 'INSERT INTO `cards` (`name`, `num`, `idDeck`, `board`, `cardType`) VALUES %s' %line
        self.db.executeInsertQuery(self.db.connection(), query)

    # multiple card query values
    def saveDeckCardsList(self, deckListCards):
        query = ''
        for card in deckListCards:
            query += ' ( "%s", "%s", "%s", "%s", "%s" ),' %(card['name'], card['num'], card['idDeck'], card['board'], card['cardType'])

        return self.replaceLastQueryChar(query)
    
    # get list of excluded decks
    def existsIdDeck(self, idDeck):
        query = 'SELECT id FROM player WHERE idDeck = %s' %idDeck 

        return self.db.selectQuery(self.db.connection(), query)

    # check if Tournament exists
    def existsTournamentOnDB(self, idTournament):
        query = 'SELECT id as id FROM tournament WHERE idTournament = %s;' %(idTournament)
        
        return self.db.selectQuery(self.db.connection(), query)
    
    # get player id - keep alive old ids
    def getPlayerIdDeckOnDB(self, name, idTournament):
        query = 'SELECT idDeck as idDeck, id as idPlayer FROM player WHERE name = "%s" AND idTournament = %s;' %(name, idTournament)
        
        return self.db.selectQuery(self.db.connection(), query)
        
    # change last "," by ";"
    def replaceLastQueryChar(self, query):
        query = query[:-1] + ';'

        return query
           