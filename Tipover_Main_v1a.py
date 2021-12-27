# -*- coding: utf-8 -*-
"""
This file plays the TipOver Game 
thinkfun.com/products/tipover/
A tipper moves about a board by tipping over pillars to reach the goal. 

Game starts by selecting a level. 
The game board is shown. 
    Each elemet of the array shows if there a pillar on the spot and how tall 
        it is (1 to 4). 
    The tipper can only reach orthogonally connected pillars. The relative 
        height doesn't matter This reachable area is shown by vertical bars (|). 
    The game ends when the tipper can reach the goal spot, shown by the stars 
        (*). The goal space is always 1 unit high (cannot be tipped, not that 
        it makes a difference because the games ends when it's reached.)
The player will continue to make moves until the goal is reached. (There is no 
    failure check.)
    Moves are made by selecting a coorindate in the reachable area 
        (row is 0 indexed, Col is capital letter from A and direction for the 
        tip is U (UP), D (Down), L (Left), R (Right)). Note that the act of 
        tipping will move the piller from the space it starts. Making a move 
        will result in a different board layout (this will not be printed till 
        following move, unless you won (no future turn)). If the move is 
        invalid, then an error will be printed and no change to the board will 
        be made. 
After each move, the game will check for a win. If the tipper has reached the 
    goal, then the game will print a winning message and exit. 

See Class function for limitations.

Created on Mon Oct 18 11:07:16 2021
Version v1a: Mon Oct 18 15:51:07 2021 BooHaw!!! 
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
"""

# load the program into local memory 
# import Tipover_Main_v1a as TOGame
from Tipover_Class_v1a import TipOverGame 

        
tmp_Game = TipOverGame(Level = 7) # creat the game at the desired level
tmp_Game.Play() 


