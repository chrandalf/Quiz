# Poker Cards Design

A clean, object-oriented design for a poker card game system implemented in Python.

## Overview

This implementation provides a complete card game framework with three main classes:
- **Card**: Represents a single playing card
- **Deck**: Manages a standard 52-card deck
- **Hand**: Represents a player's hand of cards

## Features

- ✅ Full standard 52-card deck (4 suits × 13 ranks)
- ✅ Deck shuffling and dealing
- ✅ Hand management (add, remove, sort cards)
- ✅ Type-safe enums for suits and ranks
- ✅ Card comparison and sorting by rank
- ✅ Comprehensive test coverage (20 tests, all passing)

## Classes

### Suit (Enum)
Represents the four suits in a standard deck:
- HEARTS
- DIAMONDS
- CLUBS
- SPADES

### Rank (Enum)
Represents card ranks from 2 to Ace:
- TWO through TEN (2-10)
- JACK, QUEEN, KING, ACE
- Each rank has a numeric value for comparison
- Each rank has a display string (e.g., "A", "K", "Q", "J", "10")

### Card
Represents a single playing card.

**Attributes:**
- `suit`: The card's suit
- `rank`: The card's rank

**Methods:**
- `__str__()`: Returns human-readable string (e.g., "A of Hearts")
- `__eq__()`: Compares cards for equality
- `__lt__()`: Compares cards by rank value

**Example:**
```python
from poker_cards import Card, Suit, Rank

card = Card(Suit.HEARTS, Rank.ACE)
print(card)  # Output: A of Hearts
```

### Deck
Manages a 52-card deck with shuffling and dealing capabilities.

**Methods:**
- `shuffle()`: Randomly shuffles the deck
- `deal()`: Deals a single card from the top
- `deal_multiple(n)`: Deals n cards at once
- `cards_remaining()`: Returns number of cards left
- `reset()`: Restores deck to full 52 cards

**Example:**
```python
from poker_cards import Deck

deck = Deck()
deck.shuffle()
card = deck.deal()
print(f"Dealt: {card}")
print(f"Remaining: {deck.cards_remaining()}")
```

### Hand
Represents a player's collection of cards.

**Methods:**
- `add_card(card)`: Adds a single card
- `add_cards(cards)`: Adds multiple cards
- `remove_card(card)`: Removes a specific card
- `clear()`: Removes all cards
- `sort()`: Sorts cards by rank

**Example:**
```python
from poker_cards import Hand, Deck

deck = Deck()
deck.shuffle()

hand = Hand()
hand.add_cards(deck.deal_multiple(5))
hand.sort()
print(f"Your hand: {hand}")
```

## Usage Examples

### Basic Game Setup
```python
from poker_cards import Deck, Hand

# Create and shuffle a deck
deck = Deck()
deck.shuffle()

# Deal cards to two players
player1 = Hand()
player2 = Hand()

player1.add_cards(deck.deal_multiple(5))
player2.add_cards(deck.deal_multiple(5))

print(f"Player 1: {player1}")
print(f"Player 2: {player2}")
print(f"Cards remaining: {deck.cards_remaining()}")
```

### Working with Cards
```python
from poker_cards import Card, Suit, Rank

# Create specific cards
ace_of_spades = Card(Suit.SPADES, Rank.ACE)
king_of_hearts = Card(Suit.HEARTS, Rank.KING)

# Compare cards
if ace_of_spades > king_of_hearts:
    print(f"{ace_of_spades} beats {king_of_hearts}")
```

### Managing Hands
```python
from poker_cards import Hand, Deck

deck = Deck()
deck.shuffle()

hand = Hand()
hand.add_cards(deck.deal_multiple(5))

print(f"Original hand: {hand}")

# Sort cards by rank
hand.sort()
print(f"Sorted hand: {hand}")

# Remove a card
card_to_discard = hand.cards[0]
hand.remove_card(card_to_discard)
print(f"After discard: {hand}")

# Draw a new card
hand.add_card(deck.deal())
print(f"After draw: {hand}")
```

## Testing

Run the comprehensive test suite:

```bash
python -m unittest test_poker_cards -v
```

The test suite includes:
- Unit tests for Card class (creation, comparison, equality)
- Unit tests for Deck class (initialization, shuffling, dealing)
- Unit tests for Hand class (add, remove, sort operations)
- Integration tests (dealing multiple hands from a deck)

All 20 tests pass successfully.

## Design Decisions

1. **Enums for Suits and Ranks**: Provides type safety and prevents invalid card creation
2. **Rank Numeric Values**: Enables easy comparison and sorting (2=2, ..., K=13, A=14)
3. **Error Handling**: Raises appropriate exceptions for invalid operations (empty deck, too many cards)
4. **Immutable Cards**: Cards are created with a suit and rank that cannot be changed
5. **Clean String Representations**: Both user-friendly (`__str__`) and debug-friendly (`__repr__`) formats

## Future Enhancements

Possible extensions to this design:
- Poker hand evaluation (flush, straight, full house, etc.)
- Multiple deck support (for games like Blackjack)
- Wild cards and jokers
- Card game rules engine
- Player management system

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## License

This is a coding exercise/quiz implementation demonstrating object-oriented design principles.
