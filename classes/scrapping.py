import urllib
import urllib.request
from bs4 import BeautifulSoup
import json
import unidecode

class Scrapping:
    def __init__(self):
        self.scryfall = 'https://api.scryfall.com/cards'

    # get soup
    def getSoup(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        return soup
    
    def getJsonSoup(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        data = json.loads(soup.text.encode('utf-8'))

        return data
    
    def getScryfallUrlCardData(self, name):
        return self.scryfall + '/named?exact=' + name
    
    def convertCardName(self, cardName):
        cardName = unidecode.unidecode(cardName)
        cardName = cardName.replace('L 3/4rien', 'Lorien')
        cardName = cardName.replace('Lurien', 'Lorien')
        cardName = cardName.replace('LUrien', 'Lorien')
        cardName = cardName.replace('dZm', 'dum')
        cardName = cardName.replace(' ', '%20')
        cardName = cardName.replace(',', '')
        cardName = cardName.replace('&', '')

        return cardName
