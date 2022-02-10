'''
I'd like you to build an interactive minesweeper game on the command line. 
Here's how I'd like it to work from a user perspective. 
1) It asks the user how many rows there should be in the game
2) It asks the user how many columns there should be in the game
3) It was the user how many mines there should be in the game
4) It prints a visual representation of the board, showing where all the mines are. This is not something that would happen in a real game of minesweeper, but is important for me to be able to check your work.
5) It asks the user where they would like to guess. If they click a mine the game should end and a "You lose" message should be printed. 
If the user clicks a spot next to a mine, it should show an updated board with that location replaced with the number of mines adjacent to that mine. 
Finally, if they click a spot that isn't next to a mine, the all the locations connected to that location that don't have mines on them should be uncovered, with locations next to a mine showing the number of mines adjacent to that location. Then you should show the user the updated board. 
6) when the user uncovers everywhere there isnt' a mine, a "You win" message should be printed.
7) You should ask the user if they want to play again. 
'''
'''
Solution:
In this game the major compnonent are the board and user class
there are land mines as well but they don't have many properties. 
mines will be an attributes in the board class.
the user class will interact and call the functions of the board class.

Board class:
attributes :
1)size 
2)number of mines
3)list of mines - will be a list of tuples with the row and col position of the ship [(row1,col1),(row2,col2)]
4)the board  - will be a m x n list m is the number of rows and n is the number of columns
            -1 -    represents a mine
             0 -    represents an empty spot
            [1-9] - represents the number of mines around a particular spot
We still need to store which cells are visible to the user. 
5)visibility board -  m x n list with True or False values depending on wether a cell is visible to the user
                   - this also keeps track of all the spots uncovered by the user. 

functions :
1)create_board - create board of user defined size
2)create_mines - create mines and randomly place them on the board
3)display_board - display the board
4)win_condition - check if win condition has been met
5)calculate_adjacent - at the start of the game after all mines are placed, for all the spots we calculate the number of mines next to the spot. 
6)find_empty - if the user clicks on an empty spot, uncover all empty spots connected to the clicked spot
7)uncover_spot - sets the visibility of a cell in the board to true
8)check_spot - checks if the clicked spot is empty, mine, or adjacent to a mine.

User class
Attributes

functions
get_size - asks the user to enter the rows and columns 
get_mines - asks the user the number of mines
make_guess - asks the user to make a guess and calls the check_spot function of the board 
display_board - calls the display board function of board
validate_respone - most of the user input are numbers so we can have a common function to validate the users inputs
gameplay - orchestrates the entire gameplay.

Since the user doesn't have any attributes I think it doesn't require a class of it own. 
the functions have been created in the main function itself

*** If we store the users high score, number of games etc. it would make sense to have a user class

'''
from multiprocessing.dummy import Value
import random
class Board:
    def __init__(self,m,n):
        self.no_rows = m
        self.no_cols = n
        self.board = [[0]*n for _ in range(m)] # creating a board with m rows and n columns 
        self.visible = [[False]*n for _ in range(m)]

    def create_mines(self,no_mines):
        mines = []
        for i in range(no_mines):
            row = random.randint(0,self.no_rows-1)
            col = random.randint(0,self.no_cols-1)
            #print("random number {} {}".format(row,col))
            # if the row, col is already present in the list of mines, we generate more random numbers, 
            # till we find a row,col pair which is not already in the list of mines
            while (row,col) in mines:
                #print("random number already in mines")
                row = random.randint(0,self.no_rows-1)
                col = random.randint(0,self.no_cols-1)
                #print("new random number {} {}".format(row,col))
            # mark those spots in the board
            #print("setting {} {} to -1".format(row,col))
            self.board[row][col] = -1
            
            self.visible[row][col] = True
            mines.append((row,col))
        
        self.mines = mines
        print("Mines created")
        print(self.mines)
        
        self.calculate_adjacent()
    
    def display_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.visible[i][j]:
                    if self.board[i][j] == -1:
                        print(" {*} ",end = "")
                    else:
                        print(" [{}] ".format(self.board[i][j]),end = "")
                else:
                    print(" [ ] ",end = "")
                    #print("\t{}\t".format(self.board[i][j]),end = "")
            print("")



    def win_condition(self):
        # since all the mines are already visible
        # the only spots not visible are the empty spots
        # if all the empty spots become visible the game is won
        # so we just need to check if there is any False in the visible array
        # the function returns true if the win condition has been met, else False
        # print(self.visible)
        for i in range(len(self.visible)):
            for j in range(len(self.visible)):
                if self.visible[i][j] == False:
                    return False
        return True
    
    def calculate_adjacent(self):
        # we could iterate through all the cells of the board and for each cell calculate the 
        # number of adjacent mines
        # but that would be time consuming - most of the cells would not have any value
        # we could instead just iterate through the list of mines and add 1 to all adjacent cells
        for mine in self.mines:
            # we iterate from the row above the mine to the row below the mine 
            # and column before the mine to the column after the mine
            #print("mine "+str(mine))
            for r in range(mine[0]-1,mine[0]+2):
                for c in range(mine[1]-1, mine[1]+2):
                    if r == mine[0] and c == mine[1]:
                        continue
                    
                    elif r>=0 and r< self.no_rows and c>=0 and c<self.no_cols and (r,c) not in self.mines:
                        #print("{} {}".format(r,c))
                        self.board[r][c]+=1
                        #self.uncover_spot(r,c)
        print("adjacency calculated")


    def find_empty(self, row, col):
        # we will uncover all empty spots connected to the given spot
        # this seems like breadth first search
        # lets try that 
        # we have a queue, where we add all points that need to be uncovered. 
        # everytime we uncover a spot we also check for all the spots around it which need to be uncovered and add them to the queue
        # we will also need to keep track of all the spots previously visited. 
        # otherwise we'll keep adding spots to the queue and run into an infinite loop
        if self.board[row][col] == 0:
            queue = [(row,col)]
            visited = []
            while len(queue)>0:
                current = queue.pop()
                visited.append(current)

                #if the current spot is empty, uncover the spot
                if self.board[current[0]][current[1]] == 0:
                    self.uncover_spot(current[0],current[1])

                    #then iterate through all spots adjacent to current spot
                    for r in range(current[0]-1,current[0]+2):
                        for c in range(current[1]-1, current[1]+2):
                            # if the adjacent point is not a mine and hasn't already been visited and
                            # if it isn't already in the queue
                            if r>=0 and r< self.no_rows and c>=0 and c<self.no_cols:
                                #print("{} {}".format(r,c))
                                if (r,c) not in visited and (r,c) not in queue:
                                    if self.board[r][c] != -1:
                                        queue.append((r,c))
                elif self.board[current[0]][current[1]] >= 0:
                    self.uncover_spot(current[0],current[1])
                                
                                


    def uncover_spot(self, row, col):
        if not self.visible[row][col]:
            self.visible[row][col] = True

    def check_spot(self,row, col):
        if self.board[row][col] == -1:
            return -1 # game over
        if self.board[row][col] == 0:
            self.find_empty(row,col)
            if self.win_condition():
                return 1
            return 0 
        if self.board[row][col]>0:
            self.uncover_spot(row,col)          
            if self.win_condition():
                return 1
            return 0




def valid_no(string, lower_limit, upper_limit):
    try:
        a = int(string)
        if a>=lower_limit and a<=upper_limit:
            return a
        raise ValueError
    except ValueError as e:
        print("please enter an integer between {} and {} only".format(lower_limit,upper_limit))
        raise e


def get_size():
    r = input("enter number of rows in the board (0-10)")
    c = input("enter number of columns in the board(0-10)")
    row = valid_no(r,0,10)
    col = valid_no(c,0,10)
    return row,col
def get_mines():
    m = input("enter number of mines in the board(0-20)")
    mines = valid_no(m,0,20)
    return mines

play_more = True
while play_more:

    row, col = get_size()
    mines = get_mines()

    a = Board(row,col)

    a.create_mines(mines)
    a.display_board()
    for i in range(row*col):
        r = int(input("enter row guess"))
        c = int(input("enter col"))
        response = a.check_spot(r,c)
        a.display_board()
        if response == -1:
            print("You Lose! Better luck next time!")
            break
        if response == 1:
            print("Yay!You won! Awesome!")
            break
        
    play = input("Do you want to play another game ? [Y/n]")
    if play.lower() == 'y':
        play_more =True
    else:
        play_more = False






