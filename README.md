# Planning Poker Mechanics

A Python implementation of Planning Poker (also known as Scrum Poker) - a consensus-based, gamified technique for estimating effort or complexity in Agile software development.

## 🎯 Overview

Planning Poker is an engaging estimation technique where team members use cards to independently estimate user stories. This implementation provides all the core mechanics needed to run a Planning Poker session, including:

- 🃏 Standard Fibonacci card deck (0, 1, 2, 3, 5, 8, 13, 20, 40, 100) plus special cards (?, ∞, ☕)
- 👥 Player management with observer roles
- 📖 Story management with acceptance criteria
- 🔄 Round-based estimation with reveal and discussion phases
- 🎲 Consensus checking and outlier detection
- 📊 Statistical analysis (range, average, etc.)
- ♻️ Re-voting support for reaching consensus

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pytest (for running tests)

### Installation

```bash
# Clone the repository
git clone https://github.com/chrandalf/Quiz.git
cd Quiz

# Install dependencies (optional, for testing)
pip install pytest
```

### Basic Usage

```python
from poker_mechanics import Session, Player, Story, CardValue

# Create a session
session = Session(id="sprint-1", name="Sprint 1 Planning")

# Add players
alice = Player(id="1", name="Alice")
bob = Player(id="2", name="Bob")
session.add_player(alice)
session.add_player(bob)

# Create a story
story = Story(
    id="US-101",
    title="User Login",
    description="Implement user authentication"
)

# Start estimation
session.start_round(story)
session.submit_estimate(alice, CardValue.FIVE)
session.submit_estimate(bob, CardValue.EIGHT)

# Reveal and analyze
session.reveal_estimates()
min_val, max_val = session.current_round.get_estimate_range()
avg = session.current_round.calculate_average()

# Finalize
session.finalize_round(final_estimate=5)
```

### Run the Demo

See a complete Planning Poker session in action:

```bash
python example_usage.py
```

This will demonstrate:
- Session setup with multiple players
- Story presentation
- Estimation and card reveal
- Discussion and re-voting
- Consensus and finalization

## 📚 Core Components

### CardValue (Enum)
Standard Planning Poker cards:
- **Numeric**: 0, 1, 2, 3, 5, 8, 13, 20, 40, 100 (Fibonacci sequence)
- **Special**: 
  - `?` - Uncertain/need more information
  - `∞` - Too large to estimate
  - `☕` - Need a break

### Card
Represents a single card with value checking and numeric conversion.

### Deck
A collection of all Planning Poker cards, with methods to retrieve specific cards or filter numeric ones.

### Player
Represents a participant, either an estimator or an observer. Observers can watch but not estimate.

### Story
Represents a user story with:
- ID, title, description
- Acceptance criteria
- Final estimate (once consensus is reached)

### Round
Manages a single estimation round:
- Tracks player estimates
- State management (presenting, estimating, revealed, discussing, completed)
- Consensus checking
- Statistical analysis
- Support for re-voting

### Session
Orchestrates the entire Planning Poker session:
- Player management
- Story backlog
- Round lifecycle
- Session summary and statistics

## 🎮 Typical Workflow

1. **Setup**: Create session and add players
2. **Present**: Share story details with the team
3. **Estimate**: Players independently select cards
4. **Reveal**: All cards shown simultaneously
5. **Discuss**: Team talks about differences, especially outliers
6. **Consensus**: Check if estimates are close enough
7. **Revote**: If needed, discuss and re-estimate
8. **Finalize**: Record the agreed-upon estimate

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest test_poker_mechanics.py -v

# Run specific test class
pytest test_poker_mechanics.py::TestSession -v

# Run with coverage
pytest test_poker_mechanics.py --cov=poker_mechanics
```

Tests cover:
- ✅ Card and deck functionality
- ✅ Player and observer roles
- ✅ Round state transitions
- ✅ Estimate submission and validation
- ✅ Consensus checking
- ✅ Statistical calculations
- ✅ Complete workflow scenarios

## 🔍 Key Features

### Consensus Detection
Automatically checks if team estimates are close enough (configurable threshold):

```python
has_consensus = round.has_consensus(max_difference=3)
```

### Outlier Identification
Finds players with highest and lowest estimates for discussion:

```python
lowest, highest = round.get_outliers()
```

### Statistical Analysis
Calculate range, average, and other metrics:

```python
min_val, max_val = round.get_estimate_range()
average = round.calculate_average()
```

### Re-voting Support
Easy to restart voting after discussion:

```python
round.start_discussion()
round.start_revote()
```

### Observer Role
Product owners or stakeholders can observe without influencing estimates:

```python
observer = Player(id="po", name="Product Owner", is_observer=True)
```

## 💡 Best Practices

1. **Use Reference Stories**: Calibrate estimates against previously completed stories
2. **Time-box Discussions**: Keep conversations focused and efficient
3. **Listen to Outliers**: Highest and lowest estimates often reveal important insights
4. **Avoid Anchoring**: Reveal cards simultaneously to prevent bias
5. **Keep it Light**: Planning Poker should be engaging and collaborative

## 🤝 Contributing

This is a demonstration implementation of Planning Poker mechanics. Contributions are welcome!

## 📄 License

This project is open source and available for educational and commercial use.

## 🔗 Resources

- [Planning Poker on Wikipedia](https://en.wikipedia.org/wiki/Planning_poker)
- [Scrum Alliance on Estimation](https://www.scrumalliance.org/)
- [Agile Estimation Techniques](https://www.atlassian.com/agile/project-management/estimation)

---

**Note**: This implementation focuses on the core mechanics of Planning Poker. For a production-ready application, consider adding:
- Web interface (React, Vue, etc.)
- Real-time synchronization (WebSockets)
- Database persistence
- User authentication
- Session history and analytics