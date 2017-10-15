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
    """Gets a random game ID"""
    response = requests.get(GlobalSettings['RandomGame'], headers = Headers)
    responseJSON = json.loads(response.text)
    return responseJSON['contents']['games'][0]['id']


def getJSONFromRandomID():
    """Using a random game ID, returns the JSON response of the response object"""
    randomID = getRandomGameID()
    r = requests.get(GlobalSettings['GameFromID'], params={'id':randomID}, headers = Headers)
    d = json.loads(r.text)
    return d


def getJSONFromRandomPGN():
    """Returns response object in JSON format from a PGN request using a random ID"""
    randomID = getRandomGameID()
    r = requests.get(GlobalSettings['GameFromPGN'], params={'id':randomID}, headers = Headers)
    d = json.loads(r.text)
    return d


def getOpeningAndResult(JSONfromid):
    """Simple function just because I expect to use it a alot"""
    opening = JSONfromid['contents']['game']['open_eco']
    result = JSONfromid['contents']['game']['result']
    return opening, result
    

def getRandomPGN():
    """Gets a random PGN"""
    d = getJSONFromRandomPGN()
    PGN = d['contents']['pgn']
    return PGN


def PGNParser(aPGN):
    """parses the returned object from the chess.rest API"""
    dummyFile = open("dummyPGN.txt", "w")
    
    badIndex = aPGN.index('\r\n\r\n')+4
    goodBeginning = aPGN[:badIndex]
    goodEnding = aPGN[badIndex:].replace('\r\n', '') #there was an issue with not reading all the moves due to line breaks
    aPGN = goodBeginning+goodEnding
    
    dummyFile.write(aPGN)
    dummyFile.close()
    
    with open("dummyPGN.txt") as pgn:
        gameFromPGN = chess.pgn.read_game(pgn)
    
    return gameFromPGN


def PiecesOnBoard(board, moveNum):
    """return list of pieces on the board after move number moveNum"""
    pieceDictionary = board.piece_map()
    bishops_and_knights = {'B': 0, 'b': 0, 'N': 0, 'n': 0} #white bishops, black bishops, white knights, black knights
    
    for piece in pieceDictionary.values():
        piece = str(piece)
        try:
            bishops_and_knights[piece] += 1
        except:
            pass
    return bishops_and_knights
       

    
if __name__ == "__main__":
    randomID = getRandomGameID()
    randomPGN = getRandomPGN()
    game_data_from_PGN = PGNParser(randomPGN)
    board = game_data_from_PGN.end().board()
    print(board) 
    
    bishops_and_knights = PiecesOnBoard(board, 10) #still need to incorporate move number
    
