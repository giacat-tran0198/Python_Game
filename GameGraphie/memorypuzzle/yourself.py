#tự làm

import random, pygame, sys
from pygame.locals import *

#the variable
FPS = 30
Width = 640
Height = 480
RevealSpeed = 8 #tốc độ mở hình ảnh
BoxSize = 40 
GapSize = 10 #khoảng cánh
BoardWidth = 10 #số cột của icon
BoardHeight = 7 #số hàng của icon
assert(BoardWidth * BoardHeight) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.' #biểu thức true nếu không chương trình dừng lại
XMargin = int(Width - (BoardWidth * (BoxSize + GapSize)) / 2) #xđ điểm ảnh bên cạnh viền bản
YMargin = int(Height - (BoardHeight * (BoxSize + GapSize)) / 2)

#Color       R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

#set variables constant
DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamond"
LINES = "lines"
OVAL = "oval"

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BoardHeight * BoardWidth, "Board is too bigg for the number of shapes/colors defined." #đảm bảo đủ màu sắc và hình dạng trong kích thước bài

def main():
    global FPSCLOCK, DISPLAYSURF #biến toàn cục
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((Width, Height))
    mouse_x = mouse_y = 0 #vị trí con trỏ
    pygame.display.set_caption("Memory Game")

    #trả về list 2D. 
    mainBoard = getRandomizedBoard() #trả về giá trị structure của khu vực chơi
    revealedBoxes = generateRevealedBoxesData(False) #trả về dữ liệu structure mà box che giấu tương ứng

    #animation of game
    firstSelection = None #vị trí (x,y) của lần click chuột đầu tiên

    #vẽ màn hình trò chơi lúc đầu
    DISPLAYSURF.fill(BGCOLOR) 
    startGameAnimation(mainBoard) #tạo hiệu ứng chuyển động mở ra đóng vào

    while True: #main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) #vẽ màn hình trò chơi để xóa bất kì cái gì vẽ trước đây
        drawBoard(mainBoard, revealedBoxes) #vẽ trạng thái hiện tại của mainBoard và các box đã hiện lên
        
        for event in pygame.event.get(): #vòng lặp sự kiện, khác với vòng lặp trò chơi
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE): #KEYUP = phím Esc
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION: #sử lý sự kiện con chuột di chuyển
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP: #sử lý sự kiện con chuột di chuyển và nhấn click
                mouse_x, mouse_y = event.pos
                mouseClicked = True
                
                #kiểm tra con hộp được con trỏ được click
                box_x, box_y = getBoxAtPixel(mouse_x, mouse_y)
                if box_x != None and box_y != None:
                    if not revealedBoxes[box_x][box_y]: #kiểm tra xem box đấy có được con trỏ che chưa, false nếu box đã bj che
                        drawHighlightBox(box_x, box_y) #vẽ viền xanh lên để biết box có thể mở ra
                    if not revealedBoxes[box_x][box_y] and mouseClicked: #kiểm tra box đấy con trỏ che chưa và đã được click chưa
                        revealBoxesAnimation(mainBoard, [(box_x, box_y)]) #hành động lật box
                        revealedBoxes[box_x][box_y] = True #đặt giá trị box đã mở, để ko bị che lại lập tức

                        #xử lý box được click đầu tiên
                        if firstSelection == None: #true nếu đã được click
                            firstSelection = (box_x, box_y) #giữ tọa độ box đã click
                        else: #nếu đây là box 2 -> kiểm tra xem có khớp ko vs box 1
                            icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                            icon2shape, icon2color = getShapeAndColor(mainBoard, box_x, box_y)

                        #xử lý cặp biểu tuownjg không khớp
                        if icon1shape != icon2shape or icon1color != icon2color:
                            pygame.time.wait(1000) #1000 ms = 1s
                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1], (box_x, box_y))])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[box_x][box_y] = False
                        #sử lý nếu đung
                        elif hasWon(revealedBoxes): #kiểm tra nếu toàn bộ được tìm
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)

                            #reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)

                            #show the fully unrevealed board for a second
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            #repaly the start game animation
                            strartGameAnimation(mainBoard)
                        firstSelection = None #reset 
        #Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#tạo ra list of list boolean
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BoardWidth):
        revealedBoxes.append([val] * BoardHeight) #đảm bảo giá trị cột dọc chứ không phải hàng ngang
    return revealedBoxes

