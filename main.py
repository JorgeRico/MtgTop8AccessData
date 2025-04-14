from classes.access import MSAccess

if __name__ == "__main__":
    # data from 2019 to 2025
    db = MSAccess('data/origin/data.mdb')

    print(' -- Access DB export Starting!!!')
    db.getTournaments()
    db.getDecks()
    db.getCards()
    print(' -- Access DB export Finished!!!')