#sf
import pygame, sys, random
from pygame.locals import *

boardWidth = 4 #số cột
boardHeight = 4 #số hàng
tileSize = 80
windowWidth = 640
windowHeight = 480
FPS = 30
blank = None

black = (0, , 0, 0)
white = (255, 255, 255)
brightBlue = (0, 50, 255)
darkTurquoise = (3, 54, 73)
green = (0, 204, 0)

BGcolor = darkTurquoise
tileColor = green
textColor = white
bordercolor = brightBlue
basicFontSize = 20

butonColor = white
butonTextColor = black
messageColor = white

XMargin = int((windowWidth - (tileSize * boardWidth + (boardWidth - 1))) / 2)
YMargin = int((windowHeight - (tileSize * boardHeight + (boardHeight - 1))) / 2)

Up = "up"
Down = "down"
Left = "left"
Right = "right"

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Slide Puzzle")
    BASICFONT = pygame.font.Font("freesansbold.ttf", basicFontSize)
    

#kết thúc chương trình
def terminate():
    pygame.quit()
    sys.exit()

#kiểm tra sự kiện đặc biệt và gọi hàm đợi, check quit
def checkForQuit():
    for event in pygame.event.get(QUIT): #kiểm tra toàn bộ các sự kiện Quit
        terminate()
    for event in pygame.event.get(KEYUP): #kiểm tra sự kiện keyup
        if event.key == K_ESCAPE:
            terminate() #quit nếu key là Esc key
        pygame.event.post(event) #trả lại các keyup về lại

#tạo cấu trúc dữ liệu 
def getStartingBoard():
    #trả về cấu trúc dữ liệu vs các ô trạng thái đã giải quyết
    #ex: nếu boardwidth = boardheight = 3, trả về [[1,4,7],[2,5,8],[3,6,None]]
    counter = 1
    board = []
    for x in range(boardWidth):
        column = []
        for y in range(boardHeight):
            column.append(counter)
            counter += boardWidth
        board.append(column)
        counter -= boardWidth * (boardHeight - 1) + boardWidth - 1
    board[boardWidth - 1][boardHeight - 1] = None
    return board

#tìm khoảng trống, nhưng không theo dõi vị trí mà kiểm tra toàn bộ bảng
def getBlankPosition(board):
    for x in range(boardWidth):
        for y in range(boardHeight):
            if board[x][y] == None:
                return (x, y)

#thực hiện di chuyển bằng cách cập nhật dữ liệu trong data structure
def makeMove(board, move):
    #this function does not check if the move is valide
    blankx, blanky = getBlankPosition(board)
    if move == Up:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == Down:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == Left:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == Right:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

#kiểm tra di chuyển hợp lệ ko
def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == Up and blanky != len(board[0]) - 1) or (move == Down and blanky != 0) or (move == Left and blankx != len(board) - 1) or (move == Right and blankx != 0)

#tạo bảng ngẫu nhiên để di chuyển
def getRandomMove(board, lastMove=None):
    validMoves = [Up, Down, Left, Right]
    if lastMove == Up or not isValidMove(board, Down):
        validMoves.remove(Down)
    if lastMove == Down or not isValidMove(board, Up):
        validMoves.remove(Up)
    if lastMove == Left or not isValidMove(board, Right):
        validMoves.remove(Right)
    if lastMove == Right or not isValidMove(board, Left):
        validMoves.remove(Left)
    return random.choice(validMoves)

#chuyển đổi tọa độ gốc thành tọa độ pixel
def getLeftTopOfTile(tileX, tileY):
    left = XMargin + (tileX * tileSize) + (tileX - 1)
    top = YMargin + (tileY * tileSize) + (tileY - 1)
    return (left, top)
#chuyển đổi tọa độ pixle thành tọa độ board
def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, tileSize, tileSize)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

#vẽ 1 ô
def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    #vẽ 1 ô ở tọa độ tilex và tiley, tùy từng điểm
    #trên pixel-xác định bởi tilex, tiley
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, tileColor, (left + adjx, top + adjy, tileSize, tileSize))
    textSurf = BASICFONT.render(str(number), True, textColor)
    textRect = textSurf.get_rect() #cho đối tượng surf được định vị
    textRect.center = left + int(tileSize / 2) + adjx, top + int(tileSize / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect) #để surface hiển thị

#tạo văn bản xuất hiện trên màn hình
def makeText(text, color, bgcolor, top, left):
    #tạo vật surface và rect cho 1 số văn bản
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

#vẽ bảng
def drawBoard(board, message):
    DISPLAYSURF.fill(BGcolor)
    if message:
        textSurf, textRect = makeText(message, messageColor, bgcolor, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])
    #vẽ viền
    left, top = getLeftTopOfTile(0, 0)
    width = boardWidth * tileSize
    height = boardHeight * tileSize
    pygame.draw.rect(DISPLAYSURF, bordercolor, (left - 5, top - 5, width + 11, height + 11), 4) #độ dày 4
    #vẽ nút
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

#hoạt động của tile
def slideAnimation(board, direction, message, animationSpeed):
    #không kiểm tra bước đi có hiệu lực
    blankx, blanky = getBlankPosition(board)
    if direction == Up:
        movex = blankx
        movey = blanky + 1
    elif direction == Down:
        movex = blankx
        movey = blanky - 1
    elif direction == Left:
        movex = blankx + 1
        movey = blanky
    elif direction == Right:
        movex = blanky - 1
        movey = blanky
    
    #copy() surface method
    #prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    #vẽ khoảng trắn di chuyển
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGcolor, (moveLeft, moveTop, tileSize, tileSize))
    for i range(0, tileSize, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == Up:
            drawTile(movex, moveyy, board[movex][movex], 0, -i)
        if direction == Down:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == Left:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == Right:
            drawTile(movex, movey, board[movex][movey], i, 0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#creating new puzzle
def generateNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle....', int(tileSize / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)
def resetAnimation(board, allMoves):
    #make all of the moves in allMoves in reverse
    revAllMoves = allMoves[:] #gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == Up:
            oppositeMove = Down
        elif move == Down:
            oppositeMove = Up
        elif move == Left:
            oppositeMove = Right
        elif move == Right:
            oppositeMove = Left
        slideAnimation(board, oppositeMove, '', int(tileSize / 2))
        makeMove(board, oppositeMove)
if __name__ == "__main__":
    main()