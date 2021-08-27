import random
import os #to clear termial
import time #time to slow down when dealer draws a card
import common #is a common file I created for common code that I might use in other projects
import platform #to work with os if different OS is used

DEBUG = False #Debug mode to test things

#Creating a lists of card names and suits to combine it later
name = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
#Creating a Playing cards class
class PlayingCard():
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
	def get_value(self): #Calculating a value of cards
		if self.rank in ['Jack', 'Queen', 'King']:
			return 10
		elif self.rank == 'Ace':
			return 11
		else:
			return int(self.rank)
	def get_card(self): #Returnig a card name to print it out later
		return self.rank + ' of ' + self.suit


class Hand(): #Creating a hand class for Player and Dealer
	def __init__(self, name):
		self.cards = []
		self.value = 0
		self.name = name #'Player or Dealer'
	def display_hand(self, hidden = True):
		print(f'{self.name}:')
		if self.name == 'Dealer': #Creating a statment when to hide or show dealer cards
			if hidden == False: #Here I am showing all cards that dealer has and draws
				for card in self.cards:
					print(card.get_card())
			else: #Here dealers first card is hidden
				print('Hidden!')
				print(self.cards[1].get_card())	
		else: #Players hand is shown all the time
			for card in self.cards:
				print(card.get_card())

	def calculate_value(self): #Calculating the value of cards and handling Ace value 11 or 1 
		self.value = 0	   #depending on hand
		numAces = 0 
		for card in self.cards:	
			if card.rank == "Ace":
				numAces += 1
			self.value += card.get_value()
		while self.value > 21 and numAces >= 1:
			self.value -= 10
			numAces -= 1
		
def draw_cards(hand, num_cards = 1, specific = DEBUG):
	for draw in range(num_cards):
		if specific == True:#If debug is == True, this statmen will promt to draw a card
				name = input('What card do you want? ')
				hand.cards.append(PlayingCard(name, "Hearts"))
		else:
				hand.cards.append(deck.pop(0))
		
	hand.calculate_value()	
			
def make_deck():#Creating a deck
	deck = []
	for n in name:
		for s in suits:
			c = PlayingCard(n, s)
			deck.append(c)
	return deck

def clear(): 
	'''
	This code was written on Linux system and so I wanted to add some things to clear 
	a board so it has nice look. In case different system is used, I've added if statments.
	'''
	if platform.system() == 'Windows':
		os.system('cls')
	elif platform.system() == 'Linux':
		os.system('clear')
	elif platform.system == "Darwin":
		os.system('clear')

def draw_board(hide = True):#Clearing and drawing board so the game is on the top of the termial
	clear()
	player.display_hand()
	print()
	dealer.display_hand(hide)
	print()

#Created a list of decisions for player. This could be done easier way, but I wanted to have some fun
player_draw = ['hit', 'yes', 'y', 'h', 'for sure', 'i take one more', 'for sure!', 'I take one more!', 'busts!', 'busts', 'bust', 'busted!']
player_stand = ['stand', 's', 'no', 'n', 'pass', 'no!', 'i am good', 'im good', "i'm good"]
player_double = ['double', 'i feel lucky today', 'd']
combined_list = player_draw + player_stand + player_double

player_money = 1000

game = True

