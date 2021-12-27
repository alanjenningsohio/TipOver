# -*- coding: utf-8 -*-
"""

This file contains the program for playing the TipOver Game 
thinkfun.com/products/tipover/
A tipper moves about a board by tipping over pillars to reach the goal. 

Only a few level are coded. Levels can be added by defining initial 
pillar layout (including the goal), and the starting tipper spot. 

See the main program for playing instuctions, or just read the code :P 

Created on Mon Oct 18 11:07:16 2021
@author: Wicked Al

V0: proof of concept
V1: cleaning up the files
V2: (anticipated) improve user interface, create reset option, 
    check inputs (needed?), 
    was considering debug print statements but seems robust enough

Defincincies: 
    has NOT been tested on sizes other than 6 (min size would be 3...)
    Does not implement user/run-time defined levels
    Does not save nor print out move list on win 
    Does not check for failure (reachable area is at 1 or every possible move 
        falls off board or results in collision)
    Would be fun to create a brute force or better search algorithm, but that's 
        more than an afternoon task. 

Note NumPi is 0 based indexing 
"""

import numpy as np

class TipOverGame:
    def __init__(self,Level=0, Definition=""):
        self._board = Board(Level, Definition)
    def Play(self):
        tmp_flagPlaying = not(self._board.flagWon) # if the game has already been won, print message and exit
        if not (tmp_flagPlaying):
            print('Level needs to be reinitialized')
        while (tmp_flagPlaying): 
            # show the board
            self._board.ShowBoard()
            # Take a players move
            Row, Col, Dir = input("Move (Row #, Col X, Direction (U,D,L,R)): ").split(",")
            Row_Num = int(Row)
            Col_Num = ord(Col)-ord("A") # 0 indexed 
            # Apply the move
            self._board.MakeMove(Row=Row_Num,Col=Col_Num,Direction=Dir)
            # Check for win
            self._board.CheckWin() # this currently prints winning statement 
            tmp_flagPlaying = not(self._board.flagWon)
    
    

