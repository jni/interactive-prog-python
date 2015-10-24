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

# draw subsequent cards with this offset
CARD_OFFSET = (24, 0)

# initialize some useful global variables
deck = None
dealer = None
player = None
in_play = False
outcome = 'Hit or stand?'
score = 0
canvas = None
frame = None

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
        x, y = pos
        x_off, y_off = CARD_OFFSET
        for i, card in enumerate(self.cards):
            card_pos = x + i * x_off, y + i * y_off
            card.draw(canvas, card_pos)



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
    dealer.add_card(deck.deal_card())
    player = Hand()
    player.set_name('Player')
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())

    print dealer
    print player

    outcome = 'Hit or stand?'
    in_play = True


def hit():
    global outcome, in_play, score
    global deck, player
    if in_play:
        player.add_card(deck.deal_card())
    if player.get_value() >= BUST:
        in_play = False
        outcome = 'You have busted! Deal again?'
        print outcome
        score -= 1


def stand():
    global in_play, outcome, score
    global player, dealer, deck
    if not in_play:
        outcome = ("That's like resting your case after the final verdict.\n"
                   "Deal again?")
        print outcome
        return
    while dealer.get_value() < DEALER_STAND:
        dealer.add_card(deck.deal_card())
    if dealer.get_value() < player.get_value():
        outcome = 'You win! Deal again?'
        score += 1
    elif dealer.get_value() >= BUST:
        outcome = 'Dealer busts! Deal again?'
        score += 1  # ?
    else:
        outcome = 'Dealer wins! Deal again?'
        score -= 1
    print outcome
    in_play = False


def hand_position(hand):
    '''Find x-position of first card so hand is centered.'''
    ncards = len(hand.cards)
    pos = round(300.0 - ncards * CARD_OFFSET[0] / 2)
    return pos


def draw_title(canvas):
    global frame
    title = 'Blackjack!'
    w = frame.get_canvas_textwidth(title, 36, 'serif')
    canvas.draw_text(title, (600 - w, 583), 36, 'Black', 'serif')
    canvas.draw_text(title, (600 - w - 3, 580), 36, 'Red', 'serif')


def draw_message(canvas):
    global frame, outcome
    w = frame.get_canvas_textwidth(outcome, 24, 'sans-serif')
    canvas.draw_text(outcome,
                     (300 - w // 2 + 10, 300),
                     24, 'Navy', 'sans-serif')


def draw_score(canvas):
    global frame, score
    score_str = 'Score %i' % score
    w = frame.get_canvas_textwidth(score_str, 24, 'sans-serif')
    canvas.draw_text(score_str, (600 - w, 24), 24, 'Navy', 'sans-serif')

# draw handler    
def draw(canvas):
    # draw players
    global dealer, player
    dealer_x = hand_position(dealer)
    dealer.draw(canvas, [dealer_x, 52])
    player_x = hand_position(player)
    player.draw(canvas, [player_x, 448])

    draw_title(canvas)
    draw_message(canvas)
    draw_score(canvas)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
