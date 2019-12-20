import random
import time

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11} #Aces can be 11 or 1

playing = True

class Card():

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return("%s of %s"%(self.rank, self.suit))

class Deck():
    
    def __init__(self, suits = suits , ranks = ranks):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                #How to append this? Not a variable?
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def show(self):
        for card in self.deck:
            print(card)

    def deal(self):
        return random.choice(self.deck)

class Chips():

    def __init__(self):
        self.total = 0
        self.bet = 0

    def inc_pot(self):
        self.total += self.bet
    
    def dec_pot(self):
        self.total -= self.bet

class Player():

    def __init__(self):
        self.hand = []
        self.value = 0

    def draw(self, deck):
        self.hand.append(deck.deal())

    def show(self):
        for card in self.hand:
            print (card)

    def score(self, values = values):
        self.point = 0
        self.ace = 0

        for card in self.hand:
                self.point = self.point + values[card.rank]
                if card.rank == 'Ace':
                    self.ace += 1
        #Adjust for Ace
        if self.point > 21 and self.ace == 1:
                self.point -= 10
                self.ace -= 1
        self.value = self.point
        return(self.point)


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How much would you like to bet?"))
            if chips.bet > chips.total:
                print("You have insufficient funds!, try again!!")
                continue
            else:
                break
        except ValueError:
            print("Invalid input!, try again")
            continue

def hit(player, deck):
    player.draw(deck)

def hit_or_stand(player, deck):
    global playing
    while True:
        try:
            player_input = input("Would you like to hit or stand?")
            
            if player_input[0].lower() == "h":
                hit(player, deck)
                if player.score() > 21:
                    playing = False
            elif player_input[0].lower() == "s":
                print("Dealer is playing, player stands.")
                playing = False
            else:
                print("invalid choice, try again!")
                continue
            break

        except:
            print("Invalid option!, try again ")


def show_some(player,dealer, values = values):
    print("Dealers Hand")
    print("%s"%dealer.hand[0])
    print("<Hidden Card>")
    print(values[dealer.hand[0].rank])
    print()
    print("Player Cards")
    player.show()
    print(player.score())

def show_all(player,dealer):
    dealer.show()
    print(dealer.score())
    print()
    player.show()
    print(player.score())
    
def player_busts(player_chips):
    print ("Player Busts!")
    player_chips.dec_pot()

def player_wins(player_chips):
    print ("Player Wins!")
    player_chips.inc_pot()

def dealer_busts(player_chips):
    print ("Dealer Busts!")
    player_chips.inc_pot()
    
def dealer_wins(player_chip):
    print ("Dealer Wins!")
    player_chips.dec_pot()
    
def push(player_chips):
    print ("It is a tie!")
    player_chips.bet = 0


####GAMEPLAY####

player = Player()
banker = Player()
deck = Deck()
replay = True
    
print("Welcome to a game of BlackJack!")

player_chips = Chips()
while True:
    try:
        player_chips.total = int(input("How much would you like to buy in? "))
        break
    except ValueError:
        print ("Invalid input, please enter numbers only")
        continue

while True:

    #Place Bet
    take_bet(player_chips)

    #Deal starting hand
    deck.shuffle()
    player.draw(deck)
    player.draw(deck)
    banker.draw(deck)
    banker.draw(deck)
    #Show starting cards
    show_some(player, banker)

    #Gameplay
    playing = True
    while playing:
        
        if player.score() == 21:
            print("BLACKJACK!")
            player_wins(player_chips)
            print(player_chips.total)
            print("Chips remaning %s"%(player_chips.total))
            break

        else:
            hit_or_stand(player, deck)
            player.show()
            print(player.score())
            continue

    #DEALER TURN
    if player.score() < 21:
        
        while banker.score() < 17:
            hit(banker, deck)    

    #show all cards
    print("Dealer turn ends")
    print()
    print("All Cards: ")
    show_all(player,banker)

    #Win Conditions
    #Player > Dealer , player win

    if banker.score() > 21:
        player_wins(player_chips)
    elif player.score() > 21:
        player_busts(player_chips)
    elif player.value > banker.value:
        player_wins(player_chips)
    #Player < Dealer , Dealer win
    elif player.value < banker.value:
        player_busts(player_chips)
    #Draw
    else:
        push(player_chips)


    print ("Chips total: %s"%player_chips.total)

    if player_chips.total <= 0:
        print("You are out of chips! GAME OVER!")
        break

    #newgame
    newgame = input("Would you like to play again?")
    if newgame[0].lower() == 'y':
        playing = True
        player.hand = []
        banker.hand = []
        continue
    else:
        break

print ("Thanks for playing!")

