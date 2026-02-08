// Quiz game logic
class QuizGame {
    constructor() {
        this.quizQuestions = this.generateQuizQuestions();
    }

    generateQuizQuestions() {
        // A collection of quiz questions - can be expanded or loaded from external source
        return [
            {
                question: "What is the capital of France?",
                options: ["London", "Berlin", "Paris", "Madrid"],
                correctAnswer: 2
            },
            {
                question: "What is 15 × 8?",
                options: ["120", "130", "110", "125"],
                correctAnswer: 0
            },
            {
                question: "Who painted the Mona Lisa?",
                options: ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
                correctAnswer: 1
            },
            {
                question: "What is the largest planet in our solar system?",
                options: ["Saturn", "Neptune", "Jupiter", "Uranus"],
                correctAnswer: 2
            },
            {
                question: "In which year did World War II end?",
                options: ["1943", "1944", "1945", "1946"],
                correctAnswer: 2
            },
            {
                question: "What is the chemical symbol for gold?",
                options: ["Go", "Gd", "Au", "Ag"],
                correctAnswer: 2
            },
            {
                question: "How many continents are there?",
                options: ["5", "6", "7", "8"],
                correctAnswer: 2
            },
            {
                question: "What is the speed of light (approximately)?",
                options: ["300,000 km/s", "150,000 km/s", "500,000 km/s", "200,000 km/s"],
                correctAnswer: 0
            },
            {
                question: "Who wrote 'Romeo and Juliet'?",
                options: ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                correctAnswer: 1
            },
            {
                question: "What is the smallest prime number?",
                options: ["0", "1", "2", "3"],
                correctAnswer: 2
            },
            {
                question: "How many strings does a standard guitar have?",
                options: ["4", "5", "6", "7"],
                correctAnswer: 2
            },
            {
                question: "What is the longest river in the world?",
                options: ["Amazon", "Nile", "Mississippi", "Yangtze"],
                correctAnswer: 1
            },
            {
                question: "What is the boiling point of water at sea level?",
                options: ["90°C", "100°C", "110°C", "120°C"],
                correctAnswer: 1
            },
            {
                question: "In which country is the Great Barrier Reef located?",
                options: ["Brazil", "Australia", "Indonesia", "Philippines"],
                correctAnswer: 1
            },
            {
                question: "What is the currency of Japan?",
                options: ["Yuan", "Won", "Yen", "Ringgit"],
                correctAnswer: 2
            },
            {
                question: "How many sides does a hexagon have?",
                options: ["5", "6", "7", "8"],
                correctAnswer: 1
            },
            {
                question: "Who was the first person to walk on the moon?",
                options: ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "Alan Shepard"],
                correctAnswer: 1
            },
            {
                question: "What is the hardest natural substance on Earth?",
                options: ["Gold", "Iron", "Diamond", "Platinum"],
                correctAnswer: 2
            },
            {
                question: "Which ocean is the largest?",
                options: ["Atlantic", "Pacific", "Indian", "Arctic"],
                correctAnswer: 1
            },
            {
                question: "What is the square root of 144?",
                options: ["10", "11", "12", "13"],
                correctAnswer: 2
            },
            {
                question: "How many hours are in a week?",
                options: ["148", "156", "168", "176"],
                correctAnswer: 2
            },
            {
                question: "What is the main ingredient in guacamole?",
                options: ["Tomato", "Avocado", "Pepper", "Onion"],
                correctAnswer: 1
            },
            {
                question: "Which planet is known as the Red Planet?",
                options: ["Venus", "Mars", "Jupiter", "Saturn"],
                correctAnswer: 1
            },
            {
                question: "What is the capital of Italy?",
                options: ["Venice", "Milan", "Rome", "Florence"],
                correctAnswer: 2
            },
            {
                question: "How many degrees are in a circle?",
                options: ["180", "270", "360", "450"],
                correctAnswer: 2
            },
            {
                question: "What is the largest mammal in the world?",
                options: ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
                correctAnswer: 1
            },
            {
                question: "Who invented the telephone?",
                options: ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Benjamin Franklin"],
                correctAnswer: 1
            },
            {
                question: "What is the freezing point of water?",
                options: ["-10°C", "0°C", "10°C", "32°C"],
                correctAnswer: 1
            },
            {
                question: "How many players are on a soccer team?",
                options: ["9", "10", "11", "12"],
                correctAnswer: 2
            },
            {
                question: "What is the smallest country in the world?",
                options: ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
                correctAnswer: 1
            },
            {
                question: "Which gas do plants absorb from the atmosphere?",
                options: ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
                correctAnswer: 2
            },
            {
                question: "How many bones are in the adult human body?",
                options: ["186", "206", "226", "246"],
                correctAnswer: 1
            },
            {
                question: "What is the capital of Canada?",
                options: ["Toronto", "Vancouver", "Ottawa", "Montreal"],
                correctAnswer: 2
            },
            {
                question: "What is the symbol for pi (π)?",
                options: ["3.14", "3.15", "3.16", "3.17"],
                correctAnswer: 0
            },
            {
                question: "In which year did the Titanic sink?",
                options: ["1910", "1911", "1912", "1913"],
                correctAnswer: 2
            },
            {
                question: "What is the main component of the Sun?",
                options: ["Helium", "Hydrogen", "Oxygen", "Carbon"],
                correctAnswer: 1
            },
            {
                question: "How many teeth does an adult human have?",
                options: ["28", "30", "32", "34"],
                correctAnswer: 2
            },
            {
                question: "What is the largest organ in the human body?",
                options: ["Heart", "Liver", "Brain", "Skin"],
                correctAnswer: 3
            },
            {
                question: "Which country is known as the Land of the Rising Sun?",
                options: ["China", "Japan", "South Korea", "Thailand"],
                correctAnswer: 1
            },
            {
                question: "How many minutes are in 3 hours?",
                options: ["150", "160", "170", "180"],
                correctAnswer: 3
            }
        ];
    }

    createPlayerDeck(numCards = 20) {
        // Shuffle questions and take the specified number
        const shuffled = [...this.quizQuestions].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, numCards);
    }

    getRandomQuestion(playerDeck) {
        if (playerDeck.length === 0) {
            return null;
        }
        const index = Math.floor(Math.random() * playerDeck.length);
        return playerDeck.splice(index, 1)[0];
    }

    checkAnswer(question, answerIndex) {
        return answerIndex === question.correctAnswer;
    }
}

// Export for use in game.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuizGame;
}
