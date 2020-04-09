import copy
import random
from tkinter import *

class node:
    def __init__(self, state):
        self.state = state
        self.best = None

def st_print(state):
    print("*****************")
    print(is_finished(state))
    for row in state:
        print(row)
    print("*****************")

def is_finished(state):
    for row in state:
        if ( (row[0] == row[1]) and (row[1] == row[2]) ) and (row[2] == row[3]):
            if row[0] == "x":
                return 1
            elif row[0] == "o":
                return -1

    for i in range(4):
        if (state[0][i] == state[1][i]) and (state[1][i] == state[2][i]) and (state[2][i] == state[3][i]):
            if state[0][i] == "x":
                return 1
            elif state[0][i] == "o":
                return -1

    if (state[0][0] == state[1][1]) and (state[1][1] == state[2][2]) and (state[2][2] == state[3][3]):
        if state[0][0] == "x":
            return 1
        elif state[0][0] == "o":
            return -1

    if (state[0][3] == state[1][2]) and (state[1][2] == state[2][1]) and (state[2][1] == state[3][0]):
        if state[0][3] == "x":
            return 1
        elif state[0][3] == "o":
            return -1

    for row in state:
        for elem in row:
            if elem == "-":
                return -2
    return 0


def next_states(state):
    turn = get_turn(state)
    new_states = []
    for j in range(4):
        for i in range(4):
            if state[j][i] == "-":
                temp_state = copy.deepcopy(state)
                temp_state[j][i] = turn
                new_states.append(node(temp_state))

    random.shuffle(new_states)
    return new_states

def get_turn (state):
    x_count = 0
    o_count = 0

    for row in state:
        for elem in row:
            if elem == "x":
                x_count += 1
            elif elem == "o":
                o_count += 1

    turn = ""
    if x_count > o_count:
        turn = "o"
    else:
        turn = "x"

    return turn

# alpha beta pruning to make the best move.
def alpha_beta_pruning(x, alpha, beta):
    state = x.state
    if is_finished(state) != -2:
        return is_finished(state)

    if get_turn(state) == "x" :
        maxValue = - 10
        possible_states = next_states(state)
        for itr in possible_states:
            value = alpha_beta_pruning(itr, alpha, beta)
            if value > maxValue:
                maxValue = value
                x.best = itr
            alpha = max(maxValue, alpha)
            if beta <= alpha:
                break
        return maxValue
    else:
        minValue =  10
        possible_states = next_states(state)
        for itr in possible_states:
            value = alpha_beta_pruning(itr, alpha, beta)
            if value < minValue:
                minValue = value
                x.best = itr
            beta = min(minValue, beta)
            if beta <= alpha:
                break
        return minValue


tie   = [["-","-","-","-"],["-","-","-","-"],["-","-","-","-"],["-","-","-","-"]]
tie_root = node(tie)
x_win = [["x","x","-","-"],["x","-","-","-"],["o","-","o","-"],["-","o","-","-"]]
x_win_root = node(x_win)
o_win = [["x","-","-","-"],["-","-","-","-"],["x","-","o","-"],["-","o","-","-"]]
o_win_root = node(o_win)

'''print("Tie Condition(Calculating..) : ")
print(alpha_beta_pruning(tie_root,-10,10))
print()
'''
print("X Win Condition (Calculating..) : ")
print(alpha_beta_pruning(x_win_root,-10,10))
print()
print("O Win Condition: (Calculating..) : ")
print(alpha_beta_pruning(o_win_root,-10,10))
print()


tie_list = []
while tie_root != None:
    tie_list.append(tie_root)
    tie_root = tie_root.best

x_win_list = []
while x_win_root != None:
    x_win_list.append(x_win_root)
    x_win_root = x_win_root.best

o_win_list = []
while o_win_root != None:
    o_win_list.append(o_win_root)
    o_win_root = o_win_root.best

master = Tk()
master.title("ArcticFoxes")
w = Canvas(master, width=1500, height=1000, bg="white")

def show_on_canvas (list, y):
    count =  0
    for l in list:

        offset_x = 150*count + 15
        offset_y = 50 * y
        line_space = 30
        line_length = 120

        '''w.create_text(offset_x + 10 , offset_y - 10  , font="Times 20", text="X" , fill="blue")
        w.create_text(offset_x + 20 + 10 , offset_y  - 10  , font="Times 20", text="O" , fill="red")'''

        w.create_line(offset_x, offset_y + line_space*0, offset_x + line_length, offset_y + line_space*0 )
        w.create_line(offset_x, offset_y + line_space*1, offset_x + line_length, offset_y + line_space*1 )
        w.create_line(offset_x, offset_y + line_space*2, offset_x + line_length, offset_y + line_space*2 )

        offset_x = 150*count + 45
        offset_y = offset_y - 30

        w.create_line(offset_x + line_space*0, offset_y , offset_x + line_space*0, offset_y + line_length )
        w.create_line(offset_x + line_space*1, offset_y , offset_x + line_space*1, offset_y + line_length )
        w.create_line(offset_x + line_space*2, offset_y , offset_x + line_space*2, offset_y + line_length )

        offset_x = 150*count + 15
        offset_y = offset_y + 30

        for i in range (4):
            for j in range(4):
                if (l.state[i][j] == 'x'):
                    w.create_text(offset_x + line_space*j + 15, offset_y + line_space*i - 15, font="Times 18", text="X", fill="blue")
                    #print("x")
                elif(l.state[i][j]== 'o'):
                    w.create_text(offset_x + line_space*j + 15, offset_y + line_space*i - 15, font="Times 18", text="O", fill="red")
                    #print("o")
        count = count + 1

show_on_canvas(tie_list,1)
show_on_canvas(x_win_list,4)
show_on_canvas(o_win_list,7)

scrollbar = Scrollbar(master,orient='horizontal')
scrollbar.config(command=w.xview)
scrollbar.pack(side=BOTTOM, fill=X)

w.pack()
master.mainloop()