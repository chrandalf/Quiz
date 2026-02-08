// Poker game logic
class PokerGame {
    constructor() {
        this.deck = [];
        this.communityCards = [];
        this.pot = 0;
        this.currentBet = 0;
        this.smallBlind = 10;
        this.bigBlind = 20;
        this.dealerPosition = 0;
        this.currentPlayerIndex = 0;
        this.bettingRound = 0;
        this.handInProgress = false;
    }

    // Card suits and ranks
    static suits = ['♠', '♥', '♦', '♣'];
    static ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    static rankValues = { '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14 };

    createDeck() {
        this.deck = [];
        for (let suit of PokerGame.suits) {
            for (let rank of PokerGame.ranks) {
                this.deck.push({ rank, suit, color: (suit === '♥' || suit === '♦') ? 'red' : 'black' });
            }
        }
        this.shuffleDeck();
    }

    shuffleDeck() {
        for (let i = this.deck.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.deck[i], this.deck[j]] = [this.deck[j], this.deck[i]];
        }
    }

    dealCard() {
        return this.deck.pop();
    }

    dealHoleCards(player) {
        player.hand = [this.dealCard(), this.dealCard()];
        player.currentBet = 0;
        player.hasFolded = false;
    }

    dealCommunityCards(count) {
        for (let i = 0; i < count; i++) {
            this.communityCards.push(this.dealCard());
        }
    }

    // Hand ranking functions
    evaluateHand(hand, communityCards) {
        const allCards = [...hand, ...communityCards];
        const bestHand = this.findBestFiveCardHand(allCards);
        return bestHand;
    }

    findBestFiveCardHand(cards) {
        if (cards.length < 5) return { rank: 0, cards: cards };

        let bestHand = { rank: 0, cards: [], description: 'High Card' };

        // Generate all possible 5-card combinations
        const combinations = this.getCombinations(cards, 5);

        for (let combo of combinations) {
            const handRank = this.rankHand(combo);
            if (handRank.rank > bestHand.rank || 
                (handRank.rank === bestHand.rank && this.compareHighCards(handRank.cards, bestHand.cards) > 0)) {
                bestHand = handRank;
            }
        }

        return bestHand;
    }

    getCombinations(arr, k) {
        if (k === 1) return arr.map(item => [item]);
        
        const combinations = [];
        for (let i = 0; i < arr.length - k + 1; i++) {
            const head = arr[i];
            const tailCombos = this.getCombinations(arr.slice(i + 1), k - 1);
            for (let combo of tailCombos) {
                combinations.push([head, ...combo]);
            }
        }
        return combinations;
    }

    rankHand(cards) {
        const sortedCards = cards.sort((a, b) => PokerGame.rankValues[b.rank] - PokerGame.rankValues[a.rank]);
        
        const isFlush = this.checkFlush(sortedCards);
        const isStraight = this.checkStraight(sortedCards);
        const counts = this.getCardCounts(sortedCards);

        // Royal Flush
        if (isFlush && isStraight && sortedCards[0].rank === 'A' && sortedCards[1].rank === 'K') {
            return { rank: 10, cards: sortedCards, description: 'Royal Flush' };
        }

        // Straight Flush
        if (isFlush && isStraight) {
            return { rank: 9, cards: sortedCards, description: 'Straight Flush' };
        }

        // Four of a Kind
        if (counts.fourOfAKind) {
            return { rank: 8, cards: sortedCards, description: 'Four of a Kind' };
        }

        // Full House (three of a kind + a pair)
        const rankCounts = {};
        for (let card of sortedCards) {
            rankCounts[card.rank] = (rankCounts[card.rank] || 0) + 1;
        }
        const hasThreeOfAKind = Object.values(rankCounts).includes(3);
        const hasPair = Object.values(rankCounts).includes(2);
        if (hasThreeOfAKind && hasPair) {
            return { rank: 7, cards: sortedCards, description: 'Full House' };
        }

        // Flush
        if (isFlush) {
            return { rank: 6, cards: sortedCards, description: 'Flush' };
        }

        // Straight
        if (isStraight) {
            return { rank: 5, cards: sortedCards, description: 'Straight' };
        }

        // Three of a Kind
        if (counts.threeOfAKind) {
            return { rank: 4, cards: sortedCards, description: 'Three of a Kind' };
        }

        // Two Pair
        if (counts.pairs >= 2) {
            return { rank: 3, cards: sortedCards, description: 'Two Pair' };
        }

        // One Pair
        if (counts.pairs === 1) {
            return { rank: 2, cards: sortedCards, description: 'One Pair' };
        }

        // High Card
        return { rank: 1, cards: sortedCards, description: 'High Card' };
    }

    checkFlush(cards) {
        const suit = cards[0].suit;
        return cards.every(card => card.suit === suit);
    }

    checkStraight(cards) {
        const values = cards.map(card => PokerGame.rankValues[card.rank]).sort((a, b) => b - a);
        
        // Check regular straight
        for (let i = 0; i < values.length - 1; i++) {
            if (values[i] - values[i + 1] !== 1) {
                // Check for A-2-3-4-5 (wheel)
                if (i === 0 && values[0] === 14 && values[1] === 5 && values[2] === 4 && values[3] === 3 && values[4] === 2) {
                    return true;
                }
                return false;
            }
        }
        return true;
    }

    getCardCounts(cards) {
        const rankCounts = {};
        for (let card of cards) {
            rankCounts[card.rank] = (rankCounts[card.rank] || 0) + 1;
        }

        const counts = Object.values(rankCounts);
        return {
            fourOfAKind: counts.includes(4),
            threeOfAKind: counts.includes(3),
            pairs: counts.filter(c => c === 2).length
        };
    }

    compareHighCards(cards1, cards2) {
        for (let i = 0; i < Math.min(cards1.length, cards2.length); i++) {
            const val1 = PokerGame.rankValues[cards1[i].rank];
            const val2 = PokerGame.rankValues[cards2[i].rank];
            if (val1 > val2) return 1;
            if (val1 < val2) return -1;
        }
        return 0;
    }

    determineWinner(players) {
        const activePlayers = players.filter(p => !p.hasFolded);
        
        if (activePlayers.length === 1) {
            return { winner: activePlayers[0], byFold: true };
        }

        let bestPlayer = activePlayers[0];
        let bestHand = this.evaluateHand(bestPlayer.hand, this.communityCards);

        for (let i = 1; i < activePlayers.length; i++) {
            const player = activePlayers[i];
            const playerHand = this.evaluateHand(player.hand, this.communityCards);

            if (playerHand.rank > bestHand.rank ||
                (playerHand.rank === bestHand.rank && this.compareHighCards(playerHand.cards, bestHand.cards) > 0)) {
                bestPlayer = player;
                bestHand = playerHand;
            }
        }

        return { winner: bestPlayer, hand: bestHand, byFold: false };
    }

    reset() {
        this.deck = [];
        this.communityCards = [];
        this.pot = 0;
        this.currentBet = 0;
        this.bettingRound = 0;
        this.handInProgress = false;
    }
}

// Export for use in game.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PokerGame;
}
