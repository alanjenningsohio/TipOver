# TipOver
Practice in Python by coding up a game

Hi Everyone, 
I need practice getting into the Python syntax, so I made did up the table top puzzel Tip Over: 
https://www.thinkfun.com/products/tipover/ 

The basic of the game is that there is a 6x6 grid with a tipper and individual towers of different heights. The tipper knocks over the tower he is standing on in a cardinal direction landing on top of it. The goal of the game is to get the tipper to the goal block (the 1-story tower). Because the tipper can only move on conected blocks, and towers cannot fall outside the grid or on other towers, finding a solution is a puzzel. 

This project recreates the mechanics of the game: holding the state of the board, accepting actions, and resolving them. 
Only two maps from the game have been included. Users would be encouraged to support the publisher/developer by purchasing a new or used version. ThinkFun even has some bonus challenges you can get from their product page. 
It is plan text. Doing up graphics, well, it seems graphics libraries change everytime I go to play in Python, so I wasn't going to both. That being said, It's pretty lame plan text also. Definitely room for improvement. 
It has no solver. I'm trying to remember, and I don't even think it records your solution (or attempted solution). I tried to make the class structure allow for this expansion easily, as from a programming point of veiw, this is a logical next step. Turns out there's even a Yale CS assignment on it: 
https://web.archive.org/web/20211227162514/https://zoo.cs.yale.edu/classes/cs474/f2021/Assignments/tipover.html 

Because this project is tutorial for me, I am leaving in milestone versions. Now that it's in a repository, they will be removed with the next major versioning (if that ever happens) since differencing can be done through history. 

If you have interest in contributing, please let me know. I just don't anticipate any interest, and that's why I didn't open it to the public. 

Best Regards, Alan 

---------------
v0: Prototype
---------------
v1: Separating into a driver (main) and class.
---------------
