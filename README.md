# Poker Quiz - The Ultimate Card Game 🃏🎯

A unique poker game that combines classic Texas Hold'em with trivia challenges! After each hand, the loser asks the winner a quiz question. Answer correctly to double your winnings!

## Features

- **Limit Poker**: Play Texas Hold'em with limit betting to ensure games don't end too quickly
- **Quiz Integration**: After each hand, answer trivia questions for bonus chips
- **Double or Nothing**: Get the question right and win DOUBLE the pot!
- **Quiz Card System**: Each player has 20 quiz cards (questions) to use throughout the game
- **Multiplayer Support**: Local multiplayer on the same device (future-ready for network play)

## How to Play

### Setup
1. Open `index.html` in a web browser
2. Enter player names
3. Set starting chips (default: 1000)
4. Set small blind amount (default: 10)
5. Click "Start Game"

### Poker Phase
- Players are dealt 2 hole cards each
- Blinds are automatically posted
- Betting rounds: Pre-flop, Flop (3 cards), Turn (1 card), River (1 card)
- Use **Fold**, **Call/Check**, or **Raise** buttons to play
- Game uses limit betting (raises are fixed at 1 big blind)

### Quiz Phase
- After each hand, the **losing player** asks the **winning player** a question
- The question comes from the loser's deck of quiz cards
- If answered correctly: Winner gets **DOUBLE** the pot (extra chips taken from loser)
- If answered incorrectly: Winner gets the regular pot amount
- Each player starts with 20 quiz cards

### Winning
- Game continues until:
  - A player runs out of chips, OR
  - Players want to end the game
- Player with the most chips wins!

## Technical Details

### Files
- `index.html` - Main game interface
- `style.css` - Game styling
- `poker.js` - Poker game logic (deck, hand ranking, betting)
- `quiz.js` - Quiz system (40 trivia questions)
- `game.js` - Main game controller (orchestrates poker + quiz)

### Features for Future Development
- Network multiplayer support (prepared structure)
- Additional quiz categories
- Tournament mode
- Save/load game state
- Custom quiz card decks

## Game Rules

### Poker Hands (Highest to Lowest)
1. Royal Flush
2. Straight Flush
3. Four of a Kind
4. Full House
5. Flush
6. Straight
7. Three of a Kind
8. Two Pair
9. One Pair
10. High Card

### Betting Structure (Limit)
- Small Blind: Set at game start
- Big Blind: 2x Small Blind
- Raises: Fixed at 1x Big Blind
- Limit betting ensures games don't end too quickly

## Technologies Used
- HTML5
- CSS3 (with modern features like backdrop-filter)
- Vanilla JavaScript (ES6+)
- No external dependencies

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled

## License
MIT License - Feel free to use and modify!