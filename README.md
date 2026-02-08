# Quiz Application

A flexible and comprehensive quiz application with support for multiple question types and beautiful card-based UI design.

## Features

- **Multiple Question Types**: Support for multiple choice, true/false, short answer, and multiple select questions
- **Beautiful Card Design**: Modern, responsive card-based UI with smooth animations
- **Flexible Quiz System**: Configurable quiz settings including shuffle, feedback, and passing scores
- **Rich Question Data**: Support for categories, difficulty levels, points, time limits, hints, and tags
- **Accessibility**: Keyboard navigation, screen reader support, and high contrast mode
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark Mode**: Automatic dark mode support based on system preferences

## Project Structure

```
Quiz/
├── README.md                 # This file
├── DESIGN.md                # Comprehensive design documentation
├── questions.json           # Sample quiz questions in JSON format
├── card-styles.css          # CSS styles for quiz cards
├── card-examples.html       # Visual examples of card designs
└── schema.json             # JSON schema for validation
```

## Question Types

### 1. Multiple Choice
Single correct answer from multiple options (2-6 choices).

### 2. True/False
Binary choice questions for quick fact verification.

### 3. Short Answer
Free-text input with case-insensitive matching and multiple acceptable answers.

### 4. Multiple Select
Multiple correct answers where all must be selected.

## Data Structure

### Question Format
```json
{
  "id": "unique-identifier",
  "type": "multiple-choice|true-false|short-answer|multiple-select",
  "category": "Category Name",
  "difficulty": "easy|medium|hard",
  "points": 1,
  "timeLimit": 30,
  "question": "Question text",
  "options": ["Option 1", "Option 2"],
  "correctAnswer": "Option 1",
  "explanation": "Why this is correct",
  "hint": "Optional hint",
  "tags": ["tag1", "tag2"]
}
```

### Quiz Format
```json
{
  "id": "quiz-id",
  "title": "Quiz Title",
  "description": "Quiz description",
  "questions": [...],
  "settings": {
    "shuffleQuestions": true,
    "shuffleOptions": true,
    "showFeedback": true,
    "allowSkip": true,
    "passingScore": 70
  }
}
```

## Getting Started

### Viewing Card Examples
Open `card-examples.html` in your browser to see visual examples of all card designs:

```bash
# Open in your default browser
open card-examples.html

# Or using a specific browser
firefox card-examples.html
chrome card-examples.html
```

### Using the Question Data
The `questions.json` file contains two sample quizzes:
1. **General Knowledge Quiz**: 10 questions covering various topics
2. **Programming Basics**: 5 programming-related questions

You can load and use this data in your application:

```javascript
// Load questions
fetch('questions.json')
  .then(response => response.json())
  .then(data => {
    const quizzes = data.quizzes;
    // Use quiz data in your application
  });
```

## Customization

### Card Styling
Modify `card-styles.css` to customize the appearance:

```css
:root {
  --primary-color: #4a90e2;  /* Change primary color */
  --success-color: #4caf50;  /* Success/correct color */
  --error-color: #f44336;    /* Error/incorrect color */
  /* ... more variables */
}
```

### Question Difficulty Colors
- **Easy**: Green background
- **Medium**: Orange background  
- **Hard**: Red background

## Design Principles

1. **Simplicity**: Clean, uncluttered interface
2. **Accessibility**: Keyboard navigation and screen reader support
3. **Feedback**: Immediate visual feedback on interactions
4. **Responsiveness**: Works on all device sizes
5. **Flexibility**: Easy to customize and extend

## Card States

- **Initial**: Question with selectable options
- **Selected**: User has made a selection
- **Correct**: Green highlight with checkmark
- **Incorrect**: Red highlight with correct answer shown
- **Skipped**: Grayed out, can be revisited

## Accessibility Features

- Keyboard navigation (Tab, Enter, Arrow keys)
- ARIA labels for screen readers
- High contrast mode support
- Color-blind friendly indicators (icons + colors)
- Adjustable font sizes
- Focus indicators

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Future Enhancements

- Image-based questions
- Audio/video questions
- Code execution questions
- Timed quizzes
- Multiplayer mode
- Leaderboards
- Progress tracking
- Analytics dashboard

## Documentation

See `DESIGN.md` for detailed design specifications including:
- Visual layouts
- UX flow diagrams
- Component specifications
- State management
- API considerations

## Contributing

When adding new questions:
1. Follow the JSON schema in `schema.json`
2. Include all required fields
3. Provide clear, concise question text
4. Write helpful explanations
5. Add relevant tags for filtering

## License

This project is open source and available for use in educational and commercial applications.

---

**Created with ❤️ for better learning experiences**