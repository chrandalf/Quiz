"""
Example Usage of Planning Poker Mechanics
==========================================
This script demonstrates how to use the Planning Poker mechanics
in a typical estimation session.
"""

from poker_mechanics import (
    Session, Player, Story, CardValue, RoundState
)


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 60 + "\n")


def demo_planning_poker():
    """Demonstrate a complete Planning Poker session."""
    
    print("🃏 Planning Poker Demo - Sprint 23 Estimation Session")
    print_separator()
    
    # 1. Create a session
    print("1️⃣  Creating session...")
    session = Session(id="sprint-23", name="Sprint 23 Planning")
    print(f"   ✓ Session '{session.name}' created")
    
    # 2. Add players
    print("\n2️⃣  Adding team members...")
    alice = Player(id="alice", name="Alice (Backend Dev)")
    bob = Player(id="bob", name="Bob (Frontend Dev)")
    charlie = Player(id="charlie", name="Charlie (QA)")
    observer = Player(id="po", name="Product Owner", is_observer=True)
    
    for player in [alice, bob, charlie, observer]:
        session.add_player(player)
        role = "Observer" if player.is_observer else "Estimator"
        print(f"   ✓ {player.name} joined as {role}")
    
    # 3. Add stories to estimate
    print("\n3️⃣  Adding user stories...")
    story1 = Story(
        id="US-101",
        title="User Authentication",
        description="Implement user login with email and password",
        acceptance_criteria=[
            "Users can log in with valid credentials",
            "Invalid credentials show error message",
            "Session persists for 24 hours",
            "Logout functionality works"
        ]
    )
    
    story2 = Story(
        id="US-102",
        title="Password Reset",
        description="Allow users to reset forgotten passwords",
        acceptance_criteria=[
            "User receives reset email",
            "Reset link expires after 1 hour",
            "New password must meet security requirements"
        ]
    )
    
    session.add_story(story1)
    session.add_story(story2)
    print(f"   ✓ Added {len(session.stories)} stories to backlog")
    
    print_separator()
    
    # 4. Estimate first story
    print(f"📖 Estimating Story: {story1}")
    print(f"   Description: {story1.description}")
    print(f"   Acceptance Criteria:")
    for i, criteria in enumerate(story1.acceptance_criteria, 1):
        print(f"      {i}. {criteria}")
    
    print("\n4️⃣  Starting estimation round...")
    session.start_round(story1)
    print(f"   ✓ Round started, state: {session.current_round.state.value}")
    
    # 5. Players submit estimates
    print("\n5️⃣  Team members selecting cards...")
    session.submit_estimate(alice, CardValue.EIGHT)
    print(f"   ✓ {alice.name} selected a card")
    
    session.submit_estimate(bob, CardValue.THIRTEEN)
    print(f"   ✓ {bob.name} selected a card")
    
    session.submit_estimate(charlie, CardValue.FIVE)
    print(f"   ✓ {charlie.name} selected a card")
    
    # 6. Reveal estimates
    print("\n6️⃣  Revealing cards...")
    session.reveal_estimates()
    print(f"   Cards revealed!")
    print(f"\n   📊 Estimates:")
    for player, card in session.current_round.estimates.items():
        print(f"      • {player.name}: {card}")
    
    # 7. Analyze estimates
    print("\n7️⃣  Analyzing estimates...")
    min_val, max_val = session.current_round.get_estimate_range()
    print(f"   Range: {min_val} - {max_val} (difference: {max_val - min_val})")
    
    avg = session.current_round.calculate_average()
    print(f"   Average: {avg:.1f}")
    
    lowest, highest = session.current_round.get_outliers()
    print(f"\n   🔍 Outliers for discussion:")
    print(f"      Lowest ({min_val}): {', '.join(e.player.name for e in lowest)}")
    print(f"      Highest ({max_val}): {', '.join(e.player.name for e in highest)}")
    
    has_consensus = session.current_round.has_consensus(max_difference=5)
    print(f"\n   Consensus reached: {'✓ Yes' if has_consensus else '✗ No'}")
    
    # 8. Discussion and revote (simulated)
    if not has_consensus:
        print("\n8️⃣  Team discusses differences...")
        print("   💬 Bob: 'I think we need more time for backend integration'")
        print("   💬 Charlie: 'The testing might be simpler than I thought'")
        print("   💬 Alice: 'Good point, let's revote'")
        
        print("\n   Starting revote...")
        session.current_round.start_discussion()
        session.current_round.start_revote()
        
        # Revote
        session.submit_estimate(alice, CardValue.EIGHT)
        session.submit_estimate(bob, CardValue.EIGHT)
        session.submit_estimate(charlie, CardValue.EIGHT)
        
        session.reveal_estimates()
        print(f"\n   📊 Revote Estimates:")
        for player, card in session.current_round.estimates.items():
            print(f"      • {player.name}: {card}")
        
        has_consensus = session.current_round.has_consensus(max_difference=3)
        print(f"\n   Consensus reached: {'✓ Yes' if has_consensus else '✗ No'}")
    
    # 9. Finalize estimate
    print("\n9️⃣  Finalizing estimate...")
    final_estimate = 8
    session.finalize_round(final_estimate)
    print(f"   ✓ Story {story1.id} estimated at {final_estimate} story points")
    
    print_separator()
    
    # 10. Session summary
    print("📈 Session Summary:")
    summary = session.get_session_summary()
    print(f"   Session: {summary['name']}")
    print(f"   Players: {summary['players']}")
    print(f"   Stories Estimated: {summary['stories_estimated']}")
    print(f"   Stories Pending: {summary['stories_pending']}")
    
    print("\n   Completed Stories:")
    for round in session.completed_rounds:
        print(f"      • {round.story.id}: {round.story.title} → {round.story.final_estimate} points")
    
    print_separator()
    print("✅ Planning Poker session completed successfully!")
    print("\n💡 Key Benefits:")
    print("   • Team collaboration and shared understanding")
    print("   • Reduced estimation bias")
    print("   • Identification of risks and unknowns")
    print("   • Improved accuracy through group wisdom")


if __name__ == "__main__":
    demo_planning_poker()
