from tkinter import *
import copy

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.pinsInBoard = [ ]

    #draw board
    data.margin = 10
    data.topMargin = 70
    data.resultMargin = 150
    data.guessHeights = 80


def mousePressed(event, data):
    # use event.x and event.y
    pass
def keyPressed(event, data):
    # use event.char and event.keysym
    pass
def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    drawBoard(canvas, data)
    drawPinsInBoard(canvas, data)
    drawGuessResults(canvas, data)
    if (self.game.gameOver()):
        drawFinalResult(canvas, data)



def drawBoard(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="DarkOrange2", 
        outline="DarkOrange2")
    canvas.create_rectangle(data.margin, data.topMargin, data.width-data.resultMargin, 
        data.height-data.margin, fill="sandy brown", outline="saddle brown")
    canvas.create_rectangle(data.width-data.resultMargin, data.topMargin,
        data.width-data.margin, data.height-data.margin, fill="NavajoWhite2", 
        outline="saddle brown")



def drawPinsInBoard(canvas, data):
    for row in range(8):
        for circle in range(4):
            (x0, y0, x1, y1) = getGuessCoords(data, row, circle)
            try:
                fill = data.pinsInBoard[row][circle]                
            except:
                fill = "black"
            canvas.create_oval(x0, y0, x1, y1, fill=fill)

def getGuessCoords(data, row, circle):
    data.lightMargin = 10
    width = ((data.width-data.resultMargin) - (data.margin)) / 4
    x0 = data.margin + data.lightMargin + (circle*width)
    x1 = x0 + width - (2*data.lightMargin)
    y0 = data.height - data.margin - data.lightMargin - (row*data.guessHeights)
    y1 = y0 - data.guessHeights + (2*data.lightMargin)
    return (x0, y0, x1, y1)



def drawGuessResults(canvas, data):
    for row in range(8):
        fillList = getLightFill(data, row)
        for circle in range(4):
            (x0, y0, x1, y1) = getLightCoords(data, row, circle)
            canvas.create_oval(x0, y0, x1, y1, fill=fillList[circle])

def getLightCoords(data, row, circle):
    width = data.resultMargin - data.margin
    diameter = width/4 - 2*data.margin
    x0 = data.width - data.resultMargin + data.margin + (circle*(width/4))
    x1 = x0 + diameter
    y0 = data.height - data.margin - (row*data.guessHeights) - data.guessHeights/2 - diameter/2
    y1 = y0 + diameter
    return (x0, y0, x1, y1)

def getLightFill(data, row):
    try:
        guessDict = {"red":0, "white":0, "black":0}
        finalResultCopy = copy.copy(self.game.code)
        for circle in range(4):
            if (data.pinsInBoard[row][circle] == finalResultCopy[circle]):
                guessDict["red"] += 1
                finalResultCopy[circle] = None
            elif (data.pinsInBoard[row][circle] in finalResultCopy):
                guessDict["white"] += 1
                index = finalResultCopy.index(data.pinsInBoard[row][circle])
                finalResultCopy[index] = None
            else:
                guessDict["black"] += 1
        returnList = [ ]
        for value in guessDict:
            if (guessDict[value] != 0):
                returnList += [value]*(guessDict[value])
        return returnList
    except:
        return ["gray"] * 4


def drawFinalResult(canvas, data):
    if (self.game.win):
        canvas.create_text(data.width/2, data.topMargin/2, text="YOU WIN!", 
            font="Courier 18")
    else:
        canvas.create_text(data.width/2-data.margin, data.topMargin/2, anchor=E, 
            text="YOU LOSE, RESULT WAS:", font="Courier 18")
        for circle in range(4):
            diameter = data.topMargin - 2*data.margin
            x0 = data.width/2+(circle*(diameter+data.lightMargin))
            y0 = data.margin
            canvas.create_oval(x0, y0, x0+diameter, y0+diameter, fill=self.game.code[circle])




####################################
# use the run function as-is
####################################

def run(width=500, height=720):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()