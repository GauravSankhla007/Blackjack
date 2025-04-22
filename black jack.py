import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank["Rank"]} of {self.suit}'


class Deck:
    def __init__(self):
        self.cards = []
        suits = ['spades', 'club', 'heart', 'diamond']
        ranks = [
            {'Rank': 'A', 'Value': 11},
            {'Rank': '1', 'Value': 1},
            {'Rank': '2', 'Value': 2},
            {'Rank': '3', 'Value': 3},
            {'Rank': '4', 'Value': 4},
            {'Rank': '5', 'Value': 5},
            {'Rank': '6', 'Value': 6},
            {'Rank': '7', 'Value': 7},
            {'Rank': '8', 'Value': 8},
            {'Rank': '9', 'Value': 9},
            {'Rank': '10', 'Value': 10},
            {'Rank': 'J', 'Value': 10},
            {'Rank': 'Q', 'Value': 10},
            {'Rank': 'K', 'Value': 10},
        ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        for _ in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            card_value = int(card.rank['Value'])
            self.value += card_value
            if card.rank['Rank'] == 'A':
                has_ace = True
        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_card=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if self.dealer and index == 0 and not show_all_dealer_card and not self.is_blackjack():
                print('Hidden')
            else:
                print(card)
        if not self.dealer:
            print('Value:', self.get_value())
        print()


class Game:
    def play(self):
        game_number = 0
        games_to_play = 0
        while games_to_play <= 0:
            try:
                games_to_play = int(input('How many games you want to play? '))
            except:
                print('You must enter a number.')
        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for _ in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print('*' * 30)
            print(f'Game {game_number} of {games_to_play}')
            print('*' * 30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            # Fixed input loop
            while True:
                if player_hand.get_value() >= 21:
                    break
                choice = input("Choose Hit or Stand (H/S): ").lower()
                while choice not in ['h', 'hit', 's', 'stand']:
                    choice = input("Invalid input. Please enter H (Hit) or S (Stand): ").lower()
                if choice in ['s', 'stand']:
                    break
                player_hand.add_card(deck.deal(1))
                player_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_card=True)

            if self.check_winner(player_hand, dealer_hand):
                continue

            print('Your hand:', player_hand_value)
            print("Dealer's hand:", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, True)

        print('\nThanks for Playing!')


    def check_winner(self, player_hand, dealer_hand, game_over=False):
        player_value = player_hand.get_value()
        dealer_value = dealer_hand.get_value()

        if player_value > 21:
            print('You lose! (Busted)')
            return True
        elif dealer_value > 21:
            print('Dealer busts! You win!')
            return True
        elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
            print('Draw: Both got Blackjack!')
            return True
        elif player_hand.is_blackjack():
            print('Blackjack! You win!')
            return True
        elif dealer_hand.is_blackjack():
            print("Dealer's Blackjack! You lose!")
            return True
        elif game_over:
            if player_value > dealer_value:
                print('You win!')
            elif player_value == dealer_value:
                print('Tie game!')
            else:
                print('You lose!')
            return True
        return False


g = Game()
g.play()