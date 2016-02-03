import curses
import math
import numpy as np

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()

stdscr.keypad(1)

(H,W) = stdscr.getmaxyx()

W-=1

T = 2.5
B = 0.0

win = curses.newwin(H,W,0,0)

state = -1+2*np.random.randint(2,size=(H,W))#[[1 for i in range(H)] for j in range(W)]

chars = {1:"#",-1:" "}

for y in range(H):
    stdscr.addstr(y,0,"#"*(W))

while True:
    K = 1.0/T
    h = B/T

    for it in range(4):# range(30):
        #X = random.randint(0,W-1)
        #Y = random.randint(0,H-1)
        deltaS = - 2 * state#[X][Y]
        minusdeltabetaH = K * deltaS * (
                np.roll(state,-1,1) +
                np.roll(state,+1,1) +
                np.roll(state,-1,0) +
                np.roll(state,+1,0) +
                h)

        acceptance = np.exp( np.minimum(np.zeros((H,W)),minusdeltabetaH))

        random_mask = np.random.randint(2,size=(H,W))

        mask = np.greater(acceptance,np.random.sample((H,W))) * random_mask

        #if (random.uniform(0,1) < acceptance):
        #    state[X][Y] = - state[X][Y]
        #    stdscr.addch(Y,X, chars[state[X][Y]] )

        state = (1-2*mask)*state

    for j in range(H):
        stdscr.addstr(j,0,"".join([chars[state[j,i]] for i in range(W)]) )

    stdscr.addstr(0,0,"T = %.3f"%T + ", H = %.3f"%B)
    
    stdscr.refresh()

    stdscr.nodelay(1)
    chin = stdscr.getch()

    if (chin == ord('q')):
        break

    if (chin == curses.KEY_UP): T += 0.025
    if (chin == curses.KEY_DOWN): T -= 0.025

    if (chin == curses.KEY_LEFT): B -= 0.1
    if (chin == curses.KEY_RIGHT): B += 0.1

    T = max(0.025,T)


    if (chin == curses.KEY_RESIZE):
        H, W = stdscr.getmaxyx()
        H-=1
        W-=1
        #curses.resizeterm(H,W)
        oldstate = list(state)
        state = -1 + 2*np.random.randint(2,size=(H,W))
        stdscr.refresh()
        



curses.nocbreak()
curses.echo()
curses.endwin()