#tạo dữ liệu cho bảng
def getRandomizedBoard():
    
    #bước 1: tạo các icon
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    
    #bước 2: xáo trọn và loại bỏ danh sách các icon
    random.shuffle(icons) #xáo trộn thứu tự icon
    numIconUsed = int(BoardWidth * BoardHeight / 2) #tính số lượng icon cần
    icons = icons[:numIconUsed] * 2 #tạo 2 icon giống nhau
    random.shuffle(icons)

    #bước 3: sắp xếp icon vào board
    board = []
    for x in range(BoardWidth):
        column = []
        for y in range(BoardHeight):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

#chia danh sách được gọi bởi hàm startGameAnimation
def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

#hệ thống tọa độ
def leftTopCoordOfBox(box_x, box_y):
    left = box_x * (BoxSize * GapSize) * XMargin
    top = box_y * (BoxSize * GapSize) * YMargin
    return (left, top)
    
#chuyển tọa con trỏ thành tọa độ của hộp
def getBoxAtPixel(x, y):
    for box_x in range(BoardWidth):
        for box_y in range(BoardHeight):
            left, top = leftTopCoordOfBox(box_x, box_y)
            boxRect = pygame.Rect(left, top, BoxSize, BoxSize)
            if boxRect.collidepoint(x, y):
                return (box_x, box_y)
    return (None, None)

#vẽ biểu tượng
def drawIcon(shape, color, box_x, box_y):
    quarter = int(BoxSize * 0.25)
    half = int(BoxSize * 0.5)
    
    left, top = leftTopCoordOfBox(box_x, box_y)
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BoxSize - half, BoxSize - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BoxSize - 1, top + half), (left + half, top + BoxSize - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BoxSize, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BoxSize - 1), (left + BoxSize - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BoxSize, half))

def getShapeAndColor(board, box_x, box_y):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[box_x][box_y][0], board[box_x][box_y][1]

#vẽ box đang đóng
def drawBoxCovers(board, boxes, coverage):
    #vẽ box đóng, mở, "boxes": là danh sách của cả 2 cặp items, bao gôm x,y của box
    #tạo vòng lặp để vẽ:
    # 1. vẽ nền
    # 2. vẽ icon
    # 3. vẽ box trắng
    for box in boxes:
        left, top = leftTopCoordOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BoxSize, BoxSize))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: #chỉ vẽ box đóng nếu nó là coverage, nếu ít hơn 0 thì không cần vẽ, giảm gọi hàm draw.rect
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BoxSize))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#xử lý hành động lập và đóng
def revealBoxesAnimation(board, boxesToReveal):
    #hành động mở
    for coverage in range(BoxSize, (-RevealSpeed) - 1, -RevealSpeed):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    #hành động đóng
    for coverage in range(0, BoxSize + RevealSpeed, RevealSpeed):
        drawBoxCovers(board, boxesToCover, coverage)

#vẽ toàn bộ board
def drawBoard(board, revealed):
    #vẽ tất cả các box đang bị che hoặc mở
    for box_x in range(BoardWidth):
        for box_y in range(BoardHeight):
            left, top = leftTopCoordOfBox(box_x, box_y)
            if not revealed[box_x][box_y]:
                #vẽ box đóng
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BoxSize, BoxSize))
            else:
                #vẽ box mở
                shape, color = getShapeAndColor(board, box_x, box_y)
                drawIcon(shape, color, box_x, box_y)

#vẽ viền xanh để giúp người chơi nhận ra box đang đóng
def drawHighlightBox(box_x, box_y):
    left, top = leftTopCoordOfBox(box_x, box_y)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BoxSize + 10, BoxSize + 10), 4) #độ dày 4px

#hành động mở box ban đầu
def startGameAnimation(board):
    #ngẫu nhiên mở 8 box cùng lúc
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BoardWidth):
        for y in range(BoardHeight):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

#thắng cuộc
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == "__main__":
    main()