from random import sample
from time import sleep
class Card:
	def __init__(self,value,suit,points):
		self.value = value
		self.suit = suit
		self.points = points
	def __repr__(self):
		return("{}{}".format(self.value,self.suit))
class Deck:
	def __init__(self,deck_count):
		self.cards = []
		for count in range(1,deck_count+1):
			suit =['\u2665', '\u2666', '\u2660', '\u2663']
			value = ["2", "3", "5", "4", "6", "7", "8", "9", "10", "J", "Q","K", "A"]
			for i in value:
				for j in suit:
					if i == 'A':
						wor = 11
					elif i in 'KQJ':
						wor = 10
					else:
						wor = int(i)
					card = Card(value = i, suit = j,points= wor)
					self.cards.append(card)
		self.cards = sample(self.cards, len(self.cards))
	def count(self):
		return len(self.cards)
	def deal(self):
		count = self.count() 
		if count == 0:
			raise ValueError("All cards have been dealt")
		card = self.cards.pop()
		return card
class Player():
	def __init__(self,name,buy_in):
		self.name = name
		self.hand = []
		self.split_hand = []
		self.total = 0
		self.balance = buy_in
		self.hands_played = 0
		self.total_winning = 0
		self.max_win = 0
		self.bet = 0
		self.first = True
	def reset(self):
		self.hand = []
		self.total = 0
		self.BlackJack = False
	def hit(self,deck):
		self.hand.append(deck.deal())
		self._calc() 
	def _calc(self):
		self.total = 0
		ace_count = 0
		for card in self.hand:
			if card.value == "A":
				ace_count += 1
			self.total += card.points
		while self.total > 21 and ace_count != 0:
			self.total -= 10
			ace_count -= 1
	def set_bet(self,amount):
		if amount == 'pgksj':
			amount = input("Enter your bet: ")
		while amount.isdigit() != True:
			amount = input("Enter a numeric value: ")
		amount = int(amount)
		if amount > self.balance:
			amount = input("Not enough balance! ")
			return self.set_bet(amount)
		elif amount < 1:
			amount = input("You need to place a bet: ")
			return self.set_bet(amount)
		self.bet = amount
		self.balance -= self.bet
	def win(self):
		if self.total ==21 and len(self.hand) == 2:
			winning = self.bet*2.5
		else:
			winning = self.bet*2
		if winning > self.max_win:
			self.max_win = winning
		self.balance += winning
		self.total_winning += self.bet
		self.hands_played += 1
		print(f"You Won! ${self.bet*2} Balance: ${self.balance}")
		hand_reset()
	def draw(self):
		self.balance += self.bet
		self.hands_played += 1
		print(f"PUSH! Balance: ${self.balance}")
		hand_reset()
	def lose(self):
		self.total_winning -= self.bet
		self.hands_played += 1
		print(f"Dealer Wins! You lost ${self.bet} Balance: ${self.balance}")
		if self.balance < 1:
			sleep(2)
			game_reset()
			hand_reset()
		else:
			hand_reset()
	def double(self):
		if self.balance < self.bet:
			print("Can't Double! Insufficiant Balance!")
			sleep(2)
		else:
			self.balance -= self.bet
			self.bet *= 2
			self.hit(deck)
			if self.total > 21:
				std = True
				display()
				print("BUST!")
				self.lose()
			else:
				stand()
	def insurance(self):
		insure = ''
		while insure not in ['y','n']:
			insure = input("Do you want to insure your bet? ").lower()
		if insure == "y":
			if self.balance < int(self.bet//2):
				print("Cant Insure! Insufficiant Balance!")
			else:
				if dealer.total == 21:
					self.balance += self.bet
					print(f"Insurance returns your bet {self.bet}! Balance: {self.balance}")
					self.total_winning += self.bet
					sleep(2)
					stand()
				else:
					self.balance -= int(self.bet//2)
					print(f"Lost ${int(self.bet//2)} insurance! Balance: {self.balance}")
					self.total_winning -= int(self.bet//2)
					sleep(2)
		if insure == 'n':
			if dealer.total == 21:
				stand()
		self.first = False




		


class Dealer():
	def __init__(self):
		self.hand = []
		self.total = 0
		self.BlackJack = False
		self.Bust = False
	def hit(self,deck):
		self.hand.append(deck.deal())
		self._calc() 
	def _calc(self):
		self.total = 0
		ace_count = 0
		for card in self.hand:
			if card.value == "A":
				ace_count += 1
			self.total += card.points
		while (self.total < 17 or self.total >21) and ace_count != 0:
			self.total -= 10
			ace_count -= 1
	def reset(self):
		self.hand = []
		self.total = 0
		self.BlackJack = False


def stand():
	display()
	global std
	global bet
	std = True
	p1_blackjack = False
	dealer_blackjack = False
	sleep(2)
	display()
	if p1.total == 21 and len(p1.hand) == 2:
		p1_blackjack = True
		print("BlackJack!")
	if (dealer.total == 21 and len(dealer.hand) ==2):
		print("Dealer BlackJack!")
		dealer_blackjack = True

	if p1_blackjack == True and dealer_blackjack == True:
		print(f"BlackJack PUSH!")
		return p1.draw()
	elif p1_blackjack:
		return p1.win()
	elif dealer_blackjack:
		return p1.lose()
	while dealer.total < 17:
		sleep(2)
		dealer.hit(deck)
		display()
	if dealer.total > 21 or p1.total>dealer.total:
		if dealer.total > 21:
			print(f"Dealer Bust!")
			return p1.win()		
		return p1.win()
	elif dealer.total > p1.total:
		p1.lose()
	else:
		p1.draw()


def display():
	print("-----"*10)
	if std:
		p_cards = ' '.join([f'{x.value}{x.suit}' for x in p1.hand])
		d_cards = ' '.join([f'{x.value}{x.suit}' for x in dealer.hand])
		print("\nDealer({0:2}) {1:8} \n\nPlayer({2:2}) {3:8}\n".format(dealer.total,d_cards,p1.total,p_cards))
	else:
		p_cards = ' '.join([f'{x.value}{x.suit}' for x in p1.hand])
		d_cards = f'{dealer.hand[0].value}{dealer.hand[0].suit}'
		print("\nDealer({0:2}) {1:8} \n\nPlayer({2:2}) {3:8}\n".format(dealer.hand[0].points,d_cards,p1.total,p_cards))
	print("-----"*10)
	print(f"Bet   : {p1.bet:4} Balance: {p1.balance:4}")
	print("-----"*10)
	if len(p1.hand) == 2:
		print("\nHit:'H' Stand:'S' Double:'D' Quit:'Q'")
	else:
		print("\nHit:'H' Stand:'S' Quit:'Q'")

def hand_reset():
	global std
	global deck
	global bet
	std = False
	p1.reset()
	dealer.reset()
	if len(deck.cards) < 8:
		deck = Deck(4)
	bet = 'pgksj'
	initial_game()

def game_reset():
	if p1.total_winning > -1:
		print(f"\n\nBiggest Win:{p1.max_win}\nTotal Winnings:{p1.total_winning}\nHands Played:{p1.hands_played}")
	else:
		print(f"\n\nBiggest Win:{p1.max_win}\nTotal Losings:{abs(p1.total_winning)}\nHands Played:{p1.hands_played}")
	p1.max_win = 0
	p1.total_winning = 0
	p1.hands_played = 0
	p1.bet = 0
	p1.balance = 3000

def initial_game():
	p1.set_bet(bet)
	p1.hit(deck)
	dealer.hit(deck)
	p1.hit(deck)
	dealer.hit(deck)
	display()
	if dealer.hand[0].points == 10:
		print("                peak ")
		sleep(2)
		if dealer.total == 21:
			print("Dealer BlackJack!")
			stand()
	if dealer.hand[0].value == 'A':
		p1.insurance()


p1 = Player('Darsh', 3000)
deck = Deck(4)
dealer = Dealer()
std = False
bet = 'pgksj'
initial_game()
key = ""
while key!='Q':
	if p1.total > 21:
		std = True
		display()
		print("BUST!")
		p1.lose()
	elif p1.total == 21:
		stand()
	display()
	key = (input()).upper()
	if key == 'H':
		p1.hit(deck)
	elif key == 'S':
		stand()
	elif key =='D' and len(p1.hand) == 2:
		p1.double()
		