class Board: 
    def __init__(self, Level=0, Definition=""):
        self._BOARDSIZE = 6 
        self._boardArray = np.array(np.zeros([self._BOARDSIZE,self._BOARDSIZE],dtype=np.int8))
        self._reachArray = np.array(np.zeros([self._BOARDSIZE,self._BOARDSIZE],dtype=np.int8))
        self._tipperSpot = np.array([np.nan,np.nan]) # a big part of me wants these to be integers, but a bigger part wants NaN to mark as invalid 
        self._winSpot = np.array([np.nan,np.nan])
        self._level = Level
        self._flagValidReach = False
        self.flagWon = False
        if Level == 0 :
            print ("User Defined Levels Not Implemented")
        self.GameLayout()
        self.FindReachable()

    def GameLayout(self):
        self._boardArray.fill(0)
        self._flagValidReach = False
        self.flagWon = False
        if self._level == 1 : 
            self._boardArray[0,3] = 3
            self._boardArray[1,0] = 3
            self._boardArray[2,4] = 2
            self._winSpot  = [4,1]
            self._tipperSpot = [2,4]
        elif self._level == 2 : 
            self._boardArray[0,0] = 4
            self._boardArray[0,4] = 3
            self._boardArray[1,2] = 2
            self._boardArray[1,5] = 2
            self._boardArray[5,0] = 4
            self._boardArray[5,5] = 3
            self._winSpot = [3,3]
            self._tipperSpot = [0,0]
        elif self._level == 7 : 
            self._boardArray[1,1] = 2
            self._boardArray[3,2] = 2
            self._boardArray[4,0] = 3
            self._boardArray[4,2] = 2
            self._boardArray[4,3] = 2
            self._boardArray[5,3] = 2
            self._winSpot = [0,3]
            self._tipperSpot = [5,3]
        #elif Level == 0 :
        #    print ("User Defined Levels Not Implemented")
        else :
            print (f"Level {self._level} Not Implemented.")
            self.flagWon = True # setting this so that game exits if play is attemped
        self._boardArray[self._winSpot[0],self._winSpot[1]] = 1 
        # was using -1 for winning spot, but there really wasn't a need to 
        # treat it different from other flat structure and a winspot variable 
        # made things a lot more convienent

    def FindReachable(self):
        self._reachArray.fill(0)
        flag_running = True
        self._reachArray[self._tipperSpot[0],self._tipperSpot[1]]=1
        temp_count = 1
        while (flag_running) :
            flag_running = False
            for tmp_row in range(self._BOARDSIZE):
                for tmp_col in range(self._BOARDSIZE):
                    if self._reachArray[tmp_row,tmp_col]==temp_count:
                        if (((tmp_row-1)>=0) and  # first check if step falls off board (applies short circuit evaluation)
                        self._reachArray[tmp_row-1,tmp_col]==0   and  # then see if spot has already been assigned
                        self._boardArray[tmp_row-1,tmp_col]!=0) : # and see that it isn't void 
                            self._reachArray[tmp_row-1,tmp_col] = temp_count+1 # assgn it to be checked next round
                            flag_running = True # if any new rechable spot is found, then need to do another loop 
                        # Make sure each step is consistent in block of code 
                        # I made these check explicit vs doing a +1/-1 loop 
                        # since I can apply only the one sided checkes needed and it's only 4 steps. 
                        # If I were working in 6 dimensions, then I probably would make the loops
                        if (((tmp_row+1)<self._BOARDSIZE) and 
                        self._reachArray[tmp_row+1,tmp_col]==0   and 
                        self._boardArray[tmp_row+1,tmp_col]!=0) : 
                            self._reachArray[tmp_row+1,tmp_col] = temp_count+1 
                            flag_running = True 
                        if (((tmp_col-1)>=0) and 
                        self._reachArray[tmp_row,tmp_col-1]==0   and 
                        self._boardArray[tmp_row,tmp_col-1]!=0) : 
                            self._reachArray[tmp_row,tmp_col-1] = temp_count+1
                            flag_running = True
                        if (((tmp_col+1)<self._BOARDSIZE) and 
                        self._reachArray[tmp_row,tmp_col+1]==0   and 
                        self._boardArray[tmp_row,tmp_col+1]!=0) : 
                            self._reachArray[tmp_row,tmp_col+1] = temp_count+1
                            flag_running = True
                    # end of checking around the space
                # end of doing every column in the row
            # finished last row
            temp_count = temp_count+1
            if temp_count > (self._BOARDSIZE*self._BOARDSIZE):
                print("Something has gone very wrong with checking reachability")
                # once this algorithm has maturity of being used, could remove this check
                flag_running = False
        # finished checking array 
        self._flagValidReach = True # note that currently the programs assume 
        # that the FindRechable method succeeds. There is no additional check 
        # after this method is called

    def MakeMove(self,Row, Col, Direction):
        # valid inputs for Direction: 
        # U (Up): row -
        # D (Down): row +
        # L (Left): col -
        # R (Right): col +
        
        if not self._flagValidReach:
            self.FindReachable()

        if ((Row<0) or (Row>=self._BOARDSIZE) or 
            (Col<0) or (Col>=self._BOARDSIZE)):
            print(f"Invalid Move: [Row, Col] off of board: [{Row},{Col}]")
        elif (self._boardArray[Row,Col]==0) : 
            print(f"Invalid Move: [Row, Col] not on structure: [{Row},{Col}]")
            print("Board Array")
            print(self._boardArray)
        elif (self._boardArray[Row,Col]==1) : 
            print(f"Invalid Move: [Row, Col] already flat: [{Row},{Col}]")
            print("Board Array")
            print(self._boardArray)
        elif (self._reachArray[Row,Col]==0) : 
            print(f"Invalid Move: [Row, Col] not reachable: [{Row},{Col}]")
            print("Board Array")
            print(self._boardArray)
            print("Reachable Array")
            print(self._reachArray)
        elif not (Direction in ('U','D','L','R')):
            print(f"Invalid Move Direction [U,D,L,R]: {Direction}")
        else : # basic checks done, but need to still check for collision or exceeding the board 
            tmp_flagValid = True # presume it's a valid move unless shown otherwise
            # Note the copy() method is used, otherwise it was a reference copy 
            # and the prototype was affecting the actual board 
            tmp_board = self._boardArray.copy() # easier to just try and see if it fails
            tmp_tipper= np.array([Row,Col]) # move is the pre-shifted location of tipper
            tmp_len = tmp_board[Row,Col] # copy the length of pillar out, already know it's greater than one
            tmp_board[Row,Col] = 0 # remove the piller from current spot 
            if (Direction == 'U'):
                tmp_tipper[0]=tmp_tipper[0]-1
                for tmp_fill in range(tmp_len):
                    if (((Row-(tmp_fill+1))>=0) and 
                        tmp_board[Row-(tmp_fill+1),Col]==0):
                        tmp_board[Row-(tmp_fill+1),Col] = 1
                    else: # move failed, report failure to user and don't update board 
                        tmp_flagValid = False
                        break
            elif (Direction == 'D'):
                tmp_tipper[0]=tmp_tipper[0]+1
                for tmp_fill in range(tmp_len):
                    if (((Row+(tmp_fill+1))<self._BOARDSIZE) and 
                        tmp_board[Row+(tmp_fill+1),Col]==0):
                        tmp_board[Row+(tmp_fill+1),Col] = 1
                    else: 
                        tmp_flagValid = False
                        break
            elif (Direction == 'L'):
                tmp_tipper[1]=tmp_tipper[1]-1
                for tmp_fill in range(tmp_len):
                    if (((Col-(tmp_fill+1))>=0) and 
                        tmp_board[Row,Col-(tmp_fill+1)]==0):
                        tmp_board[Row,Col-(tmp_fill+1)] = 1
                    else: 
                        tmp_flagValid = False
                        break
            elif (Direction == 'R'):
                tmp_tipper[1]=tmp_tipper[1]+1
                for tmp_fill in range(tmp_len):
                    if (((Row+(tmp_fill+1))<self._BOARDSIZE) and 
                        tmp_board[Row,Col+(tmp_fill+1)]==0):
                        tmp_board[Row,Col+(tmp_fill+1)] = 1
                    else: 
                        tmp_flagValid = False
                        break
            else: 
                print("Never should reach this spot based on input checking")
                # could be removed once there's enough confidence with this section of code

            if (tmp_flagValid ) : # move suceeded, copy the protoype back into the board
                self._boardArray = tmp_board.copy()
                self._tipperSpot = tmp_tipper.copy()
                self._flagValidReach = False
            else : 
                print(f"Invalid move: Piller fell off board or ", \
                      f"collided with something: [{Row},{Col},{Direction}]")
                print("Board Array")
                print(self._boardArray)
                
    def ShowBoard(self): 
        if not self._flagValidReach:
            self.FindReachable()

        print('     |',end='') # start col labels row with space for row labels
        tmp_s = '-------' # this is the horizontal line 
        for tmp_col in range(self._BOARDSIZE):
            print('{0:^6}'.format(chr(tmp_col+ord("A"))),end='') 
            # {# of input:(blank for spacing character)(^ for centering)(# characters)}
            # I don't understand why this takes 6 spaces while the numbers take 5 
            tmp_s = tmp_s + '------'
        print('') # finish the line with a newline 
        print(tmp_s,sep='') # print the horizontal line, the sep isn't needed 
        # since tmp_s is one string, but doesn't hurt and gives me a reference 
        # for the future
        for tmp_row in range(self._BOARDSIZE):
            print('  {0:2d} |'.format(tmp_row),end='') 
            for tmp_col in range(self._BOARDSIZE):
                if ((tmp_row==self._winSpot[0]) and (tmp_col==self._winSpot[1])):
                    print('{0:*^5} '.format(self._boardArray[tmp_row,tmp_col]),end='',sep='') 
                    # winning spot centered in stars
                elif (self._reachArray[tmp_row,tmp_col]>0):
                    print('{0:|^5} '.format(self._boardArray[tmp_row,tmp_col]),end='',sep='') 
                    # reachable area centered in bars (if winning spot is reachable, game is won)
                else :
                    print('{0:^5} '.format(self._boardArray[tmp_row,tmp_col]),end='',sep='') 
                    # the rest of the board 
            print('') # ending each row with a new line 
            
            
    def CheckWin(self):
        if not self._flagValidReach:
            self.FindReachable()
        if self._reachArray[self._winSpot[0],self._winSpot[1]]>0:
            self.flagWon = True
            print("You Won")
            self.ShowBoard()
        # else : # debatable if this should be coded in, there an argument to keep default
        #     self.flagWon = False
        # Note flagWon == True is also used to show that the level wasn't 
        # properly initialized. Just caution if it's used to trigger other 
        # events, should consider initialization to invalid level. 
        #!# Future: print list of moves 
        
