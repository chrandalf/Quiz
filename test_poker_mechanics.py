"""
Tests for Planning Poker Mechanics
"""

import pytest
from datetime import datetime
from poker_mechanics import (
    Card, CardValue, Deck, Player, Estimate, Story, Round, RoundState, Session
)


class TestCard:
    """Tests for Card class."""
    
    def test_card_creation(self):
        """Test creating a card."""
        card = Card(CardValue.FIVE)
        assert card.value == CardValue.FIVE
        assert str(card) == "5"
    
    def test_numeric_card(self):
        """Test numeric card properties."""
        card = Card(CardValue.EIGHT)
        assert card.is_numeric() is True
        assert card.get_numeric_value() == 8
    
    def test_special_card(self):
        """Test special card properties."""
        card = Card(CardValue.QUESTION)
        assert card.is_numeric() is False
        assert card.get_numeric_value() is None


class TestDeck:
    """Tests for Deck class."""
    
    def test_deck_initialization(self):
        """Test deck is initialized with all cards."""
        deck = Deck()
        assert len(deck.cards) == len(CardValue)
    
    def test_get_card(self):
        """Test getting a specific card from deck."""
        deck = Deck()
        card = deck.get_card(CardValue.THIRTEEN)
        assert card is not None
        assert card.value == CardValue.THIRTEEN
    
    def test_get_numeric_cards(self):
        """Test getting only numeric cards."""
        deck = Deck()
        numeric_cards = deck.get_numeric_cards()
        assert all(card.is_numeric() for card in numeric_cards)
        assert len(numeric_cards) == 10  # 0, 1, 2, 3, 5, 8, 13, 20, 40, 100


class TestPlayer:
    """Tests for Player class."""
    
    def test_player_creation(self):
        """Test creating a player."""
        player = Player(id="p1", name="Alice")
        assert player.id == "p1"
        assert player.name == "Alice"
        assert player.is_observer is False
    
    def test_observer_creation(self):
        """Test creating an observer."""
        observer = Player(id="o1", name="Bob", is_observer=True)
        assert observer.is_observer is True


class TestStory:
    """Tests for Story class."""
    
    def test_story_creation(self):
        """Test creating a story."""
        story = Story(
            id="US-123",
            title="User login feature",
            description="As a user, I want to log in",
            acceptance_criteria=["Valid credentials accepted", "Invalid credentials rejected"]
        )
        assert story.id == "US-123"
        assert story.title == "User login feature"
        assert len(story.acceptance_criteria) == 2
        assert story.final_estimate is None


