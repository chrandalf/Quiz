// Main game controller
class Game {
    constructor() {
        this.poker = new PokerGame();
        this.quiz = new QuizGame();
        this.players = [];
        this.currentPlayerIndex = 0;
        this.roundNumber = 1;
        this.gamePhase = 'setup'; // setup, poker, quiz, gameover
        this.currentQuizQuestion = null;
        this.quizAsker = null;
        this.quizAnswerer = null;
        this.handWinner = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('start-game-btn').addEventListener('click', () => this.startGame());
        document.getElementById('fold-btn').addEventListener('click', () => this.handleFold());
        document.getElementById('call-btn').addEventListener('click', () => this.handleCall());
        document.getElementById('raise-btn').addEventListener('click', () => this.handleRaise());
        document.getElementById('continue-btn').addEventListener('click', () => this.continueToNextHand());
        document.getElementById('new-game-btn').addEventListener('click', () => this.resetGame());
    }

    startGame() {
        const player1Name = document.getElementById('player1-name').value || 'Player 1';
        const player2Name = document.getElementById('player2-name').value || 'Player 2';
        const startingChips = parseInt(document.getElementById('starting-chips').value) || 1000;
        const smallBlind = parseInt(document.getElementById('small-blind').value) || 10;

        this.poker.smallBlind = smallBlind;
        this.poker.bigBlind = smallBlind * 2;

        this.players = [
            {
                name: player1Name,
                chips: startingChips,
                hand: [],
                currentBet: 0,
                hasFolded: false,
                quizCards: this.quiz.createPlayerDeck(20)
            },
            {
                name: player2Name,
                chips: startingChips,
                hand: [],
                currentBet: 0,
                hasFolded: false,
                quizCards: this.quiz.createPlayerDeck(20)
            }
        ];

        this.showScreen('game-screen');
        this.updatePlayerDisplays();
        this.startNewHand();
    }

    startNewHand() {
        this.gamePhase = 'poker';
        this.poker.reset();
        this.poker.createDeck();

        // Reset player states
        this.players.forEach(player => {
            player.currentBet = 0;
            player.hasFolded = false;
            player.hand = [];
        });

        // Deal hole cards
        this.poker.dealHoleCards(this.players[0]);
        this.poker.dealHoleCards(this.players[1]);

        // Post blinds
        this.postBlinds();

        // Start betting
        this.currentPlayerIndex = (this.poker.dealerPosition + 2) % 2; // Player after big blind
        this.poker.bettingRound = 0;

        this.updateDisplay();
        this.addMessage(`Round ${this.roundNumber} started! ${this.players[this.currentPlayerIndex].name}'s turn.`);
    }

    postBlinds() {
        const smallBlindPlayer = this.players[this.poker.dealerPosition];
        const bigBlindPlayer = this.players[(this.poker.dealerPosition + 1) % 2];

        // Small blind
        const smallBlindAmount = Math.min(this.poker.smallBlind, smallBlindPlayer.chips);
        smallBlindPlayer.chips -= smallBlindAmount;
        smallBlindPlayer.currentBet = smallBlindAmount;
        this.poker.pot += smallBlindAmount;

        // Big blind
        const bigBlindAmount = Math.min(this.poker.bigBlind, bigBlindPlayer.chips);
        bigBlindPlayer.chips -= bigBlindAmount;
        bigBlindPlayer.currentBet = bigBlindAmount;
        this.poker.pot += bigBlindAmount;
        this.poker.currentBet = bigBlindAmount;

        this.addMessage(`${smallBlindPlayer.name} posts small blind: $${smallBlindAmount}`);
        this.addMessage(`${bigBlindPlayer.name} posts big blind: $${bigBlindAmount}`);
    }

    handleFold() {
        const player = this.players[this.currentPlayerIndex];
        player.hasFolded = true;
        this.addMessage(`${player.name} folds.`, true);

        // Other player wins
        const winner = this.players[(this.currentPlayerIndex + 1) % 2];
        this.handWinner = winner;
        this.endHand();
    }

