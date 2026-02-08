"""
Planning Poker Mechanics
========================
Implementation of Planning Poker (Scrum Poker) for Agile estimation.

Planning Poker is a consensus-based technique for estimating effort or complexity
of user stories in Agile development.
"""

from enum import Enum
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime


class CardValue(Enum):
    """Standard Planning Poker card values using Fibonacci sequence."""
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    EIGHT = 8
    THIRTEEN = 13
    TWENTY = 20
    FORTY = 40
    HUNDRED = 100
    QUESTION = "?"  # Uncertain/need more information
    INFINITY = "∞"  # Too large to estimate
    COFFEE = "☕"  # Need a break


@dataclass
class Card:
    """Represents a single Planning Poker card."""
    value: CardValue
    
    def __str__(self) -> str:
        return str(self.value.value)
    
    def __repr__(self) -> str:
        return f"Card({self.value.name})"
    
    def is_numeric(self) -> bool:
        """Check if card has a numeric value."""
        return isinstance(self.value.value, int)
    
    def get_numeric_value(self) -> Optional[int]:
        """Get numeric value if card is numeric, None otherwise."""
        return self.value.value if self.is_numeric() else None


@dataclass
class Deck:
    """Represents a deck of Planning Poker cards."""
    cards: List[Card] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize standard deck if empty."""
        if not self.cards:
            self.cards = [Card(value) for value in CardValue]
    
    def get_card(self, value: CardValue) -> Optional[Card]:
        """Get a specific card from the deck."""
        for card in self.cards:
            if card.value == value:
                return card
        return None
    
    def get_numeric_cards(self) -> List[Card]:
        """Get only numeric cards from the deck."""
        return [card for card in self.cards if card.is_numeric()]


@dataclass
class Player:
    """Represents a player in the Planning Poker session."""
    id: str
    name: str
    is_observer: bool = False
    
    def __str__(self) -> str:
        role = "Observer" if self.is_observer else "Player"
        return f"{self.name} ({role})"
    
    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Estimate:
    """Represents a player's estimate for a story."""
    player: Player
    card: Card
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.player.name}: {self.card}"


@dataclass
class Story:
    """Represents a user story to be estimated."""
    id: str
    title: str
    description: str
    acceptance_criteria: List[str] = field(default_factory=list)
    final_estimate: Optional[int] = None
    
    def __str__(self) -> str:
        return f"Story {self.id}: {self.title}"


class RoundState(Enum):
    """States of an estimation round."""
    PRESENTING = "presenting"  # Story is being presented
    ESTIMATING = "estimating"  # Players are selecting cards
    REVEALED = "revealed"  # Cards have been revealed
    DISCUSSING = "discussing"  # Team is discussing estimates
    COMPLETED = "completed"  # Consensus reached


