/**
 * Quiz Application - Simple Implementation
 * 
 * This is a basic implementation showing how to load and use the quiz data.
 * It can be extended for a full-featured quiz application.
 */

class QuizApp {
  constructor(quizData) {
    this.quizzes = quizData.quizzes;
    this.currentQuiz = null;
    this.currentQuestionIndex = 0;
    this.answers = [];
    this.score = 0;
    this.startTime = null;
  }

  /**
   * Load quiz by ID
   */
  loadQuiz(quizId) {
    this.currentQuiz = this.quizzes.find(q => q.id === quizId);
    if (!this.currentQuiz) {
      throw new Error(`Quiz with id "${quizId}" not found`);
    }
    
    // Shuffle questions if enabled
    if (this.currentQuiz.settings?.shuffleQuestions) {
      this.currentQuiz.questions = this.shuffleArray([...this.currentQuiz.questions]);
    }
    
    this.currentQuestionIndex = 0;
    this.answers = [];
    this.score = 0;
    this.startTime = Date.now();
    
    return this.currentQuiz;
  }

  /**
   * Get current question
   */
  getCurrentQuestion() {
    if (!this.currentQuiz) {
      throw new Error('No quiz loaded');
    }
    return this.currentQuiz.questions[this.currentQuestionIndex];
  }

  /**
   * Get question with shuffled options if enabled
   */
  getQuestionWithOptions(question) {
    const questionCopy = { ...question };
    
    // Shuffle options if enabled and question has options
    if (this.currentQuiz.settings?.shuffleOptions && question.options) {
      questionCopy.options = this.shuffleArray([...question.options]);
    }
    
    return questionCopy;
  }

  /**
   * Submit answer for current question
   */
  submitAnswer(userAnswer) {
    const question = this.getCurrentQuestion();
    const isCorrect = this.checkAnswer(question, userAnswer);
    
    const result = {
      questionId: question.id,
      userAnswer,
      correctAnswer: question.correctAnswer,
      isCorrect,
      points: isCorrect ? question.points : 0,
      explanation: question.explanation
    };
    
    this.answers.push(result);
    if (isCorrect) {
      this.score += question.points;
    }
    
    return result;
  }

  /**
   * Check if answer is correct
   */
  checkAnswer(question, userAnswer) {
    switch (question.type) {
      case 'multiple-choice':
        return userAnswer === question.correctAnswer;
      
      case 'true-false':
        return userAnswer === question.correctAnswer;
      
      case 'short-answer':
        const correctAnswers = Array.isArray(question.correctAnswer) 
          ? question.correctAnswer 
          : [question.correctAnswer];
        return correctAnswers.some(ans => 
          ans.toLowerCase() === userAnswer.toLowerCase().trim()
        );
      
      case 'multiple-select':
        if (!Array.isArray(userAnswer)) return false;
        const correct = [...question.correctAnswer].sort();
        const user = [...userAnswer].sort();
        return JSON.stringify(correct) === JSON.stringify(user);
      
      default:
        return false;
    }
  }

  /**
   * Move to next question
   */
  nextQuestion() {
    if (this.hasNextQuestion()) {
      this.currentQuestionIndex++;
      return this.getCurrentQuestion();
    }
    return null;
  }

  /**
   * Check if there are more questions
   */
  hasNextQuestion() {
    return this.currentQuestionIndex < this.currentQuiz.questions.length - 1;
  }

  /**
   * Skip current question
   */
  skipQuestion() {
    if (!this.currentQuiz.settings?.allowSkip) {
      throw new Error('Skipping is not allowed in this quiz');
    }
    
    const question = this.getCurrentQuestion();
    this.answers.push({
      questionId: question.id,
      userAnswer: null,
      correctAnswer: question.correctAnswer,
      isCorrect: false,
      points: 0,
      skipped: true
    });
    
    return this.nextQuestion();
  }

  /**
   * Get quiz results
   */
  getResults() {
    if (!this.currentQuiz) {
      throw new Error('No quiz loaded');
    }
    
    const totalPoints = this.currentQuiz.questions.reduce((sum, q) => sum + q.points, 0);
    const percentage = Math.round((this.score / totalPoints) * 100);
    const passed = percentage >= (this.currentQuiz.settings?.passingScore || 70);
    const timeElapsed = Math.round((Date.now() - this.startTime) / 1000);
    
    return {
      score: this.score,
      totalPoints,
      percentage,
      passed,
      timeElapsed,
      answers: this.answers,
      correctCount: this.answers.filter(a => a.isCorrect).length,
      incorrectCount: this.answers.filter(a => !a.isCorrect && !a.skipped).length,
      skippedCount: this.answers.filter(a => a.skipped).length
    };
  }

  /**
   * Get progress information
   */
  getProgress() {
    return {
      current: this.currentQuestionIndex + 1,
      total: this.currentQuiz.questions.length,
      percentage: Math.round(((this.currentQuestionIndex + 1) / this.currentQuiz.questions.length) * 100)
    };
  }

  /**
   * Shuffle array helper
   */
  shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }

  /**
   * List all available quizzes
   */
  listQuizzes() {
    return this.quizzes.map(q => ({
      id: q.id,
      title: q.title,
      description: q.description,
      questionCount: q.questions.length,
      totalPoints: q.questions.reduce((sum, question) => sum + question.points, 0)
    }));
  }
}

/**
 * Example Usage
 */
async function exampleUsage() {
  // Load quiz data
  const response = await fetch('questions.json');
  const quizData = await response.json();
  
  // Create quiz app instance
  const app = new QuizApp(quizData);
  
  // List available quizzes
  console.log('Available Quizzes:');
  app.listQuizzes().forEach(quiz => {
    console.log(`- ${quiz.title} (${quiz.questionCount} questions)`);
  });
  
  // Load a specific quiz
  app.loadQuiz('general-knowledge-001');
  console.log('\nLoaded:', app.currentQuiz.title);
  
  // Get first question
  const question = app.getQuestionWithOptions(app.getCurrentQuestion());
  console.log('\nQuestion:', question.question);
  if (question.options) {
    console.log('Options:', question.options);
  }
  
  // Submit an answer
  const result = app.submitAnswer('H2O');
  console.log('Result:', result.isCorrect ? '✓ Correct!' : '✗ Incorrect');
  
  // Move to next question
  if (app.hasNextQuestion()) {
    app.nextQuestion();
  }
  
  // Get progress
  const progress = app.getProgress();
  console.log(`Progress: ${progress.current}/${progress.total} (${progress.percentage}%)`);
  
  // Get final results (after completing all questions)
  // const results = app.getResults();
  // console.log('Final Score:', results.percentage + '%');
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = QuizApp;
}

// Example: Uncomment to run
// exampleUsage();
