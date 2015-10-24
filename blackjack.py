# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
deck = None
dealer = None
player = None
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# other constants
BUST = 22
DEALER_STAND = 17

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        card_pos = (pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1])
        canvas.draw_image(card_images,
                          card_loc, CARD_SIZE, # position in card_images
                          card_pos, CARD_SIZE)  # position on canvas


def is_ace(card):
    return card.rank == 'A'


# define hand class
class Hand:
    def __init__(self):
        self.hole_card = None
        self.cards = []
        self.name = ''

    def __str__(self):
        return (self.name + ':' +
                '[' + ', '.join(map(str, self.cards)) + ']')

    def add_card(self, card):
        self.cards.append(card)
        print 'Card added to', self

    def get_value(self):
        base_value = sum([VALUES[card.rank] for card in self.cards])
        has_ace = len(filter(is_ace, self.cards)) > 0
        if has_ace and base_value + 10 < BUST:
            total_value = base_value + 10
        else:
            total_value = base_value
        return total_value

    def set_name(self, name):
        self.name = name

    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards



# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        return '/'.join(map(str, self.cards))


#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck
    global dealer, player

    deck = Deck()
    deck.shuffle()

    dealer = Hand()
    dealer.set_name('Dealer')
    dealer.add_card(deck.deal_card())
    player = Hand()
    player.set_name('Player')
    player.add_card(deck.deal_card())

    print dealer
    print player

    outcome = ''
    in_play = True


def hit():
    global outcome, in_play, score
    global deck, player
    if in_play:
        player.add_card(deck.deal_card())
    if player.get_value() > BUST:
        in_play = False
        outcome = 'You have busted!'
        print outcome
        score -= 1


def stand():
    global in_play, outcome, score
    global player, dealer, deck
    if not in_play:
        print "Erm, that's like resting your case after the verdict."
        return
    while dealer.get_value() < DEALER_STAND:
        dealer.add_card(deck.deal_card())
    if dealer.get_value() < player.get_value():
        outcome = 'You win!'
        score += 1
    elif dealer.get_value() >= BUST:
        outcome = 'Dealer busts!'
        score += 1  # ?
    else:
        outcome = 'Dealer wins!'
        score -= 1
    print outcome
    in_play = False

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
