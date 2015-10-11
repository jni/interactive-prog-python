# implementation of card game - Memory

import simplegui
import random

NUM_PAIRS = 8
CARD_WIDTH = 50  # in pixels
TEXT_SIZE = 64  # in points

# helper function to initialize globals
def new_game():
    # global variables to hold game state
    global cards, exposed, state, current, turns,\
           lastcard, label, tohide
    score = 0
    turns = 0
    cards = range(NUM_PAIRS) + range(NUM_PAIRS)
    random.shuffle(cards)
    exposed = [False] * NUM_PAIRS * 2
    state = 0
    lastcard = (-1, -1)
    label.set_text('Turns = %i' % turns)
    tohide = []


# define event handlers
def mouseclick(pos):
    global cards, exposed, state, current, turns,\
           lastcard, label, tohide
    index = pos[0] // CARD_WIDTH
    if not exposed[index]:
        print 'clicked on card number', index
        exposed[index] = True
        # hide unmatched cards from previous turn, if any
        for h in tohide:
            exposed[h] = False
        # and reset the list
        tohide = []
    else:
        print 'click IGNORED on card number', index
        return
    currentcard = (index, cards[index])
    if state == 1:  #  step number in current turn
        state = 0
        turns += 1
        label.set_text('Turns = %i' % turns)
        if lastcard[1] == currentcard[1]:
            # the cards match and we are awesome
            lastcard = (-1, -1)
        else:
            # Oops, they didn't match
            # Hide at start of next turn
            tohide = [lastcard[0], currentcard[0]]
    else:
        state = 1
        lastcard = currentcard


# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards, exposed
    for i, (exp, val) in enumerate(zip(exposed, cards)):
        # Rectangle to be drawn. Coordinates are in pixels,
        # (width, height), and origin is at top-left
        lower_left = i * CARD_WIDTH, 100
        upper_left = i * CARD_WIDTH, 0
        upper_right = (i + 1) * CARD_WIDTH, 0
        lower_right = (i + 1) * CARD_WIDTH, 100
        rectangle = [lower_left, upper_left,
                     upper_right, lower_right]
        if exp:
            canvas.draw_polygon(rectangle, 2,
                                'Gray', 'White')
            lower_left_offset = (lower_left[0] + 7,
                                 lower_left[1] - 25)
            canvas.draw_text(str(val), lower_left_offset,
                             TEXT_SIZE, 'Blue', 'monospace')
        else:
            canvas.draw_polygon(rectangle, 1,
                                'Black', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
