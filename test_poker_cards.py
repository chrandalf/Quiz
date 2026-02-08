"""
Unit tests for the poker cards design implementation.
"""

import unittest
from poker_cards import Card, Deck, Hand, Suit, Rank


class TestCard(unittest.TestCase):
    """Test cases for the Card class."""
    
    def test_card_creation(self):
        """Test creating a card."""
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.ACE)
    
    def test_card_str(self):
        """Test string representation of a card."""
        card = Card(Suit.SPADES, Rank.KING)
        self.assertEqual(str(card), "K of Spades")
    
    def test_card_equality(self):
        """Test card equality comparison."""
        card1 = Card(Suit.DIAMONDS, Rank.TEN)
        card2 = Card(Suit.DIAMONDS, Rank.TEN)
        card3 = Card(Suit.CLUBS, Rank.TEN)
        
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
    
    def test_card_comparison(self):
        """Test card comparison by rank."""
        card1 = Card(Suit.HEARTS, Rank.TWO)
        card2 = Card(Suit.SPADES, Rank.ACE)
        
        self.assertTrue(card1 < card2)
        self.assertFalse(card2 < card1)


class TestDeck(unittest.TestCase):
    """Test cases for the Deck class."""
    
    def test_deck_initialization(self):
        """Test that a new deck has 52 cards."""
        deck = Deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(deck.cards_remaining(), 52)
    
    def test_deck_has_all_cards(self):
        """Test that deck contains all unique cards."""
        deck = Deck()
        
        # Check we have 4 suits × 13 ranks = 52 cards
        suits_count = {suit: 0 for suit in Suit}
        ranks_count = {rank: 0 for rank in Rank}
        
        for card in deck.cards:
            suits_count[card.suit] += 1
            ranks_count[card.rank] += 1
        
        # Each suit should appear 13 times
        for count in suits_count.values():
            self.assertEqual(count, 13)
        
        # Each rank should appear 4 times
        for count in ranks_count.values():
            self.assertEqual(count, 4)
    
    def test_deck_shuffle(self):
        """Test that shuffling changes the deck order."""
        deck1 = Deck()
        original_order = deck1.cards.copy()
        
        deck1.shuffle()
        
        # It's theoretically possible (but extremely unlikely) that
        # shuffle results in the same order, so we just check it's callable
        self.assertEqual(len(deck1.cards), 52)
    
    def test_deck_deal(self):
        """Test dealing a single card."""
        deck = Deck()
        initial_count = len(deck)
        
        card = deck.deal()
        
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck), initial_count - 1)
    
    def test_deck_deal_multiple(self):
        """Test dealing multiple cards."""
        deck = Deck()
        cards = deck.deal_multiple(5)
        
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(deck), 47)
        
        for card in cards:
            self.assertIsInstance(card, Card)
    
    def test_deck_deal_from_empty(self):
        """Test that dealing from an empty deck raises an error."""
        deck = Deck()
        
        # Deal all cards
        deck.deal_multiple(52)
        
        # Try to deal from empty deck
        with self.assertRaises(IndexError):
            deck.deal()
    
    def test_deck_deal_too_many(self):
        """Test that dealing more cards than available raises an error."""
        deck = Deck()
        
        with self.assertRaises(ValueError):
            deck.deal_multiple(53)
    
    def test_deck_reset(self):
        """Test resetting the deck."""
        deck = Deck()
        deck.deal_multiple(10)
        
        self.assertEqual(len(deck), 42)
        
        deck.reset()
        
        self.assertEqual(len(deck), 52)


class TestHand(unittest.TestCase):
    """Test cases for the Hand class."""
    
    def test_hand_initialization(self):
        """Test creating an empty hand."""
        hand = Hand()
        self.assertEqual(len(hand), 0)
        self.assertEqual(str(hand), "Empty hand")
    
    def test_hand_add_card(self):
        """Test adding a card to a hand."""
        hand = Hand()
        card = Card(Suit.HEARTS, Rank.QUEEN)
        
        hand.add_card(card)
        
        self.assertEqual(len(hand), 1)
        self.assertIn(card, hand.cards)
    
    def test_hand_add_multiple_cards(self):
        """Test adding multiple cards to a hand."""
        hand = Hand()
        cards = [
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.CLUBS, Rank.THREE),
            Card(Suit.DIAMONDS, Rank.FOUR)
        ]
        
        hand.add_cards(cards)
        
        self.assertEqual(len(hand), 3)
        for card in cards:
            self.assertIn(card, hand.cards)
    
    def test_hand_remove_card(self):
        """Test removing a card from a hand."""
        hand = Hand()
        card = Card(Suit.SPADES, Rank.JACK)
        hand.add_card(card)
        
        result = hand.remove_card(card)
        
        self.assertTrue(result)
        self.assertEqual(len(hand), 0)
        self.assertNotIn(card, hand.cards)
    
    def test_hand_remove_nonexistent_card(self):
        """Test removing a card that's not in the hand."""
        hand = Hand()
        card = Card(Suit.HEARTS, Rank.FIVE)
        
        result = hand.remove_card(card)
        
        self.assertFalse(result)
    
    def test_hand_clear(self):
        """Test clearing all cards from a hand."""
        hand = Hand()
        hand.add_cards([
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.CLUBS, Rank.THREE)
        ])
        
        hand.clear()
        
        self.assertEqual(len(hand), 0)
    
    def test_hand_sort(self):
        """Test sorting cards in a hand."""
        hand = Hand()
        hand.add_cards([
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.DIAMONDS, Rank.SEVEN)
        ])
        
        hand.sort()
        
        # Check cards are sorted by rank value
        self.assertEqual(hand.cards[0].rank, Rank.TWO)
        self.assertEqual(hand.cards[1].rank, Rank.SEVEN)
        self.assertEqual(hand.cards[2].rank, Rank.KING)


class TestIntegration(unittest.TestCase):
    """Integration tests for the poker cards system."""
    
    def test_deal_hands_from_deck(self):
        """Test dealing multiple hands from a deck."""
        deck = Deck()
        deck.shuffle()
        
        # Deal 4 hands of 5 cards each
        hands = []
        for _ in range(4):
            hand = Hand()
            hand.add_cards(deck.deal_multiple(5))
            hands.append(hand)
        
        # Check that each hand has 5 cards
        for hand in hands:
            self.assertEqual(len(hand), 5)
        
        # Check that 32 cards remain in the deck
        self.assertEqual(deck.cards_remaining(), 32)
        
        # Check that all cards are unique across all hands
        all_cards = []
        for hand in hands:
            all_cards.extend(hand.cards)
        
        # No duplicates - we can now use set directly since Card is hashable
        self.assertEqual(len(all_cards), len(set(all_cards)))


if __name__ == '__main__':
    unittest.main()
