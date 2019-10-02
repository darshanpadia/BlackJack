from random import shuffle

class Card:
	def __init__(self, value, suit, amount):
		self.suit = suit
		self.value = value
		self.amount = amount

	def __repr__(self):
		return f"{self.value}{self.suit}"

class Deck:
	
	cards = []

	def __init__(self, n_decks):
		self.n_decks = n_decks
		suits = ['\u2665', '\u2666', '\u2660', '\u2663'] # heart # diamond # spade # club
		values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
		amount = [1,2,3,4,5,6,7,8,9,10,10,10,10]
		for i in range(n_decks):
			for suit in suits:
				for j in range(13):
					self.cards.append(Card(values[j], suit, amount[j]))
	

	def __repr__(self):
		return f"The deck has {len(self.cards)} cards"

	def _deal(self, num):
		if self.cards:
			temp = min(num,self.count())
			removed_cards = []
			i = 1
			while i<=temp:
				removed_cards.append(self.cards.pop())
				i += 1
			return removed_cards
		else:
			raise ValueError("All cards have been dealt")	

	def shuffle(self):
		if len(self.cards) != self.n_decks*52:
			raise ValueError("Only full decks can be shuffled")
		shuffle(self.cards)

	def count(self):
		return len(self.cards)

	def deal_card(self):
		return self._deal(1)[0]

	def deal_hand(self, hand_size):
		return self._deal(hand_size)

class Player:
	def __init__(self):
		self.buy_in = 3000
		self.balance = self.buy_in
		self.bet = 0
		self.cards = []
		self.total = 0
		self.biggest_win = 0
		self.total_winning = 0
		self.hands_played = 0
	def reset(self):
		self.cards = []
		self.total = 0
	def hit(self, deck):
		self.cards.append(deck.deal_card())
		self._calc()
	def _calc(self):
		temp1 = 0
		temp2 = 0
		for i in self.cards:
			if i.amount == 1:
				temp1 += i.amount
				temp2 += 11
			else:
				temp1 += i.amount
				temp2 += i.amount
		if temp2 > 21:
			self.total = temp1
		else:
			self.total = temp2
	def set_bet(self, b_amount):
		if b_amount > (self.bet + self.balance):
			print("You don't have that much balance!")
		elif b_amount <= 0:
			print("Please bet at least 1")
		else:
			self.balance += self.bet
			self.balance -= b_amount
			self.bet = b_amount
	def win(self):
			self.balance += self.bet
			if (self.bet*2) > self.biggest_win:
				self.biggest_win = (self.bet*2)
			self.total_winning += (self.bet*2)
			self.hands_played += 1
			hand_reset()
	def lose(self):
			self.balance -= self.bet
			self.hands_played += 1
			if self.balance < 0:
				game_reset()
				hand_reset()
			else:
				hand_reset()






class Dealer:
	def __init__(self):
		self.cards = []
		self.total = 0
	def hit(self, deck):
		self.cards.append(deck.deal_card())
		self._calc()
	def reset(self):
		self.cards = []
		self.total = 0
	def _calc(self):
		temp1 = 0
		temp2 = 0
		for i in self.cards:
			if i.amount == 1:
				temp1 += i.amount
				temp2 += 11
			else:
				temp1 += i.amount
				temp2 += i.amount
		if temp1 > 21:
			self.total = temp2
		else:
			self.total = temp1


def hand_reset():
	global std
	global deck1
	std = False
	p1.reset()
	d1.reset()
	if len(deck1.cards) < 8:
		deck1 = Deck(4)
	p1.hit(deck1)
	p1.hit(deck1)
	d1.hit(deck1)
	d1.hit(deck1)


def game_reset():
	print(f"Biggest Win:{p1.biggest_win}\nTotal Winnings:{p1.total_winning}\nHands Played:{p1.hands_played}")
	p1.biggest_win = 0
	p1.total_winning = 0
	p1.hands_played = 0
	p1.bet = 0
	p1.balance = p1.buy_in
	p1.set_bet(500)




def stand():
	global std
	std = True
	while d1.total < 17:
		d1.hit(deck1)
	display()
	if d1.total > 21 or p1.total > d1.total:
		if p1.total == 21:
			print("\u2665 \u2666 BLACK JACK \u2660 \u2663 YOU WIN!")
			p1.win()
		else:
			print("YOU WIN!")
			p1.win()
	elif d1.total > p1.total:
		p1.lose()
		print("DEALER WINS!")
	else:
		print("PUSH")
	hand_reset()
	input()

def display():
	global std
	print("-----"*10)
	if std:
		p_cards = ' '.join([f'{x.value}{x.suit}' for x in p1.cards])
		d_cards = ' '.join([f'{x.value}{x.suit}' for x in d1.cards])
		print("\nDealer({0:2}) {1:8} \n\nPlayer({2:2}) {3:8}\n".format(d1.total,d_cards,p1.total,p_cards))
	else:
		p_cards = ' '.join([f'{x.value}{x.suit}' for x in p1.cards])
		d_cards = f'{d1.cards[0].value}{d1.cards[0].suit}'
		print("\nDealer({0:2}) {1:8} \n\nPlayer({2:2}) {3:8}\n".format(d1.cards[0].amount,d_cards,p1.total,p_cards))
	print("-----"*10)
	print(f"Bet   : {p1.bet:4} Balane: {p1.balance:4}")
	print("-----"*10)
	print("\nHit:'H' Stand:'S' ChangeBet:'B' Quit:'Q'")






p1 = Player()
p1.set_bet(500)
deck1 = Deck(4)
deck1.shuffle()
d1 = Dealer()
p1.hit(deck1)
p1.hit(deck1)
d1.hit(deck1)
d1.hit(deck1)
key = ""
std = False
while key!='Q':
	if p1.total > 21:
		display()
		print("BUST!, YOU LOSE!")
		p1.lose()
		input()
	elif p1.total == 21:
		stand()
	display()
	
	key = (input()).upper()
	if key == 'H':
		p1.hit(deck1)
	elif key == 'S':
		stand()
	elif key == 'B':
		p1.set_bet(int(input("Enter amount: ")))