while game: #Actual game loop
	player_game = True
	dealer_game = True
	player = Hand('Player')
	dealer = Hand('Dealer')
	deck = make_deck()
	random.shuffle(deck)
	print(f'Your budget is ${player_money}!')
	a_bet = common.get_integer('Place your bet: ', 'Incorrect input. Try again!', 'Bet needs to be an integer')
	#^^^ Here I am assigning a_bet to my common 
	print()
	if a_bet > player_money or a_bet < 0:
		print("You don't have that amount of money, plese place correct amount!")
		continue
	player_money -= a_bet
	draw_cards(player, 2)
	draw_cards(dealer, 2)

	draw_board()
	#If first 2 cards got value 21 it is instant Black Jack, draw if both player and dealer got 21
	if player.value == 21:
		player_game = False
		dealer_game = False
	if dealer.value == 21:
		player_game = False
		dealer_game = False
	while player_game:	#In this loop player decides what to do. Hit, Stand or Double
		draw_aCard = input('Do you want to Hit, Stand or Double?: ')	
		draw_board()
		if draw_aCard.lower() not in combined_list:
			print('Incorrect input! Please, try again!')
			print()
			continue
		if draw_aCard.lower() in player_double:
			if a_bet > player_money:
				print('You can not double, you do not have enough money!') 
				continue
			player_money -= a_bet
			a_bet = a_bet * 2		
			print(f"Your bet now is ${a_bet}!")
			draw_cards(player)
			draw_board()
			if player.value > 21:#If player gor more than 21, player busts!
				pass
			break
		if draw_aCard.lower() in player_draw:
			draw_cards(player)
			draw_board()
			if player.value > 21:
				break
			print()
		else:
			print()
			break

	draw_board(False)

	#if dealer has less than 17 points he draws the card
	while dealer_game:
		while dealer.value < 17 and player.value < 22: 
			draw_cards(dealer)
			#each time dealer draws the card animation will be slowed down to see what is going on
			time.sleep(1)
			draw_board(False)
		break


	#Deciding who wins in this match
	if player_game == False and player.value > dealer.value:
		print('Player got Black Jack! Player wins!')
		player_money += a_bet * 2.5
	elif dealer_game == False and player.value < dealer.value:
		print('Dealer got Black Jack! Dealer wins!')
	elif player.value > dealer.value and player.value < 22:
		print(f'Player got {player.value} points and dealer got {dealer.value} points. Player WINS!')
		player_money += a_bet * 2
	elif dealer.value > player.value and dealer.value < 22 or player.value > 21:
		print(f'Player got {player.value} points and dealer got {dealer.value} points. Dealer WINS!')
	elif dealer.value == player.value:
		print(f'Player: {player.value}. Dealer {dealer.value}. Draw!')
		player_money += a_bet
	else:
		print(f'Dealer: {dealer.value}. Player: {player.value}. Player WINS!')
		player_money += a_bet * 2
	print()	

	if player_money == 0:#If player out of money, he is kicked out!
		print('You are flat out broke! You need to leave!')
		break

	while True:#Asking player does he want to continue
		player_decision = input('Do you want to continue? Y/N: ')
		clear()
		if player_decision.lower() not in combined_list:
			print('Incorrect input, try again!')
		else:
			break
	
	if player_decision.lower() not in player_draw:
		game = False
	clear()
	



		

















'''
def draw_specific_card():
	
	sdeck = []
	s = 'Hearts'
	for n in name:
		d = PlayingCard(n, s)
		#print(d.get_card())
		sdeck.append(d)
	draw_sCard = input('What card do you want? ')
	if draw_sCard in ['Jack', 'Queen', 'King']:
		return sdeck[9]
	elif draw_sCard == 'Ace':
		return sdeck[0]
	else:
		return sdeck[int(draw_sCard) - 1]
	
	name = input('What card do you want? ')
	hand.cards.append(PlayingCard(name, "Hearts"))
	hand.calculate_value()

''
print('Player:')
player = 0
for p1 in player_cards:
	print(p1.card())
	player += p1.get_value()
print()

print('Dealer:')
dealer = 0
for d1 in dealer_cards:
	print(d1.card())
	dealer += d1.get_value()
print()

if player > dealer:
	print(f'Player got {player} points and dealer got {dealer} points. Player WINS!')
elif dealer > player:
	print(f'Player got {player} points and dealer got {dealer} points. Dealer WINS!')
else:
	print('Draw')
'''


'''
for d in deck:
	print(d.card())
'''

#card1 = PlayingCard(name[3], suits[0])
#card2 = PlayingCard(name[12], suits[2])

#print(f'{card1.card()} and {card2.card()}')
























