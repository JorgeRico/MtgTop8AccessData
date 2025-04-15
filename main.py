from classes.access import MSAccess
from classes.mysql import Mysql
import pandas as pd

def accessToExcel():
    # data from 2019 to 2025
    data = MSAccess('data/origin/data.mdb')

    print(' -- Access DB export Starting!!!')
    data.getTournaments()
    data.getDecks()
    data.getCards()
    print(' -- Access DB export Finished!!!')

def excelToInsertText():
    data = Mysql()

    print(' -- Generate Insert Files Start!!!')
    data.getTournamentInserts()
    data.getTop8Players()
    data.getTop8PlayerDeck()
    data.getDeckCards()
    print(' -- Generate Insert Files Finished!!!')


if __name__ == "__main__":
    accessToExcel()
    excelToInsertText()

        

    