# Quiz - Play with Friends! 🎯

A fun, interactive quiz game that you can play with your friends in real-time!

## Features

- 🎮 Multiplayer gameplay - play with friends using room codes
- 📊 Real-time score tracking
- 🏆 Competitive leaderboard
- 💡 10 trivia questions covering various topics
- 🎨 Beautiful, responsive UI
- 📱 Works on desktop and mobile devices

## How to Play

### Creating a Game
1. Open `index.html` in your web browser
2. Click "Create New Game"
3. Enter your name
4. Share the generated room code with your friends

### Joining a Game
1. Open `index.html` in your web browser
2. Click "Join Game"
3. Enter your name and the room code shared by your friend
4. Wait for the host to start the game

### Playing
- Answer questions by clicking on your chosen answer
- Each correct answer gives you 10 points
- Click "Next Question" to proceed
- See final scores and rankings at the end!

## Technical Details

This is a self-contained HTML/CSS/JavaScript application that uses localStorage for simple multiplayer functionality. **It works by having multiple browser tabs open on the same device** - friends can each open the game in their own tab and join using the room code.

**Note:** This implementation is designed for local play (multiple tabs on the same browser). For true cross-device/network play, you would need to implement:
- A proper backend server for cross-network play
- WebSocket connections for real-time updates
- A database for persistent game storage
- User authentication

## Getting Started

Simply open `index.html` in any modern web browser. No installation or setup required!

## Contributing

Feel free to fork this repository and add more features like:
- Custom quiz categories
- Difficulty levels
- Time limits for questions
- Power-ups and bonuses
- Achievement system

Enjoy playing! 🎉