    handleCall() {
        const player = this.players[this.currentPlayerIndex];
        const callAmount = Math.min(this.poker.currentBet - player.currentBet, player.chips);
        
        player.chips -= callAmount;
        player.currentBet += callAmount;
        this.poker.pot += callAmount;

        this.addMessage(`${player.name} calls $${callAmount}.`);
        this.updateDisplay();

        if (callAmount === 0 || player.currentBet === this.poker.currentBet) {
            this.advanceAction();
        }
    }

    handleRaise() {
        const player = this.players[this.currentPlayerIndex];
        const raiseAmount = this.poker.bigBlind;
        const totalBet = this.poker.currentBet + raiseAmount;
        const amountToAdd = Math.min(totalBet - player.currentBet, player.chips);

        if (amountToAdd <= 0) {
            this.addMessage(`${player.name} doesn't have enough chips to raise.`);
            return;
        }

        player.chips -= amountToAdd;
        player.currentBet += amountToAdd;
        this.poker.pot += amountToAdd;
        this.poker.currentBet = player.currentBet;

        this.addMessage(`${player.name} raises to $${player.currentBet}.`, true);
        this.updateDisplay();
        this.advanceAction();
    }

    advanceAction() {
        // Check if betting round is complete
        const activePlayers = this.players.filter(p => !p.hasFolded);
        const allBetsEqual = activePlayers.every(p => p.currentBet === this.poker.currentBet || p.chips === 0);

        if (allBetsEqual && activePlayers.length > 0) {
            this.advanceBettingRound();
        } else {
            this.currentPlayerIndex = (this.currentPlayerIndex + 1) % 2;
            if (this.players[this.currentPlayerIndex].hasFolded) {
                this.advanceAction();
            } else {
                this.updateDisplay();
            }
        }
    }

    advanceBettingRound() {
        this.poker.bettingRound++;

        // Reset current bets
        this.players.forEach(player => player.currentBet = 0);
        this.poker.currentBet = 0;

        if (this.poker.bettingRound === 1) {
            // Flop
            this.poker.dealCommunityCards(3);
            this.addMessage('Flop dealt!', true);
        } else if (this.poker.bettingRound === 2) {
            // Turn
            this.poker.dealCommunityCards(1);
            this.addMessage('Turn dealt!', true);
        } else if (this.poker.bettingRound === 3) {
            // River
            this.poker.dealCommunityCards(1);
            this.addMessage('River dealt!', true);
        } else if (this.poker.bettingRound === 4) {
            // Showdown
            this.showdown();
            return;
        }

        this.currentPlayerIndex = this.poker.dealerPosition;
        this.updateDisplay();
    }

    showdown() {
        const result = this.poker.determineWinner(this.players);
        this.handWinner = result.winner;

        if (result.byFold) {
            this.addMessage(`${result.winner.name} wins by fold! Pot: $${this.poker.pot}`, true);
        } else {
            this.addMessage(`${result.winner.name} wins with ${result.hand.description}! Pot: $${this.poker.pot}`, true);
        }

        // Award pot (will be potentially doubled after quiz)
        this.endHand();
    }

    endHand() {
        // Show all cards
        this.updateDisplay(true);

        // Determine quiz participants
        const loser = this.players.find(p => p !== this.handWinner);
        
        // Check if loser has quiz cards
        if (loser.quizCards.length > 0) {
            this.quizAsker = loser;
            this.quizAnswerer = this.handWinner;
            setTimeout(() => this.startQuizPhase(), 2000);
        } else {
            // No quiz cards, just award pot normally
            this.handWinner.chips += this.poker.pot;
            this.addMessage(`${loser.name} has no quiz cards left!`);
            setTimeout(() => this.checkGameOver(), 2000);
        }
    }

