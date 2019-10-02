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
		self.total = 0
		self.balance = buy_in
		self.hands_played = 0
		self.max_win = 0
		self.bet = 0
		self.BlackJack = False
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
		while amount > self.balance:
			amount = int(input("Not enough balance! "))
		while amount < 1:
			amount = int(input("You need to place a bet: "))
		self.bet = amount
		self.balance -= self.bet
	def win(self):
		winning = self.bet*2
		if winning > self.max_win:
			self.max_win = winning
		self.balance += winning
		self.hands_played += 1
	def draw(self):
		self.balance += self.bet
		self.hands_played += 1
	def lose(self):
		self.hands_played += 1
	def blackjack(self):
		if self.total == 21 and len(self.cards) == 2:
			self.BlackJack = True
	
		




class Dealer():
	def __init__(self):
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
		while (self.total < 17 or self.total >21) and ace_count != 0:
			self.total -= 10
			ace_count -= 1
	def reset(self):
		self.hand = []
		self.total = 0
		self.BlackJack = False
	def peak(self):
		if self.cards[0] > 9:
			if self.total == 21 and len(self.cards) == 2:
				self.BlackJack = True


def compare():
	if p1.total < dealer.total:
		display()
		print("You Lose!")
		return p1.lose()
	elif p1.total > dealer.total:
		display()
		print("You Win!")
		p1.win()
	else:
		display()
		print("Draw!")
		p1.draw()

def passive_game():
	bet = int(input("Place your bet: "))
	p1.set_bet(bet)
	p1.hit(deck)
	dealer.hit(deck)
	p1.hit(deck)
	dealer.hit(deck)
	display()
	if p1.total == 21:
		print("BlackJack")
		if dealer.total != 21:
			display()
			return p1.win()


	display()
	if dealer.hand[0].points > 9:
		print("Peak")
		if dealer.total == 21:
			sleep(2)
			if p1.total == 21:
				print("BlackJack Draw!")
				return p1.draw()
			print(dealer.hand,dealer.total)
			print("Dealer BlackJack! You Lose")
			return p1.lose()
	active_game()


def active_game():
	inp = ''
	while p1.total <21 and inp != 's':
		inp = input("hit/stand? ").lower()
		if inp == 'h':
			p1.hit(deck)	
			display()
			if p1.total > 21:
				print(f'Bust! You Lose!')
				return p1.lose()
	std = True
	display()
	while dealer.total < 17:
		sleep(2)
		dealer.hit(deck)
		display()
	if dealer.total > 21:
		display()
		print('Dealer Bust! You Win!')
		return p1.win()
	compare()

def display():
	print("-----"*10)
	if std:
		p_cards = ' '.join([f'{x.value}{x.suit}' for x in p1.hand])
		d_cards = ' '.join([f'{x.value}{x.suit}' for x in dealer.hand])
		print("\nDealer({0:2}) {1:8} \n\nPlayer({2:2}) {3:8}\n".format(d1.total,d_cards,p1.total,p_cards))
	else:
		p_cards = ' '.join([f'{x.value}{x.suit}' for x in p1.hand])
		d_cards = f'{dealer.hand[0].value}{dealer.hand[0].suit}'
		print("\nDealer({0:2}) {1:8} \n\nPlayer({2:2}) {3:8}\n".format(dealer.hand[0].points,d_cards,p1.total,p_cards))
	print("-----"*10)
	print(f"Bet   : {p1.bet:4} Balane: {p1.balance:4}")
	print("-----"*10)
	print("\nHit:'H' Stand:'S' ChangeBet:'B' Quit:'N'")




deck = Deck(4)
p1 = Player('Darsh',3000)
dealer = Dealer()
quit = ''
std = False	
while quit not in ['n','no']:
	p1.reset()
	dealer.reset()
	std = False
	passive_game()
	print(p1.balance)
	quit = input("Next Round?(y/n) ").lower()
print(f"\nhands played : {p1.hands_played} \nmaximum win: {p1.max_win} \nBalance: {p1.balance}")









		
