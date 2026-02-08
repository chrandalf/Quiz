# Quiz

A collection of coding exercises and design challenges.

## Exercises

### Poker Cards Design
A complete object-oriented design for a poker card game system.

**Files:**
- `poker_cards.py` - Main implementation (Card, Deck, Hand classes)
- `test_poker_cards.py` - Comprehensive test suite (20 tests)
- `POKER_CARDS_README.md` - Full documentation with examples

**Features:**
- Standard 52-card deck with 4 suits and 13 ranks
- Deck shuffling and dealing operations
- Hand management (add, remove, sort)
- Type-safe enums for suits and ranks
- Card comparison and sorting

**Quick Start:**
```python
from poker_cards import Deck, Hand

# Create and shuffle a deck
deck = Deck()
deck.shuffle()

# Deal a 5-card hand
hand = Hand()
hand.add_cards(deck.deal_multiple(5))
hand.sort()

print(f"Your hand: {hand}")
```

See [POKER_CARDS_README.md](POKER_CARDS_README.md) for complete documentation.