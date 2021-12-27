# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:07:16 2021

@author: Wicked Al

Note NumPi is 0 based indexing 
"""

import numpy as np

print (np.sin(1.5))

Board = np.array(np.zeros([6,6]))

class TipOverGame:
    def __init__(self,Level=0, Definition=""):
        self._board = Board(Level, Definition)
    def Play(self):
        tmp_flagPlaying = True 
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
            self._board.CheckWin()
            tmp_flagPlaying = not(self._board.flagWon)
            # tmp_flagPlaying = False # prototyping for now 
    
    

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
        self._boardArray[self._winSpot[0],self._winSpot[1]] = -1 
        # could change the winning spot to a 1, but keeping distinct from toppled blocks for now 
        print(self._boardArray)
        print(self._tipperSpot)

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
                        # print(f"Found match: ({temp_count},{tmp_row},{tmp_col})")
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
                flag_running = False
        # finished checking array 
        #self._flagValidReach = True
        #print("Tipper Spot")
        #print(self._tipperSpot)
        #print("Board Array")
        #print(self._boardArray)
        #print("Reachable Array")
        #print(self._reachArray)

    def CheckWin(self):
        if not self._flagValidReach:
            self.FindReachable()
        if self._reachArray[self._winSpot[0],self._winSpot[1]]>0:
            self.flagWon = True
            print("You Won")
        # else : # debatable if this should be coded in, there an argument to keep default
        #     self.flagWon = False

            #!# Future: print list of moves 

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
                    else: # could 
                        tmp_flagValid = False
                        break
            elif (Direction == 'D'):
                tmp_tipper[0]=tmp_tipper[0]+1
                for tmp_fill in range(tmp_len):
                    if (((Row+(tmp_fill+1))<self._BOARDSIZE) and 
                        tmp_board[Row+(tmp_fill+1),Col]==0):
                        tmp_board[Row+(tmp_fill+1),Col] = 1
                    else: # could 
                        tmp_flagValid = False
                        break
            elif (Direction == 'L'):
                tmp_tipper[1]=tmp_tipper[1]-1
                for tmp_fill in range(tmp_len):
                    if (((Col-(tmp_fill+1))>=0) and 
                        tmp_board[Row,Col-(tmp_fill+1)]==0):
                        tmp_board[Row,Col-(tmp_fill+1)] = 1
                    else: # could 
                        tmp_flagValid = False
                        break
            elif (Direction == 'R'):
                tmp_tipper[1]=tmp_tipper[1]+1
                for tmp_fill in range(tmp_len):
                    if (((Row+(tmp_fill+1))<self._BOARDSIZE) and 
                        tmp_board[Row,Col+(tmp_fill+1)]==0):
                        tmp_board[Row,Col+(tmp_fill+1)] = 1
                    else: # could 
                        tmp_flagValid = False
                        break
            else: 
                print("Never should reach this spot based on input checking")

            if (tmp_flagValid ) : 
                self._boardArray = tmp_board.copy()
                self._tipperSpot = tmp_tipper.copy()
                self._flagValidReach = False
            else : 
                print(f"Invalid move: Piller fell off board or ", \
                      f"collided with something: [{Row},{Col},{Direction}]")
                print("Board Array")
                print(self._boardArray)
                
    def ShowBoard(self): 
        tmp_ColLabel = 'ABCDEFGHIJKLMNOP' 
        # Should have a check somewhere that tmp_ColLabel is not shorter than BOARDSIZE
        # or better yet, conver the tmp_col into ascii
        if not self._flagValidReach:
            self.FindReachable()

        print('     |',end='') 
        tmp_s = '-------'
        for tmp_col in range(self._BOARDSIZE):
            print('{0:^6}'.format(tmp_ColLabel[tmp_col]),end='') 
            tmp_s = tmp_s + '------'
        print('') 
        print(tmp_s,sep='') 
        for tmp_row in range(self._BOARDSIZE):
            print('  {0:2d} |'.format(tmp_row),end='') 
            for tmp_col in range(self._BOARDSIZE):
                if ((tmp_row==self._winSpot[0]) and (tmp_col==self._winSpot[1])):
                    print('{0:*^5} '.format(self._boardArray[tmp_row,tmp_col]),end='',sep='') 
                elif (self._reachArray[tmp_row,tmp_col]>0):
                    print('{0:|^5} '.format(self._boardArray[tmp_row,tmp_col]),end='',sep='') 
                else :
                    print('{0:^5} '.format(self._boardArray[tmp_row,tmp_col]),end='',sep='') 
            print('') 
            
            
                            
            
        
        
        
tmp_Game = TipOverGame(Level = 7)
tmp_Game.Play()