    startQuizPhase() {
        this.gamePhase = 'quiz';
        
        // Get a random question from the loser's deck
        this.currentQuizQuestion = this.quiz.getRandomQuestion(this.quizAsker.quizCards);
        
        if (!this.currentQuizQuestion) {
            // No more questions
            this.handWinner.chips += this.poker.pot;
            this.checkGameOver();
            return;
        }

        this.showScreen('quiz-screen');
        this.displayQuiz();
    }

    displayQuiz() {
        document.getElementById('quiz-instruction').textContent = 
            `${this.quizAsker.name} asks ${this.quizAnswerer.name} a question. Get it right for DOUBLE chips!`;
        
        document.getElementById('quiz-question').textContent = this.currentQuizQuestion.question;
        
        const optionsContainer = document.getElementById('quiz-options');
        optionsContainer.innerHTML = '';
        
        this.currentQuizQuestion.options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'quiz-option';
            optionDiv.textContent = option;
            optionDiv.addEventListener('click', () => this.handleQuizAnswer(index));
            optionsContainer.appendChild(optionDiv);
        });

        document.getElementById('quiz-result').classList.add('hidden');
        document.getElementById('continue-btn').classList.add('hidden');
    }

    handleQuizAnswer(answerIndex) {
        const isCorrect = this.quiz.checkAnswer(this.currentQuizQuestion, answerIndex);
        
        // Disable all options
        const options = document.querySelectorAll('.quiz-option');
        options.forEach((option, index) => {
            option.classList.add('disabled');
            if (index === this.currentQuizQuestion.correctAnswer) {
                option.classList.add('correct');
            } else if (index === answerIndex && !isCorrect) {
                option.classList.add('incorrect');
            }
        });

        // Show result
        const resultDiv = document.getElementById('quiz-result');
        resultDiv.classList.remove('hidden');
        
        if (isCorrect) {
            resultDiv.className = 'quiz-result correct';
            const doubleAmount = this.poker.pot * 2;
            resultDiv.textContent = `🎉 Correct! ${this.quizAnswerer.name} wins DOUBLE the pot: $${doubleAmount}!`;
            // Winner gets pot, plus extra pot-amount taken from loser
            this.quizAnswerer.chips += this.poker.pot;
            const extraAmount = Math.min(this.poker.pot, this.quizAsker.chips);
            this.quizAsker.chips -= extraAmount;
            this.quizAnswerer.chips += extraAmount;
        } else {
            resultDiv.className = 'quiz-result incorrect';
            resultDiv.textContent = `❌ Wrong! The correct answer was: ${this.currentQuizQuestion.options[this.currentQuizQuestion.correctAnswer]}. ${this.quizAnswerer.name} wins the regular pot: $${this.poker.pot}`;
            this.quizAnswerer.chips += this.poker.pot;
        }

        document.getElementById('continue-btn').classList.remove('hidden');
    }

    continueToNextHand() {
        this.updatePlayerDisplays();
        this.checkGameOver();
    }

    checkGameOver() {
        // Check if any player is out of chips or out of quiz cards
        const player1 = this.players[0];
        const player2 = this.players[1];

        if (player1.chips <= 0 || player2.chips <= 0) {
            this.endGame();
            return;
        }

        // Move to next round
        this.roundNumber++;
        this.poker.dealerPosition = (this.poker.dealerPosition + 1) % 2;
        this.showScreen('game-screen');
        this.startNewHand();
    }

    endGame() {
        this.gamePhase = 'gameover';
        this.showScreen('game-over-screen');
        
        const winner = this.players[0].chips > this.players[1].chips ? this.players[0] : this.players[1];
        
        document.getElementById('winner-message').textContent = `${winner.name} wins the game!`;
        
        const statsDiv = document.getElementById('final-stats');
        statsDiv.innerHTML = `
            <p><strong>${this.players[0].name}:</strong> $${this.players[0].chips} | Quiz Cards Left: ${this.players[0].quizCards.length}</p>
            <p><strong>${this.players[1].name}:</strong> $${this.players[1].chips} | Quiz Cards Left: ${this.players[1].quizCards.length}</p>
            <p><strong>Total Rounds:</strong> ${this.roundNumber - 1}</p>
        `;
    }

    resetGame() {
        this.roundNumber = 1;
        this.poker.dealerPosition = 0;
        this.showScreen('setup-screen');
    }

    updateDisplay(showAllCards = false) {
        // Update round and pot
        document.getElementById('round-number').textContent = `Round: ${this.roundNumber}`;
        document.getElementById('pot-amount').textContent = `Pot: $${this.poker.pot}`;

        // Update players
        this.players.forEach((player, index) => {
            const playerNum = index + 1;
            const playerArea = document.getElementById(`player${playerNum}-area`);
            
            // Highlight active player
            if (index === this.currentPlayerIndex && !player.hasFolded) {
                playerArea.classList.add('active');
            } else {
                playerArea.classList.remove('active');
            }

            // Update stats
            document.getElementById(`player${playerNum}-chips`).textContent = `Chips: $${player.chips}`;
            document.getElementById(`player${playerNum}-quiz-cards`).textContent = `Quiz Cards: ${player.quizCards.length}`;

            // Display cards
            const cardsContainer = document.getElementById(`player${playerNum}-cards`);
            cardsContainer.innerHTML = '';
            
            if (player.hand && player.hand.length > 0 && (showAllCards || index === this.currentPlayerIndex)) {
                player.hand.forEach(card => {
                    const cardDiv = this.createCardElement(card);
                    cardsContainer.appendChild(cardDiv);
                });
            } else if (player.hand && player.hand.length > 0) {
                // Show card backs for opponent
                for (let i = 0; i < 2; i++) {
                    const cardBack = document.createElement('div');
                    cardBack.className = 'card-back';
                    cardBack.textContent = '🂠';
                    cardsContainer.appendChild(cardBack);
                }
            }
        });

        // Update community cards
        const communityContainer = document.getElementById('community-cards-container');
        communityContainer.innerHTML = '';
        this.poker.communityCards.forEach(card => {
            const cardDiv = this.createCardElement(card);
            communityContainer.appendChild(cardDiv);
        });

        // Update action buttons
        this.updateActionButtons();
        this.updatePlayerDisplays();
    }

    updatePlayerDisplays() {
        this.players.forEach((player, index) => {
            const playerNum = index + 1;
            document.getElementById(`player${playerNum}-display-name`).textContent = player.name;
            document.getElementById(`player${playerNum}-chips`).textContent = `Chips: $${player.chips}`;
            document.getElementById(`player${playerNum}-quiz-cards`).textContent = `Quiz Cards: ${player.quizCards.length}`;
        });
    }

    updateActionButtons() {
        const currentPlayer = this.players[this.currentPlayerIndex];
        const foldBtn = document.getElementById('fold-btn');
        const callBtn = document.getElementById('call-btn');
        const raiseBtn = document.getElementById('raise-btn');

        if (currentPlayer.hasFolded || currentPlayer.chips <= 0) {
            foldBtn.disabled = true;
            callBtn.disabled = true;
            raiseBtn.disabled = true;
            return;
        }

        foldBtn.disabled = false;
        callBtn.disabled = false;
        raiseBtn.disabled = currentPlayer.chips <= this.poker.currentBet - currentPlayer.currentBet;

        // Update call button text
        const callAmount = this.poker.currentBet - currentPlayer.currentBet;
        if (callAmount === 0) {
            callBtn.textContent = 'Check';
        } else {
            callBtn.textContent = `Call $${Math.min(callAmount, currentPlayer.chips)}`;
        }
    }

    createCardElement(card) {
        const cardDiv = document.createElement('div');
        cardDiv.className = `card ${card.color}`;
        cardDiv.innerHTML = `
            <div class="rank">${card.rank}</div>
            <div class="suit">${card.suit}</div>
        `;
        return cardDiv;
    }

    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }

    addMessage(message, important = false) {
        const messagesContainer = document.getElementById('game-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `game-message ${important ? 'important' : ''}`;
        messageDiv.textContent = message;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.game = new Game();
});
