"""
15-110 Hw6 - Battleship Project
Name:
AndrewID:
"""

import hw6_battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4



"""
15-110 Hw6 - Battleship Project
Name:
AndrewID:
"""

import hw6_battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
#5 [Check6-1] & #3 [Check6-2] & #3 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["boardSize"] = 500
    data["cellSize"] = 50
    data["numShips"] = 5
    data["user"] = emptyGrid(data["rows"],data["cols"])
    data["computer"] = addShips(emptyGrid(data["rows"],data["cols"]), data["numShips"])
    data["tempShip"] = []
    data["countShips"] = 0
    data["winner"] = None
    data["turns"] = 0
    data["maxTurns"] = 50
    data["restart"] = False
    


'''
makeView(data, userCanvas, compCanvas)
#6 [Check6-1] & #2 [Check6-2] & #3 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    emtGrid = emptyGrid(data["rows"], data["cols"])
    drawGrid(data, userCanvas, data["user"], True)
    drawGrid(data, compCanvas, data["computer"], False)
    
    drawShip(data, userCanvas, data["tempShip"])
    
    if data["winner"] != None :
        drawGameOver(data, userCanvas)
        
    if data["restart"] :
        makeModel(data)
        drawGrid(data, userCanvas, data["user"], True)
        drawGrid(data, compCanvas, data["computer"], False)


'''
keyPressed(data, events)
#5 [Hw6]
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return" and data["winner"] != None:
        data["restart"] = True


'''
mousePressed(data, event, board)
#5 [Check6-2] & #1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; mouse event object ; str
Returns: None
'''
def mousePressed(data, event, board):
    coor = getClickedCell(data, event)
    if board == "user" :
        clickUserBoard(data, coor[0], coor[1])
    if board == "comp" and data["countShips"] == 5 and data["winner"] == None:
        runGameTurn(data, coor[0], coor[1])
    pass

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
#1 [Check6-1]
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for row in range (rows) :
        temp = []
        for col in range (cols) :
            temp.append(EMPTY_UNCLICKED)
        grid.append(temp)
    return grid



'''
createShip()
#2 [Check6-1]
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    ship = []
    row = random.randint(1,8)
    col = random.randint(1,8)
    direction = random.randint(0,1)
    if direction == 0 :
        ship = [[row, col-1], [row, col], [row, col+1]]
    else :
        ship = [[row-1, col], [row, col], [row+1, col]]
    return ship


'''
checkShip(grid, ship)
#3 [Check6-1]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for row in range (len(ship)) :
        storeR = ship[row][0]
        storeC = ship[row][1]
        if grid[storeR][storeC] != EMPTY_UNCLICKED :
            return False
    return True


'''
addShips(grid, numShips)
#4 [Check6-1]
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    while (numShips > 0) :
        newShip = createShip()
        if(checkShip(grid, newShip)) :
            for row in range (len(newShip)) :
                storeR = newShip[row][0]
                storeC = newShip[row][1]
                grid[storeR][storeC] = SHIP_UNCLICKED
            numShips -= 1
    return grid



'''
drawGrid(data, canvas, grid, showShips)
#6 [Check6-1] & #1 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''

def drawGrid(data, canvas, grid, showShips):
    x = data["cellSize"]
    for row in range (data["rows"]) :
        for col in range (data["cols"]) :
            if grid[row][col] == SHIP_UNCLICKED and showShips :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "yellow")
            elif grid[row][col] == SHIP_CLICKED :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "red")
            elif grid[row][col] == EMPTY_CLICKED :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "white")
            else :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "blue")
            


### WEEK 2 ###

'''
isVertical(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    if ((ship[0][1]) == (ship[1][1]) == (ship[2][1])):
        xmost = max(ship)
        xleast = min(ship)
        if (xmost[0] - xleast[0]) == 2 :
            return True
    return False


'''
isHorizontal(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    if (ship[0][0]) == (ship[1][0]) == (ship[2][0]) :
        ymost = max(ship)
        yleast = min(ship)
        if (ymost[1] - yleast[1]) == 2 :
            return True
    return False

'''
getClickedCell(data, event)
#2 [Check6-2]
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x, y = event.x, event.y
    cellSize = data["cellSize"]
    col  = x // cellSize
    row = y // cellSize
    vals = [row,col]
    return vals



'''
drawShip(data, canvas, ship)
#3 [Check6-2]
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    x = data["cellSize"]
    for curr in range (len(ship)) :
        currZero = ship[curr][0]
        currOne = ship[curr][1]
        canvas.create_rectangle((currOne * x), (currZero * x), (currOne * x) + x, (currZero * x) + x, fill = "white")
        


'''
shipIsValid(grid, ship)
#4 [Check6-2]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship) == 3 and checkShip(grid, ship) and (isVertical(ship) or isHorizontal(ship)) :
        return True
    return False


'''
placeShip(data)
#4 [Check6-2]
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["user"], data["tempShip"]) :
        for curr in range (len(data["tempShip"])) :
            currZero = data["tempShip"][curr][0]
            currOne = data["tempShip"][curr][1]
            data["user"][currZero][currOne] = SHIP_UNCLICKED
        data["countShips"] += 1
    else :
        print("Sorry you can't do that. Try another ship.")
    data["tempShip"] =[]

'''
clickUserBoard(data, row, col)
#4 [Check6-2]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if [row, col] in data["tempShip"] or data["countShips"] == 5 :
        return
    
    data["tempShip"].append([row, col])
    
    if len(data["tempShip"]) == 3 :
        placeShip(data)
    
    if data["countShips"] == 5 :
        print("Let's start the game.")


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
#1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED :
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED :
        board[row][col] = EMPTY_CLICKED
    if isGameOver(board) :
        data["winner"] = player



'''
runGameTurn(data, row, col)
#1 [Hw6] & #2 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if (data["computer"][row][col] == SHIP_CLICKED) or (data["computer"][row][col] == EMPTY_CLICKED) :
        return
    coor = getComputerGuess(data["user"])
    updateBoard(data, data["computer"], row, col, "user")
    updateBoard(data, data["user"], coor[0], coor[1], "computer")
    data["turns"] += 1
    if data["turns"] == data["maxTurns"] :
        data["winner"] = "draw"


'''
getComputerGuess(board)
#2 [Hw6]
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row = random.randint(0,9)
    col = random.randint(0,9)
    while (board[row][col] == SHIP_CLICKED or board[row][col] == EMPTY_CLICKED) :
        row = random.randint(0,9)
        col = random.randint(0,9)
    return [row, col]


'''
isGameOver(board)
#3 [Hw6]
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in board :
        if SHIP_UNCLICKED in row :
                return False
    return True


'''
drawGameOver(data, canvas)
#3 [Hw6] & #4 [Hw6] & #5 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"] == "computer" :
        canvas.create_text(250, 250, fill = "pink", font = ("Purisa", 50), text = "EASY W!")
        canvas.create_text(250, 300, fill = "pink", font = ("Purisa", 20), text = "Press enter to restart.")

    elif data["winner"] == "draw" :
        canvas.create_text(250, 250, fill = "black", font = ("Purisa", 50), text = "Out of turns!")
        canvas.create_text(250, 300, fill = "pink", font = ("Purisa", 20), text = "Press enter to restart.")
    else :
        canvas.create_text(250, 250, fill = "black", font = ("Purisa", 50), text = "You loose!")
        canvas.create_text(250, 300, fill = "pink", font = ("Purisa", 20), text = "Press enter to restart.")



### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()

    ## Uncomment these for Week 2 ##
    """
    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    """

    ## Uncomment these for Week 3 ##
    """
    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    test.week3Tests()
    """

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
