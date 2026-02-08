"""
Poker Cards Design

This module implements a simple object-oriented design for a poker card game system.
It includes Card, Deck, and Hand classes to represent standard playing cards.
"""

from enum import Enum
from typing import List
import random


class Suit(Enum):
    """Enum representing the four suits in a standard deck of cards."""
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Rank(Enum):
    """Enum representing the ranks of cards in a standard deck."""
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")
    
    def __init__(self, numeric_value: int, display: str):
        self._numeric_value = numeric_value
        self.display = display
    
    @property
    def numeric_value(self) -> int:
        """Get the numeric value for card comparison."""
        return self._numeric_value


class Card:
    """Represents a single playing card with a suit and rank."""
    
    def __init__(self, suit: Suit, rank: Rank):
        """
        Initialize a card with a suit and rank.
        
        Args:
            suit: The suit of the card (Hearts, Diamonds, Clubs, Spades)
            rank: The rank of the card (2-10, Jack, Queen, King, Ace)
        """
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        """Return a string representation of the card."""
        return f"{self.rank.display} of {self.suit.value}"
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the card."""
        return f"Card(suit={self.suit.name}, rank={self.rank.name})"
    
    def __eq__(self, other) -> bool:
        """
        Check if two cards are equal.
        
        Cards are equal if they have the same suit and rank.
        """
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self) -> int:
        """Make Card hashable so it can be used in sets and as dict keys."""
        return hash((self.suit, self.rank))
    
    def __lt__(self, other) -> bool:
        """
        Compare cards by rank value for sorting.
        
        Note: Comparison is based on rank only, not suit. This is typical
        for poker where card rank determines value (e.g., Ace > King).
        
        Args:
            other: Another Card to compare with.
            
        Returns:
            True if this card's rank is less than the other card's rank.
        """
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank.numeric_value < other.rank.numeric_value


class Deck:
    """Represents a deck of 52 playing cards."""
    
    def __init__(self):
        """Initialize a standard deck of 52 cards."""
        self.cards: List[Card] = []
        self._initialize_deck()
    
    def _initialize_deck(self):
        """Create a standard deck with all 52 cards."""
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
    
    def shuffle(self):
        """Shuffle the deck randomly."""
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        """
        Deal one card from the top of the deck.
        
        Returns:
            The card dealt from the deck.
            
        Raises:
            IndexError: If the deck is empty.
        """
        if not self.cards:
            raise IndexError("Cannot deal from an empty deck")
        return self.cards.pop()
    
    def deal_multiple(self, num_cards: int) -> List[Card]:
        """
        Deal multiple cards from the deck.
        
        Args:
            num_cards: The number of cards to deal.
            
        Returns:
            A list of cards dealt from the deck.
            
        Raises:
            ValueError: If trying to deal more cards than available.
        """
        if num_cards > len(self.cards):
            raise ValueError(f"Cannot deal {num_cards} cards, only {len(self.cards)} remaining")
        return [self.deal() for _ in range(num_cards)]
    
    def cards_remaining(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self.cards)
    
    def reset(self):
        """Reset the deck to a full 52-card deck."""
        self._initialize_deck()
    
    def __len__(self) -> int:
        """Return the number of cards in the deck."""
        return len(self.cards)
    
    def __str__(self) -> str:
        """Return a string representation of the deck."""
        return f"Deck with {len(self.cards)} cards"


class Hand:
    """Represents a player's hand of cards."""
    
    def __init__(self):
        """Initialize an empty hand."""
        self.cards: List[Card] = []
    
    def add_card(self, card: Card):
        """
        Add a card to the hand.
        
        Args:
            card: The card to add to the hand.
        """
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]):
        """
        Add multiple cards to the hand.
        
        Args:
            cards: List of cards to add to the hand.
        """
        self.cards.extend(cards)
    
    def remove_card(self, card: Card) -> bool:
        """
        Remove a specific card from the hand.
        
        Args:
            card: The card to remove.
            
        Returns:
            True if the card was removed, False if not found.
        """
        try:
            self.cards.remove(card)
            return True
        except ValueError:
            return False
    
    def clear(self):
        """Remove all cards from the hand."""
        self.cards.clear()
    
    def sort(self):
        """Sort the cards in the hand by rank."""
        self.cards.sort()
    
    def __len__(self) -> int:
        """Return the number of cards in the hand."""
        return len(self.cards)
    
    def __str__(self) -> str:
        """Return a string representation of the hand."""
        if not self.cards:
            return "Empty hand"
        return ", ".join(str(card) for card in self.cards)
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the hand."""
        return f"Hand({len(self.cards)} cards: {[repr(card) for card in self.cards]})"


# Example usage
if __name__ == "__main__":
    # Create a new deck
    deck = Deck()
    print(f"Created {deck}")
    
    # Shuffle the deck
    deck.shuffle()
    print("Shuffled the deck")
    
    # Deal a hand of 5 cards
    hand = Hand()
    hand.add_cards(deck.deal_multiple(5))
    print(f"\nDealt hand: {hand}")
    
    # Sort the hand
    hand.sort()
    print(f"Sorted hand: {hand}")
    
    # Check remaining cards
    print(f"\nCards remaining in deck: {deck.cards_remaining()}")
    
    # Deal another hand
    hand2 = Hand()
    hand2.add_cards(deck.deal_multiple(5))
    print(f"Second hand: {hand2}")
    
    print(f"\nCards remaining in deck: {deck.cards_remaining()}")