@dataclass
class Round:
    """Represents a single estimation round for a story."""
    story: Story
    estimates: Dict[Player, Optional[Card]] = field(default_factory=dict)
    state: RoundState = RoundState.PRESENTING
    round_number: int = 1
    
    def add_estimate(self, player: Player, card: Card) -> None:
        """Add or update a player's estimate."""
        if player.is_observer:
            raise ValueError("Observers cannot provide estimates")
        self.estimates[player] = card
    
    def reveal_cards(self) -> None:
        """Reveal all cards."""
        if self.state != RoundState.ESTIMATING:
            raise ValueError(f"Cannot reveal cards in {self.state.value} state")
        self.state = RoundState.REVEALED
    
    def start_discussion(self) -> None:
        """Start discussion phase."""
        if self.state != RoundState.REVEALED:
            raise ValueError(f"Cannot start discussion from {self.state.value} state")
        self.state = RoundState.DISCUSSING
    
    def start_revote(self) -> None:
        """Start a new voting round."""
        self.estimates.clear()
        self.round_number += 1
        self.state = RoundState.ESTIMATING
    
    def get_numeric_estimates(self) -> List[int]:
        """Get all numeric estimates."""
        numeric_estimates = []
        for card in self.estimates.values():
            if card and card.is_numeric():
                value = card.get_numeric_value()
                if value is not None:
                    numeric_estimates.append(value)
        return numeric_estimates
    
    def get_estimate_range(self) -> tuple[Optional[int], Optional[int]]:
        """Get min and max estimates."""
        numeric_estimates = self.get_numeric_estimates()
        if not numeric_estimates:
            return None, None
        return min(numeric_estimates), max(numeric_estimates)
    
    def get_outliers(self) -> tuple[List[Estimate], List[Estimate]]:
        """Get players with highest and lowest estimates."""
        numeric_estimates = self.get_numeric_estimates()
        if not numeric_estimates:
            return [], []
        
        min_val, max_val = min(numeric_estimates), max(numeric_estimates)
        
        lowest = [
            Estimate(player, card)
            for player, card in self.estimates.items()
            if card and card.get_numeric_value() == min_val
        ]
        highest = [
            Estimate(player, card)
            for player, card in self.estimates.items()
            if card and card.get_numeric_value() == max_val
        ]
        
        return lowest, highest
    
    def has_consensus(self, max_difference: int = 3) -> bool:
        """Check if consensus has been reached."""
        min_val, max_val = self.get_estimate_range()
        if min_val is None or max_val is None:
            return False
        return (max_val - min_val) <= max_difference
    
    def calculate_average(self) -> Optional[float]:
        """Calculate average of numeric estimates."""
        numeric_estimates = self.get_numeric_estimates()
        if not numeric_estimates:
            return None
        return sum(numeric_estimates) / len(numeric_estimates)
    
    def complete_round(self, final_estimate: int) -> None:
        """Complete the round with a final estimate."""
        self.story.final_estimate = final_estimate
        self.state = RoundState.COMPLETED
    
    def all_players_estimated(self, active_players: Set[Player]) -> bool:
        """Check if all active (non-observer) players have estimated."""
        estimating_players = {p for p in active_players if not p.is_observer}
        estimated_players = {p for p in self.estimates.keys() if not p.is_observer}
        return estimating_players == estimated_players


@dataclass
class Session:
    """Represents a Planning Poker session."""
    id: str
    name: str
    deck: Deck = field(default_factory=Deck)
    players: Set[Player] = field(default_factory=set)
    stories: List[Story] = field(default_factory=list)
    current_round: Optional[Round] = None
    completed_rounds: List[Round] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_player(self, player: Player) -> None:
        """Add a player to the session."""
        self.players.add(player)
    
    def remove_player(self, player: Player) -> None:
        """Remove a player from the session."""
        self.players.discard(player)
    
    def add_story(self, story: Story) -> None:
        """Add a story to the backlog."""
        self.stories.append(story)
    
    def start_round(self, story: Story) -> Round:
        """Start a new estimation round for a story."""
        if self.current_round and self.current_round.state != RoundState.COMPLETED:
            raise ValueError("Cannot start new round while another is in progress")
        
        self.current_round = Round(story=story, state=RoundState.ESTIMATING)
        return self.current_round
    
    def submit_estimate(self, player: Player, card_value: CardValue) -> None:
        """Submit an estimate for the current round."""
        if not self.current_round:
            raise ValueError("No active round")
        
        if player not in self.players:
            raise ValueError("Player not in session")
        
        card = self.deck.get_card(card_value)
        if not card:
            raise ValueError(f"Invalid card value: {card_value}")
        
        self.current_round.add_estimate(player, card)
    
    def reveal_estimates(self) -> None:
        """Reveal all estimates for the current round."""
        if not self.current_round:
            raise ValueError("No active round")
        self.current_round.reveal_cards()
    
    def finalize_round(self, final_estimate: int) -> None:
        """Finalize the current round with a consensus estimate."""
        if not self.current_round:
            raise ValueError("No active round")
        
        self.current_round.complete_round(final_estimate)
        self.completed_rounds.append(self.current_round)
        self.current_round = None
    
    def get_session_summary(self) -> Dict:
        """Get a summary of the session."""
        return {
            "session_id": self.id,
            "name": self.name,
            "players": len(self.players),
            "stories_estimated": len([r for r in self.completed_rounds]),
            "stories_pending": len(self.stories) - len(self.completed_rounds),
            "created_at": self.created_at.isoformat()
        }
