from classes.filePaths import FilePaths
from classes.supabase.dbSupabase import DbSupabase

class Queries:

    def __init__(self):
        self.filePath = FilePaths()
        self.db       = DbSupabase()
    
    # tournament insert query
    def insertTournamentQuery(self, line, idLeague):
        item = {
            "id"           : line['idTournament'], 
            "idTournament" : line['idTournament'], 
            "name"         : line['name'], 
            "date"         : line['date'], 
            "idLeague"     : idLeague, 
            "players"      : line['players']
        }

        self.db.insert('tournaments', item)

    def existsTournament(self, id, idTournament, idLeague):
        supabase = self.db.getSupabase()
        result   = supabase.table('tournaments').select('id').eq('id', id).eq('idTournament', idTournament).eq('idLeague', idLeague).execute()

        return result.data

    # get list of excluded decks
    def existsLeague(self, idLeague):
        return self.db.getTableDataQueryWhere('leagues', 'id', 'id', int(idLeague))
    
    # league insert or update query
    def insertLeagueQuery(self, idLeague, year, leagueName):
        item = {
            "id"     : idLeague, 
            "name"   : leagueName, 
            "year"   : year, 
            "active" : 1 
        }

        self.db.insert('leagues', item)

    # tournament top8 - top16 multiple players insert query
    def insertMultipleTournamentPlayerQuery(self, players, previousTournament):
        for player in players:
            exist = self.existsTournamentPlayer(player)

            if len(exist) == 0:
                item = {
                    "name"         : player['name'], 
                    "position"     : player['position'], 
                    "idTournament" : player['idTournament'],
                    "idDeck"       : player['idDeck']
                }

                self.db.insert('players', item)
            print("    -- Top Players Added Tournament: %s" %previousTournament)

    # get list of excluded decks
    def existsTournamentPlayer(self, player):
        supabase = self.db.getSupabase()
        result   = supabase.table('players').select('idDeck, id').eq('name', player['name']).eq('position', player['position']).eq('idTournament', player['idTournament']).execute()
        
        return result.data
    
    # get list of excluded decks
    def existsTournamentPlayerDeck(self, deck):
        supabase = self.db.getSupabase()
        result   = supabase.table('decks').select('id').eq('name', deck['name']).eq('id', deck['id']).execute()

        return result.data


    # tournament multiple deck insert query
    def insertMultipleDeckQuery(self, decks):
        for deck in decks:
            if len(self.existsTournamentPlayerDeck(deck)) == 1:
                print("        !! Deck is on DB: %s - %s" %(deck['id'], deck['name']))
            else:
                item = {
                    "id"          : deck['id'], 
                    "name"        : deck['name'], 
                    "cardsLoaded" : False
                }

                self.db.insert('decks', item)
                print("        !! Deck insert: %s - %s" %(deck['id'], deck['name']))

    # get list of excluded decks
    def deckIsLoaded(self, idDeck):
        supabase = self.db.getSupabase()
        result   = supabase.table('decks').select('cardsLoaded').eq('id', idDeck).execute()

        return result.data
    
    # deck cards insert query
    def insertMultipleCardsQuery(self, cards, previousDeck):
        result = self.deckIsLoaded(cards[0]['idDeck'])

        # TODO: 8564, 8762 is an exception - need to be fixed manually
        if cards[0]['idDeck'] != 8564 and cards[0]['idDeck'] != 8762:
            if result[0].get('cardsLoaded') == False:
                for card in cards:
                    item = {
                        "name"     : card['name'],
                        "num"      : card['num'], 
                        "idDeck"   : card['idDeck'], 
                        "board"    : card['board'], 
                        "cardType" : card['cardType']
                    }

                    self.db.insert('cards', item)
                self.db.update('decks', {'cardsLoaded' : True}, 'id', card['idDeck'])
                print("        -- Cards added - idDeck: %s" %previousDeck)
            else:    
                print('        !!! Deck cards is on DB - idDeck: %s' %cards[0]['idDeck'])
    
    # get list of excluded decks
    def existsIdDeck(self, idDeck):
        return self.db.getTableDataQueryWhere('players', 'id', 'idDeck', idDeck)

    # check if Tournament exists
    def existsTournamentOnDB(self, idTournament):
        return self.db.getTableDataQueryWhere('tournaments', 'id', 'idTournament', idTournament)
    
    # get player id - keep alive old ids
    def getPlayerIdDeckOnDB(self, name, idTournament):
        supabase = self.db.getSupabase()
        result   = supabase.table('players').select('idDeck, id').eq('name', name).eq('idTournament', idTournament).execute()

        return result.data
