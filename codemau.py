import sys
def enterPlayerMove(previousMoves):		
# Let the player enter their move. Return a two-item list of int xy coordinates.		
   print('Where do you want to drop the next sonar device? (0-59 0-14) (or type quit)')		
   while True:		
        move = input()		
        if move.lower() == 'quit':		
            print('Thanks for playing!')		
            sys.exit()		

        move = move.split()		
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit():		
            if [int(move[0]), int(move[1])] in previousMoves:		
                print('You already moved there.')		
                continue		
            return [int(move[0]), int(move[1])]		

previousMoves = []
def main():
    x, y = enterPlayerMove(previousMoves)