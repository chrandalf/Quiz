# Quiz Application Design

## Overview
This document outlines the design for a flexible quiz application that supports multiple question types and card-based UI representation.

## Question Types

### 1. Multiple Choice Questions
- Single correct answer from multiple options
- 2-6 answer choices
- Can include images or code snippets
- Immediate feedback on selection

### 2. True/False Questions
- Binary choice questions
- Simple and quick to answer
- Useful for fact verification

### 3. Short Answer Questions
- Free-text input
- Case-insensitive matching
- Support for multiple acceptable answers
- Optional hints

### 4. Multiple Select Questions
- Multiple correct answers
- All correct answers must be selected
- Partial credit optional

## Card Design Specifications

### Visual Layout
```
┌─────────────────────────────────────┐
│  Category Badge         Timer       │
│─────────────────────────────────────│
│                                     │
│  Question Text                      │
│  (supports markdown)                │
│                                     │
│─────────────────────────────────────│
│  [ ] Option A                       │
│  [ ] Option B                       │
│  [ ] Option C                       │
│  [ ] Option D                       │
│─────────────────────────────────────│
│  [Hint] [Skip]        [Submit]      │
└─────────────────────────────────────┘
```

### Card States
1. **Initial**: Question displayed with answer options
2. **Answered**: User selection highlighted
3. **Correct**: Green highlight with checkmark
4. **Incorrect**: Red highlight with explanation
5. **Skipped**: Grayed out, can be revisited

### Card Properties
- **Difficulty**: Easy, Medium, Hard
- **Category**: Topic or subject area
- **Points**: Score value (1-10)
- **Time Limit**: Optional timer
- **Tags**: For filtering and search

## Data Structure

### Question Schema
```json
{
  "id": "unique-identifier",
  "type": "multiple-choice|true-false|short-answer|multiple-select",
  "category": "category-name",
  "difficulty": "easy|medium|hard",
  "points": 1-10,
  "timeLimit": 30,
  "question": "Question text (supports markdown)",
  "options": [...],
  "correctAnswer": "...",
  "explanation": "Why this is the correct answer",
  "hint": "Optional hint text",
  "tags": ["tag1", "tag2"]
}
```

### Quiz Schema
```json
{
  "id": "quiz-identifier",
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

## User Experience Flow

1. **Start Screen**: Quiz title, description, settings preview
2. **Question Navigation**: Linear or free navigation
3. **Progress Tracking**: Question counter, progress bar
4. **Feedback**: Immediate or at end
5. **Results Screen**: Score, time taken, review option

## Accessibility Features
- Keyboard navigation support
- Screen reader friendly
- High contrast mode
- Adjustable font sizes
- Color-blind friendly indicators

## Future Enhancements
- Image-based questions
- Audio/video questions
- Code execution questions
- Timed quizzes
- Multiplayer mode
- Leaderboards
