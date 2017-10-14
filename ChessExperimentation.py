# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 08:05:03 2017

@author: Derek
"""



import requests, json, chess, chess.pgn
from pprint import pprint



GlobalSettings = {'SecretKey': ###,\
                  'GameFromID': 'http://chess.rest/gameref/game',\
                  'GameFromPGN': 'http://chess.rest/gameref/pgn.json',\
                  'RandomGame': 'http://chess.rest/gameref/random.json'}
Headers = {
          "Accept": "application/json",
          "X-Chess-Api-Secret": GlobalSettings['SecretKey']
          }



def getRandomGameID():
    response = requests.get(GlobalSettings['RandomGame'], headers = Headers)
    responseJSON = json.loads(response.text)
    return responseJSON['contents']['games'][0]['id']


def getRandomPGN():
    randomID = getRandomGameID()
    r = requests.get(GlobalSettings['GameFromPGN'], params={'id':randomID}, headers = Headers)
    d = json.loads(r.text) 
    PGN = d['contents']['pgn']
    return PGN


def PGNParser(aPGN):
    """parses the returned object from the chess.rest API"""
    #to be added
    return None
       

    
if __name__ == "__main__":
    randomID = getRandomGameID()
    randomPGN = getRandomPGN()
    board = chess.Board()
    
    