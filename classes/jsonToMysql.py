from classes.filePaths import FilePaths
from classes.db import Db
import json

class JsonToMysql:
    def __init__(self):
        self.filePath = FilePaths()

    def readFile(self):
        print('read file')
        db         = Db()
        connection = db.connection()

        print(self.filePath.getJsonTournamentPath())

        with open(self.filePath.getJsonTournamentPath(), 'r') as openfile:
            # Reading from json file
            jsonObject = json.load(openfile)

        print(jsonObject)
        # for line in jsonObject:
        #     print(line)

        
           