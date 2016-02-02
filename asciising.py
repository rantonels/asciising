import curses
import random
import math

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()

stdscr.keypad(1)

(H,W) = stdscr.getmaxyx()

W-=1

T = 1.0
B = 0.0

win = curses.newwin(H,W,0,0)

state = [[1 for i in range(H)] for j in range(W)]

chars = {1:"#",-1:" "}

for y in range(H):
    stdscr.addstr(y,0,"#"*(W))

while True:
    K = 1.0/T
    h = B/T

    for it in range(30):
        X = random.randint(0,W-1)
        Y = random.randint(0,H-1)
        deltaS = - 2 * state[X][Y]
        minusdeltabetaH = K * deltaS * (
                state[(X-1)%W][Y] +
                state[X][(Y-1)%H] +
                state[(X+1)%W][Y] +
                state[X][(Y+1)%H] + 
                h)

        acceptance = math.exp( min(0,minusdeltabetaH))

        if (random.uniform(0,1) < acceptance):
            state[X][Y] = - state[X][Y]
            stdscr.addch(Y,X, chars[state[X][Y]] )

    stdscr.addstr(0,0,"T = "+str(T) + ", H = "+str(B))
    
    stdscr.refresh()

    stdscr.nodelay(1)
    chin = stdscr.getch()

    if (chin == ord('q')):
        break

    if (chin == curses.KEY_UP): T += 0.025
    if (chin == curses.KEY_DOWN): T -= 0.025

    if (chin == curses.KEY_LEFT): B -= 0.025
    if (chin == curses.KEY_RIGHT): B += 0.025

    T = max(0.025,T)




curses.nocbreak()
curses.echo()
curses.endwin()
