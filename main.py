from classes.access import MSAccess

def accessToExcel():
    # data from 2019 to 2025
    db = MSAccess('data/origin/data.mdb')

    print(' -- Access DB export Starting!!!')
    db.getTournaments()
    db.getDecks()
    db.getCards()
    print(' -- Access DB export Finished!!!')

if __name__ == "__main__":
    accessToExcel()

    # print(' -- Read Tournament excel file')
    