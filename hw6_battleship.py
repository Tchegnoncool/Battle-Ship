from tkinter import *
import random


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    # Ships state
    data['EMPTY_UNCLICKED'] = 1
    data['SHIP_UNCLICKED'] = 2
    data['EMPTY_CLICKED'] = 3
    data['SHIP_CLICKED'] = 4
    # Board Dimentions
    data["rows"] = 10
    data["cols"] = 10
    data["boardSize"] = 500
    data["cellSize"] = 50
    # Game guidelines
    data["numShips"] = 5
    data["user"] = emptyGrid(data)
    data["computer"] = addShips(emptyGrid(data), data["numShips"], data['EMPTY_UNCLICKED'], data['SHIP_UNCLICKED'])
    data["tempShip"] = []
    data["countShips"] = 0
    data["winner"] = None
    data["turns"] = 0
    data["maxTurns"] = 123567890987654
    data["restart"] = False
 

'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    emtGrid = emptyGrid(data)
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
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return" and data["winner"] != None:
        data["restart"] = True


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; str
Returns: None
'''
def mousePressed(data, event, board):
    coor = getClickedCell(data, event)
    if board == "user" :
        clickUserBoard(data, coor[0], coor[1])
    if board == "comp" and data["countShips"] == 5 and data["winner"] == None:
        runGameTurn(data, coor[0], coor[1])


'''
emptyGrid(data)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(data):
    grid = []
    for row in range (data['rows']) :
        temp = []
        for col in range (data['cols']) :
            temp.append(data['EMPTY_UNCLICKED'])
        grid.append(temp)
    return grid


'''
createShip()
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
checkShip(grid, ship, emptyUncliked)
Parameters: 2D list of ints ; 2D list of ints; int
Returns: bool
'''
def checkShip(grid, ship, emptyUncliked):
    for row in range (len(ship)) :
        storeR = ship[row][0]
        storeC = ship[row][1]
        if grid[storeR][storeC] != emptyUncliked:
            return False
    return True


'''
addShips(grid, numShips, emptyUncliked, shipUnclicked)
Parameters: 2D list of ints ; int; int; int
Returns: 2D list of ints
'''
def addShips(grid, ships, emptyUncliked, shipUnclicked):
    while (ships > 0) :
        newShip = createShip()
        if(checkShip(grid, newShip, emptyUncliked)) :
            for row in range (len(newShip)) :
                storeR = newShip[row][0]
                storeC = newShip[row][1]
                grid[storeR][storeC] = shipUnclicked
            ships -= 1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''

def drawGrid(data, canvas, grid, showShips):
    x = data["cellSize"]
    for row in range (data["rows"]) :
        for col in range (data["cols"]) :
            if grid[row][col] == data['SHIP_UNCLICKED'] and showShips :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "yellow")
            elif grid[row][col] == data['SHIP_CLICKED'] :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "red")
            elif grid[row][col] == data['EMPTY_CLICKED'] :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "white")
            else :
                canvas.create_rectangle((col * x), (row * x), (col * x) + x, (row * x) + x, fill = "blue")


'''
isVertical(ship)
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
shipIsValid(grid, ship, emptyUncliked)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship, emptyUncliked):
    if len(ship) == 3 and checkShip(grid, ship, emptyUncliked) and (isVertical(ship) or isHorizontal(ship)) :
        return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    emptyUncliked = data['EMPTY_UNCLICKED']
    if shipIsValid(data["user"], data["tempShip"], emptyUncliked) :
        for curr in range (len(data["tempShip"])) :
            currZero = data["tempShip"][curr][0]
            currOne = data["tempShip"][curr][1]
            data["user"][currZero][currOne] = data['SHIP_UNCLICKED']
        data["countShips"] += 1
    else :
        print("Sorry you can't do that. Try another ship.")
    data["tempShip"] =[]


'''
clickUserBoard(data, row, col)
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


'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == data['SHIP_UNCLICKED'] :
        board[row][col] = data['SHIP_CLICKED']
    elif board[row][col] == data['EMPTY_UNCLICKED'] :
        board[row][col] = data['EMPTY_CLICKED']
    if isGameOver(board, data['SHIP_UNCLICKED']) :
        data["winner"] = player


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if (data["computer"][row][col] == data['SHIP_CLICKED']) or (data["computer"][row][col] == data['EMPTY_CLICKED']) :
        return
    coor = getComputerGuess(data["user"], data['SHIP_CLICKED'], data['EMPTY_CLICKED'])
    updateBoard(data, data["computer"], row, col, "user")
    updateBoard(data, data["user"], coor[0], coor[1], "computer")
    data["turns"] += 1
    if data["turns"] == data["maxTurns"] :
        #print('tie')
        data["winner"] = "draw"


'''
getComputerGuess(board, shipClicked, emptyClicked)
Parameters: 2D list of ints; int; int
Returns: list of ints
'''
def getComputerGuess(board, shipClicked, emptyClicked):
    row = random.randint(0,9)
    col = random.randint(0,9)
    while (board[row][col] == emptyClicked or board[row][col] == emptyClicked):
        row = random.randint(0,9)
        col = random.randint(0,9)
    return [row, col]


'''
isGameOver(board, shipUnclicked)
Parameters: 2D list of ints; int
Returns: bool
'''
def isGameOver(board, shipUnclicked):
    for row in board:
        if shipUnclicked in row:
            return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"] == "user" :
        canvas.create_text(250, 250, fill = "pink", font = ("Purisa", 50), text = "EASY W!")
        canvas.create_text(250, 300, fill = "pink", font = ("Purisa", 20), text = "Press enter to restart.")

    elif data["winner"] == "draw" :
        canvas.create_text(250, 250, fill = "black", font = ("Purisa", 50), text = "Out of turns!")
        canvas.create_text(250, 300, fill = "pink", font = ("Purisa", 20), text = "Press enter to restart.")
    else :
        canvas.create_text(250, 250, fill = "black", font = ("Purisa", 50), text = "You loose!")
        canvas.create_text(250, 300, fill = "pink", font = ("Purisa", 20), text = "Press enter to restart.")


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


def main():
    runSimulation(500, 500)
main()
