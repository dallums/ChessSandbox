# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 08:05:03 2017

@author: Derek
"""



import requests, json, chess, chess.pgn
from pprint import pprint



GlobalSettings = {'SecretKey': 'PctfMoGWE5cw_idHjpJymgeF',\
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


def getJSONFromGameID(gameID):
    """Using a random game ID, returns the JSON response of the response object"""
    r = requests.get(GlobalSettings['GameFromID'], params={'id':gameID}, headers = Headers)
    d = json.loads(r.text)
    return d


def getJSONFromPGN(gameID):
    """Returns response object in JSON format from a PGN request using a random ID"""
    r = requests.get(GlobalSettings['GameFromPGN'], params={'id':gameID}, headers = Headers)
    d = json.loads(r.text)
    return d


def getOpeningAndResult(JSONfromid):
    """Simple function just because I expect to use it a alot"""
    opening = JSONfromid['contents']['game']['open_eco']
    result = JSONfromid['contents']['game']['result']
    return opening, result
    

def getPGN(gameID):
    """Gets a random PGN"""
    d = getJSONFromPGN(gameID)
    PGN = d['contents']['pgn']
    return PGN


def PGNParser(aPGN, moveNum):
    """parses the returned object from the chess.rest API after move numvber moveNum"""
    dummyFile = open("dummyPGN.txt", "w")
    moveNum += 1
    moveNum = str(moveNum)+'.'
    
    badIndex = aPGN.index('\r\n\r\n')+4
    goodBeginning = aPGN[:badIndex]
    goodEnding = aPGN[badIndex:].replace('\r\n', ' ') #there was an issue with not reading all the moves due to line breaks
    
    #if moveNum exceeds max number of moves, just return the whole game
    try:
        aPGN = goodBeginning+goodEnding[:goodEnding.index(moveNum)]
    except:
        aPGN = goodBeginning+goodEnding
    
    dummyFile.write(aPGN)
    dummyFile.close()
    
    with open("dummyPGN.txt") as pgn:
        gameFromPGN = chess.pgn.read_game(pgn)
    
    return gameFromPGN


def PiecesOnBoard(aPGN, moveNum):
    """return list of pieces on the board after move number moveNum"""
    game_data_from_PGN = PGNParser(PGN, moveNum)
    board = game_data_from_PGN.end().board()
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
    moveNumber = 100
    randomID = getRandomGameID()
    
    PGN = getPGN(randomID)
    game_data_from_PGN = PGNParser(PGN, moveNumber)
    board = game_data_from_PGN.end().board()
    opening, result = getOpeningAndResult(getJSONFromGameID(randomID))
    print(board) 
    
    bishops_and_knights = PiecesOnBoard(board, moveNumber) #still need to incorporate move number
    print(bishops_and_knights)

    