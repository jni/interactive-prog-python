# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

def initialize_game():
    global secret_number, rangemax, guesses_remaining, guesses_label
    rangemax = 100
    guesses_remaining = 7
    new_game()

# helper function to start and restart the game
def new_game():
    global secret_number, rangemax, guesses_remaining, guesses_label
    secret_number = random.randrange(rangemax)
    if rangemax == 100:
        guesses_remaining = 7
    else:
        guesses_remaining = 10

# define event handlers for control panel
def range100():
    global rangemax
    rangemax = 100
    new_game()
    print 'The secret number is now in [0, 100).'

def range1000():
    global rangemax
    rangemax = 1000
    new_game()
    print 'The secret number is now in [0, 1000).'
    
def input_guess(guess):
    global secret_number, guesses_remaining, guesses_label
    guess = int(guess)
    print 'Your guess was %i' % guess
    guesses_remaining -= 1
    guesses_label.set_text('Guesses remaining: %i' % guesses_remaining)
    if guess < secret_number:
        print '... and it was too low.'
    elif guess > secret_number:
        print '... and it was too high.'
    else:
        print '... and BOOM. You got it.'
    if guesses_remaining == 0:
        print 'You ran out of guesses! Starting a new game.'
        print '(The secret number was %i.)' % secret_number
        new_game()

    
# create frame
initialize_game()
frame = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame
frame.add_input('Enter guess:', input_guess, 50)
frame.add_button('New game in [0, 100)', range100, 100)
frame.add_button('New game in [0, 1000)', range1000, 100)
guesses_label = frame.add_label('Guesses remaining: %i' %
                                guesses_remaining)

# call new_game 
new_game()

frame.start()
