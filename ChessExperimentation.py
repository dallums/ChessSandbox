# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 08:05:03 2017

@author: Derek
"""



import requests, json, chess, chess.pgn
from pprint import pprint



GlobalSettings = {'SecretKey': '',\
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
    game_data_from_PGN = PGNParser(aPGN, moveNum)
    board = game_data_from_PGN.end().board()
    pieceDictionary = board.piece_map()
    bishops_and_knights = {'B': 0, 'b': 0, 'N': 0, 'n': 0} #white bishops, black bishops, white knights, black knights
    
    for piece in pieceDictionary.values():
        piece = str(piece)
        try:
            bishops_and_knights[piece] += 1
        except:
            pass
        
    return bishops_and_knights, pieceDictionary
       

def openOrClosed(pieces):
    """returns extent to which a game is open or closed at a certain time - needs to be built"""
#    Taken from cgss on chess.SE:
#    Number of pawns(a position with no pawns is apparently wide open).
#    Number of pawn moves(assuming a position with three pawns each,there's a big difference if they are on f2,g2,f7 and f7,g7,h7 respectively and if they are on c4,d5,e4 and c5,d6,e5.
#    As you see in 2 you may give an extra weight for pawn moves in the center. Generally it will be a good idea to give extra weight for anything open in the center. This will be more clear in 4.
#    Number of open and semi-open files. The ones in the center again should have an extra weight.
#    Open diagonals. Note that diagonals with one or more isolani should be counted almost as opens(As an example think about the Indian's bishop targeting d4 and b2 when the c pawn is not on c3). And you should of course take into consideration the length of the diagonal.
#          
#    Another idea from chess.SE from Philip Roe:
#    Look at every piece on the board, and count the number of moves that it would have if there was nothing else on the board. Add this up for all pieces on both sides and call it $N_{empty}$.
#    Now count the number of moves/captures that each piece actually has and add these. Call this total $N_{actual}$. The ratio $N_{actual}/N_{empty}$ is a measure of the open-ness of the position.
                                                                                    
    return 0


    
if __name__ == "__main__":
    moveNumber = 1
    randomID = getRandomGameID()
    
    entirePGN = getPGN(randomID)
    game_data_from_PGN = PGNParser(entirePGN, moveNumber)
    board = game_data_from_PGN.end().board()
    opening, result = getOpeningAndResult(getJSONFromGameID(randomID))
    print(board) 
    
    bishops_and_knights, pieces_on_board = PiecesOnBoard(entirePGN , moveNumber) 
    print(bishops_and_knights)
    
    howOpen = openOrClosed(pieces_on_board)

    