class TestRound:
    """Tests for Round class."""
    
    @pytest.fixture
    def story(self):
        """Create a test story."""
        return Story(id="US-1", title="Test Story", description="Test")
    
    @pytest.fixture
    def players(self):
        """Create test players."""
        return [
            Player(id="p1", name="Alice"),
            Player(id="p2", name="Bob"),
            Player(id="p3", name="Charlie")
        ]
    
    @pytest.fixture
    def round(self, story):
        """Create a test round."""
        return Round(story=story, state=RoundState.ESTIMATING)
    
    def test_round_creation(self, story):
        """Test creating a round."""
        round = Round(story=story)
        assert round.story == story
        assert round.state == RoundState.PRESENTING
        assert round.round_number == 1
    
    def test_add_estimate(self, round, players):
        """Test adding an estimate."""
        card = Card(CardValue.FIVE)
        round.add_estimate(players[0], card)
        assert players[0] in round.estimates
        assert round.estimates[players[0]] == card
    
    def test_observer_cannot_estimate(self, round):
        """Test that observers cannot provide estimates."""
        observer = Player(id="o1", name="Observer", is_observer=True)
        card = Card(CardValue.FIVE)
        with pytest.raises(ValueError, match="Observers cannot provide estimates"):
            round.add_estimate(observer, card)
    
    def test_reveal_cards(self, round, players):
        """Test revealing cards."""
        round.add_estimate(players[0], Card(CardValue.FIVE))
        round.add_estimate(players[1], Card(CardValue.EIGHT))
        round.reveal_cards()
        assert round.state == RoundState.REVEALED
    
    def test_get_numeric_estimates(self, round, players):
        """Test getting numeric estimates."""
        round.add_estimate(players[0], Card(CardValue.FIVE))
        round.add_estimate(players[1], Card(CardValue.EIGHT))
        round.add_estimate(players[2], Card(CardValue.QUESTION))
        
        numeric = round.get_numeric_estimates()
        assert len(numeric) == 2
        assert 5 in numeric
        assert 8 in numeric
    
    def test_get_estimate_range(self, round, players):
        """Test getting estimate range."""
        round.add_estimate(players[0], Card(CardValue.TWO))
        round.add_estimate(players[1], Card(CardValue.EIGHT))
        round.add_estimate(players[2], Card(CardValue.FIVE))
        
        min_val, max_val = round.get_estimate_range()
        assert min_val == 2
        assert max_val == 8
    
    def test_get_outliers(self, round, players):
        """Test getting outliers."""
        round.add_estimate(players[0], Card(CardValue.TWO))
        round.add_estimate(players[1], Card(CardValue.EIGHT))
        round.add_estimate(players[2], Card(CardValue.FIVE))
        
        lowest, highest = round.get_outliers()
        assert len(lowest) == 1
        assert lowest[0].player == players[0]
        assert len(highest) == 1
        assert highest[0].player == players[1]
    
    def test_has_consensus_true(self, round, players):
        """Test consensus check when estimates are close."""
        round.add_estimate(players[0], Card(CardValue.FIVE))
        round.add_estimate(players[1], Card(CardValue.FIVE))
        round.add_estimate(players[2], Card(CardValue.EIGHT))
        
        assert round.has_consensus(max_difference=3) is True
    
    def test_has_consensus_false(self, round, players):
        """Test consensus check when estimates are far apart."""
        round.add_estimate(players[0], Card(CardValue.TWO))
        round.add_estimate(players[1], Card(CardValue.TWENTY))
        
        assert round.has_consensus(max_difference=3) is False
    
    def test_calculate_average(self, round, players):
        """Test calculating average estimate."""
        round.add_estimate(players[0], Card(CardValue.TWO))
        round.add_estimate(players[1], Card(CardValue.EIGHT))
        round.add_estimate(players[2], Card(CardValue.FIVE))
        
        avg = round.calculate_average()
        assert avg == 5.0  # (2 + 8 + 5) / 3
    
    def test_complete_round(self, round):
        """Test completing a round."""
        round.complete_round(8)
        assert round.state == RoundState.COMPLETED
        assert round.story.final_estimate == 8
    
    def test_start_revote(self, round, players):
        """Test starting a revote."""
        round.add_estimate(players[0], Card(CardValue.FIVE))
        round.reveal_cards()
        round.start_discussion()
        round.start_revote()
        
        assert round.state == RoundState.ESTIMATING
        assert round.round_number == 2
        assert len(round.estimates) == 0
    
    def test_all_players_estimated(self, round, players):
        """Test checking if all players have estimated."""
        active_players = set(players)
        
        # Not all estimated yet
        round.add_estimate(players[0], Card(CardValue.FIVE))
        assert round.all_players_estimated(active_players) is False
        
        # All estimated
        round.add_estimate(players[1], Card(CardValue.EIGHT))
        round.add_estimate(players[2], Card(CardValue.FIVE))
        assert round.all_players_estimated(active_players) is True


