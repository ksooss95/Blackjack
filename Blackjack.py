"""
Ben Poliquin

Blackjack GUI with Tk
"""
from CardLabel import *
from Deck import *
from Card import *
import tkinter as tk
from tkinter.messagebox import showinfo
import sys
import os

def restart_program():
	python = sys.executable
	os.execl(python, python, * sys.argv)

class Blackjack(BlackjackCard):
		
	def __init__(self):
		self.root = tk.Tk()
		self.root.wm_title("BlackJack Game")
		
		self.deal = Button(master = self.root, text='Deal', command = self.deal)
		self.deal.grid(row=2, column=0, pady=10, columnspan=2)
		
		self.hit = Button(master = self.root, text='Hit', command = self.hit)
		self.hit.grid(row=2, column=2, pady=10, columnspan=2)
		
		self.cpass = Button(master = self.root, text='Pass', command = self.cpass)
		self.cpass.grid(row=2, column=4, pady=10, columnspan=2)

		CardLabel.load_images()	
		self._dealercard = [CardLabel(self.root) for i in range(6)]
		self._playercard = [CardLabel(self.root) for i in range(6)]
		
		dealerpos = 0
		for x in self._dealercard:
			x.grid(row=0, column=dealerpos)
			x.display(side='blank') 
			dealerpos += 1
			
		playerpos = 0
		for y in self._playercard:
			y.grid(row=1, column=playerpos)
			y.display(side='blank')
			playerpos += 1
		self.root.mainloop()
	
	def deal(self):     
		self.hit.configure(state = 'normal') 
		self.cpass.configure(state = 'normal')

		self.deck = Deck()
		self.deck.shuffle()
		self.dealer = self.deck.deal(2)
		self.player = self.deck.deal(2)
		
		self._dealercard[0].display('front', self.dealer[0]._id)
		self._dealercard[1].display('back', self.dealer[1]._id)
		
		self._playercard[0].display('front', self.player[0]._id)
		self._playercard[1].display('front', self.player[1]._id)
			
	counter = 1 
	def hit(self):
	   
		Blackjack.total(self)
		if self.player_points > 21:
			showinfo("Game Over", "Dealer Wins!")
			Blackjack.ended(self)
	
		if len(self.player) < 6: 
			self.player += self.deck.deal(1)
			self._playercard[Blackjack.counter+1].display('front', self.player[Blackjack.counter+1]._id)
			Blackjack.counter += 1
		else:
			self.hit.configure(state = 'disabled')
			
	dealercounter = 1
	def cpass(self):
		Blackjack.total(self)
		self._dealercard[1].display('front', self.dealer[1]._id)
		while self.dealer_points < 17:
			self.dealer += self.deck.deal(1)
			self._dealercard[Blackjack.dealercounter+1].display('front', self.dealer[Blackjack.dealercounter+1]._id)
			Blackjack.dealercounter += 1
			Blackjack.total(self)
		if self.dealer_points > self.player_points and self.dealer_points <= 21 or self.player_points > 21:
			showinfo('Game Over', "Dealer Wins!")
		elif self.dealer_points < self.player_points or self.dealer_points > 21:
			showinfo("Game Over", "Player 1 Wins!")
		else:
			showinfo("Game Over", "Its a Tie!")
		Blackjack.ended(self)

	def ended(self):
		self.cpass.configure(state = 'disable')
		self.hit.configure(state = 'disable')
		restart_program()      
		
	def total(self):
		self.player_points = 0 
		aces = 0
		for x in self.player:
			self.player_points += BlackjackCard(x._id).points()
			if BlackjackCard(x._id).rank() == 12:
				aces += 1
		while self.player_points > 21 and aces > 0:
			self.player_points -= 10
			aces -= 1
			
		self.dealer_points = 0
		aces = 0
		for y in self.dealer:
			self.dealer_points += BlackjackCard(y._id).points()
			if BlackjackCard(y._id).rank() == 12:
				aces += 1
		while self.dealer_points > 21 and aces > 0:
			self.player_points -= 10
			aces -= 1

if __name__ == "__main__":
	Blackjack()        