class TestSession:
    """Tests for Session class."""
    
    @pytest.fixture
    def session(self):
        """Create a test session."""
        return Session(id="s1", name="Sprint Planning")
    
    @pytest.fixture
    def players(self):
        """Create test players."""
        return [
            Player(id="p1", name="Alice"),
            Player(id="p2", name="Bob"),
            Player(id="p3", name="Charlie")
        ]
    
    @pytest.fixture
    def story(self):
        """Create a test story."""
        return Story(id="US-1", title="Test Story", description="Test")
    
    def test_session_creation(self):
        """Test creating a session."""
        session = Session(id="s1", name="Sprint Planning")
        assert session.id == "s1"
        assert session.name == "Sprint Planning"
        assert len(session.players) == 0
        assert session.current_round is None
    
    def test_add_player(self, session, players):
        """Test adding players."""
        session.add_player(players[0])
        session.add_player(players[1])
        assert len(session.players) == 2
        assert players[0] in session.players
    
    def test_remove_player(self, session, players):
        """Test removing players."""
        session.add_player(players[0])
        session.add_player(players[1])
        session.remove_player(players[0])
        assert len(session.players) == 1
        assert players[0] not in session.players
    
    def test_add_story(self, session, story):
        """Test adding a story."""
        session.add_story(story)
        assert len(session.stories) == 1
        assert story in session.stories
    
    def test_start_round(self, session, story):
        """Test starting a round."""
        round = session.start_round(story)
        assert session.current_round == round
        assert round.story == story
        assert round.state == RoundState.ESTIMATING
    
    def test_cannot_start_round_while_active(self, session, story):
        """Test that cannot start new round while one is active."""
        session.start_round(story)
        story2 = Story(id="US-2", title="Story 2", description="Test")
        
        with pytest.raises(ValueError, match="Cannot start new round"):
            session.start_round(story2)
    
    def test_submit_estimate(self, session, players, story):
        """Test submitting an estimate."""
        session.add_player(players[0])
        session.start_round(story)
        session.submit_estimate(players[0], CardValue.FIVE)
        
        assert players[0] in session.current_round.estimates
        assert session.current_round.estimates[players[0]].value == CardValue.FIVE
    
    def test_submit_estimate_invalid_player(self, session, players, story):
        """Test submitting estimate from player not in session."""
        session.start_round(story)
        
        with pytest.raises(ValueError, match="Player not in session"):
            session.submit_estimate(players[0], CardValue.FIVE)
    
    def test_reveal_estimates(self, session, players, story):
        """Test revealing estimates."""
        session.add_player(players[0])
        session.add_player(players[1])
        session.start_round(story)
        session.submit_estimate(players[0], CardValue.FIVE)
        session.submit_estimate(players[1], CardValue.EIGHT)
        session.reveal_estimates()
        
        assert session.current_round.state == RoundState.REVEALED
    
    def test_finalize_round(self, session, players, story):
        """Test finalizing a round."""
        session.add_player(players[0])
        session.start_round(story)
        session.submit_estimate(players[0], CardValue.FIVE)
        session.reveal_estimates()
        session.finalize_round(5)
        
        assert session.current_round is None
        assert len(session.completed_rounds) == 1
        assert session.completed_rounds[0].story.final_estimate == 5
    
    def test_get_session_summary(self, session, players, story):
        """Test getting session summary."""
        session.add_player(players[0])
        session.add_player(players[1])
        session.add_story(story)
        
        summary = session.get_session_summary()
        assert summary["session_id"] == "s1"
        assert summary["name"] == "Sprint Planning"
        assert summary["players"] == 2
        assert summary["stories_estimated"] == 0
        assert summary["stories_pending"] == 1
    
    def test_full_estimation_workflow(self, session, players, story):
        """Test a complete estimation workflow."""
        # Setup session
        for player in players:
            session.add_player(player)
        session.add_story(story)
        
        # Start round
        session.start_round(story)
        assert session.current_round.state == RoundState.ESTIMATING
        
        # Players submit estimates
        session.submit_estimate(players[0], CardValue.FIVE)
        session.submit_estimate(players[1], CardValue.EIGHT)
        session.submit_estimate(players[2], CardValue.FIVE)
        
        # Reveal cards
        session.reveal_estimates()
        assert session.current_round.state == RoundState.REVEALED
        
        # Check estimates
        min_val, max_val = session.current_round.get_estimate_range()
        assert min_val == 5
        assert max_val == 8
        
        # Consensus reached, finalize
        avg = session.current_round.calculate_average()
        assert avg == 6.0
        
        session.finalize_round(5)
        assert story.final_estimate == 5
        assert len(session.completed_rounds) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
