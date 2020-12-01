from typing import List, Tuple

from poker import Card, Hand, best_possible_hand

HoleCards = Tuple[Card, Card]

CHAIN = '⛓'
WEB = '🕸'
KEY = '🔑'
LOCK = '🔒'

# Tests that two pairs of hole cards with given community cards are ranked correctly
# expected is the expected result. 1 means hand1 should win, 2 means hand2 should win
# 0 means the two hands should tie
def test_ranking(public: List[Card], hand1: HoleCards, hand2: HoleCards, expected: int) -> bool:
    best_hand1 = best_possible_hand(public, hand1)
    best_hand2 = best_possible_hand(public, hand2)
    if best_hand1 == best_hand2:
        winner = 0
    elif best_hand1 > best_hand2:
        winner = 1
    else:
        winner = 2
    if winner == expected:
        return True
    expected_strs = ["a tie", "hand 1 to win", "hand 2 to win"]
    actualstrs = ["the two hands tied", "hand 1 won", "hand 2 won"]
    print("Test failed! Expected", expected_strs[expected], "but", actualstrs[winner])
    print("Shared cards:",  " ".join(str(card) for card in public))
    print("Hole cards 1: ", " ".join(str(card) for card in hand1))
    print("Hole cards 2: ", " ".join(str(card) for card in hand2))
    print("Hand 1: ", " ".join(str(card) for card in best_hand1.cards))
    print("Hand 2: ", " ".join(str(card) for card in best_hand2.cards))
    print("")
    return False

# Tests a list of test cases to see that the hands will be ranked appropriately
def test_rankings(hands: List[Tuple[List[Card], HoleCards, HoleCards, int]]):
    print("Testing hand rankings:")
    tests_passed = 0
    for hand in hands:
        if test_ranking(*hand):
            tests_passed += 1
    print(f"{tests_passed} out of {len(hands)} tests passed!")
    print("")

# Tests that the description for the hands are correct
def test_hand_descriptions(test_cases: List[Tuple[Hand, str]]):
    print("Testing hand descriptions:")
    tests_passed = 0
    for hand, description in test_cases:
        if str(hand) == description:
            tests_passed += 1
        else:
            print(f"Test failed! Expected '{description}', but got {str(hand)}!")
            print("Hand: ", " ".join(str(card) for card in hand.cards))
            print("")
    print(f"{tests_passed} out of {len(test_cases)} tests passed!")
    print("")

test_rankings([
    # Testing that a high card beats a less-high card
    ([Card(CHAIN, '9'), Card(LOCK, '4'), Card(WEB, '5'), Card(CHAIN, '6'), Card(WEB, '7')],
     (Card(LOCK, 'K'), Card(LOCK, 'Q')),
     (Card(LOCK, 'A'), Card(LOCK, '2')),
     2),

    # The next highest card decides it if the first highest cards tie
    ([Card(CHAIN, 'J'), Card(LOCK, '2'), Card(WEB, '5'), Card(CHAIN, '9'), Card(WEB, '10')],
     (Card(LOCK, 'A'), Card(LOCK, '8')),
     (Card(KEY, 'A'), Card(LOCK, '7')),
     1),

    # If the board beats all the hole cards, the two players should tie
    ([Card(CHAIN, 'J'), Card(LOCK, '10'), Card(WEB, '9'), Card(CHAIN, '8'), Card(WEB, '6')],
     (Card(LOCK, '5'), Card(LOCK, '4')),
     (Card(LOCK, '3'), Card(LOCK, '2')),
     0),

    # A pair beats a high card
    ([Card(CHAIN, '2'), Card(LOCK, '4'), Card(WEB, '5'), Card(KEY, '6'), Card(LOCK, '7')],
     (Card(LOCK, '2'), Card(LOCK, '3')),
     (Card(LOCK, 'A'), Card(LOCK, 'K')),
     1),

    # A high pair beats a low pair
    ([Card(CHAIN, '2'), Card(KEY, '3'), Card(WEB, '5'), Card(KEY, '6'), Card(LOCK, '7')],
     (Card(LOCK, '2'), Card(LOCK, 'A')),
     (Card(LOCK, '3'), Card(LOCK, '4')),
     2),

    # The pair with a higher kicker beats the same pair with a worse kicker
    ([Card(CHAIN, '2'), Card(LOCK, '4'), Card(WEB, '5'), Card(KEY, '6'), Card(LOCK, '7')],
     (Card(LOCK, '2'), Card(LOCK, 'A')),
     (Card(WEB, '2'), Card(LOCK, 'K')),
     1),

    # The kicker for pairs doesn't matter if they're both too low
    ([Card(CHAIN, '2'), Card(LOCK, 'K'), Card(WEB, 'Q'), Card(KEY, 'J'), Card(LOCK, '7')],
     (Card(KEY, 'K'), Card(LOCK, '3')),
     (Card(CHAIN, 'K'), Card(LOCK, '6')),
     0),

    # Two pair beats one pair
    ([Card(CHAIN, '2'), Card(LOCK, '3'), Card(WEB, '5'), Card(KEY, '6'), Card(LOCK, '7')],
     (Card(KEY, '2'), Card(CHAIN, '3')),
     (Card(LOCK, 'A'), Card(KEY, 'A')),
     1),

    # The higher pair for a two pair decides which one wins
    ([Card(CHAIN, '2'), Card(LOCK, '4'), Card(WEB, '5'), Card(KEY, '6'), Card(LOCK, '7')],
     (Card(LOCK, '5'), Card(CHAIN, '6')),
     (Card(LOCK, '2'), Card(CHAIN, '7')),
     2),

    # The second pair can decide for two tied two pairs
    ([Card(LOCK, '2'), Card(CHAIN, '4'), Card(KEY, '6'), Card(WEB, '8'), Card(LOCK, '10')],
     (Card(CHAIN, '10'), Card(LOCK, '4')),
     (Card(WEB, '10'), Card(CHAIN, '2')),
     1),

    # The kicker can decide it who wins if both players have the same two pair
    ([Card(LOCK, 'K'), Card(CHAIN, '9'), Card(WEB, '9'), Card(KEY, '3'), Card(CHAIN, '2')],
     (Card(CHAIN, 'K'), Card(LOCK, '4')),
     (Card(WEB, 'K'), Card(LOCK, '5')),
     2),

    # Two pairs can tie if the two pairs are the same and the kickers are too low
    ([Card(LOCK, 'K'), Card(CHAIN, '9'), Card(WEB, '9'), Card(KEY, '5'), Card(CHAIN, '2')],
     (Card(CHAIN, 'K'), Card(LOCK, '4')),
     (Card(WEB, 'K'), Card(LOCK, '3')),
     0),

    # Three-of-a-kind beats a pair
    ([Card(CHAIN, '2'), Card(CHAIN, 'A'), Card(LOCK, '10'), Card(WEB, 'J'), Card(KEY, '6')],
     (Card(LOCK, '2'), Card(WEB, '2')),
     (Card(KEY, 'A'), Card(LOCK, 'K')),
     1),

    # Three-of-a-kind beats two pair
    ([Card(CHAIN, '2'), Card(CHAIN, 'A'), Card(LOCK, '10'), Card(WEB, 'K'), Card(KEY, '6')],
     (Card(KEY, 'A'), Card(LOCK, 'K')),
     (Card(LOCK, '2'), Card(WEB, '2')),
     2),

    # A higher three-of-a-kind beats a lower three-of-a-kind
    ([Card(LOCK, 'K'), Card(CHAIN, 'Q'), Card(WEB, '5'), Card(WEB, '4'), Card(WEB, '3')],
     (Card(CHAIN, 'K'), Card(WEB, 'K')),
     (Card(LOCK, 'Q'), Card(WEB, 'Q')),
     1),

    # A three-of-a-kind with a higher kicker beats the same three-of-a-kind with a lower
    ([Card(LOCK, '10'), Card(CHAIN, '10'), Card(WEB, 'J'), Card(KEY, '6'), Card(LOCK, '2')],
     (Card(KEY, '10'), Card(KEY, 'K')),
     (Card(WEB, '10'), Card(LOCK, 'A')),
     2),

    # Two three-of-a-kinds can tie with different kickers if the kickers are low enough
    ([Card(LOCK, '10'), Card(CHAIN, '10'), Card(WEB, 'J'), Card(KEY, '6'), Card(LOCK, 'K')],
     (Card(KEY, '10'), Card(KEY, '3')),
     (Card(WEB, '10'), Card(LOCK, '2')),
     0),

    # Staight beats a pair
    ([Card(LOCK, '10'), Card(CHAIN, '9'), Card(KEY, '8'), Card(WEB, '7'), Card(CHAIN, 'A')],
     (Card(LOCK, 'A'), Card(CHAIN, 'K')),
     (Card(LOCK, '6'), Card(LOCK, '2')),
     2),

    # Straight beats two pair
    ([Card(LOCK, '10'), Card(CHAIN, '9'), Card(KEY, '8'), Card(WEB, 'K'), Card(CHAIN, 'A')],
     (Card(LOCK, '6'), Card(LOCK, '7')),
     (Card(LOCK, 'A'), Card(CHAIN, 'K')),
     1),

    # Straight beats three-of-a-kind
    ([Card(LOCK, '10'), Card(CHAIN, '9'), Card(KEY, '8'), Card(WEB, 'A'), Card(CHAIN, 'A')],
     (Card(LOCK, 'A'), Card(CHAIN, 'K')),
     (Card(LOCK, '6'), Card(LOCK, '7')),
     2),

    # A higher straight beats a lower one
    ([Card(LOCK, '10'), Card(CHAIN, '9'), Card(KEY, '8'), Card(WEB, '7'), Card(CHAIN, 'A')],
     (Card(LOCK, 'J'), Card(CHAIN, '2')),
     (Card(LOCK, '6'), Card(LOCK, 'A')),
     1),

    # Straights can tie
    ([Card(LOCK, '10'), Card(CHAIN, '9'), Card(KEY, '8'), Card(WEB, '7'), Card(CHAIN, 'A')],
     (Card(LOCK, '6'), Card(CHAIN, '2')),
     (Card(CHAIN, '6'), Card(LOCK, 'A')),
     0),

    # Flush beats a pair
    ([Card(LOCK, '5'), Card(LOCK, '6'), Card(LOCK, '7'), Card(CHAIN, 'A'), Card(CHAIN, 'Q')],
     (Card(LOCK, '3'), Card(LOCK, '2')),
     (Card(WEB, 'A'), Card(WEB, 'K')),
     1),

    # Flush beats two pair
    ([Card(LOCK, '5'), Card(LOCK, '6'), Card(LOCK, '7'), Card(CHAIN, 'A'), Card(CHAIN, 'K')],
     (Card(LOCK, '3'), Card(LOCK, '2')),
     (Card(WEB, 'A'), Card(WEB, 'K')),
     1),

    # Flush beats three-of-a-kind
    ([Card(LOCK, '5'), Card(LOCK, '6'), Card(LOCK, '7'), Card(CHAIN, 'A'), Card(LOCK, 'K')],
     (Card(LOCK, '3'), Card(LOCK, '2')),
     (Card(WEB, 'A'), Card(KEY, 'A')),
     1),

    # Flush beats a straight
    ([Card(LOCK, '5'), Card(LOCK, '6'), Card(LOCK, '7'), Card(CHAIN, 'A'), Card(CHAIN, 'Q')],
     (Card(LOCK, '3'), Card(LOCK, '2')),
     (Card(WEB, '8'), Card(WEB, '9')),
     1),

    # Higher flush beats lower flush
    ([Card(CHAIN, '7'), Card(CHAIN, '4'), Card(CHAIN, '8'), Card(KEY, 'K'), Card(LOCK, 'K')],
     (Card(CHAIN, 'K'), Card(CHAIN, 'Q')),
     (Card(CHAIN, 'A'), Card(CHAIN, '2')),
     2),

    # Full house beats a pair
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(WEB, '3'), Card(KEY, 'Q'), Card(KEY, 'J')],
     (Card(WEB, '2'), Card(CHAIN, '3')),
     (Card(KEY, 'K'), Card(KEY, 'A')),
     1),

    # Full house beats two pair
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(WEB, '3'), Card(KEY, 'Q'), Card(KEY, 'A')],
     (Card(KEY, 'K'), Card(CHAIN, 'A')),
     (Card(WEB, '2'), Card(CHAIN, '3')),
     2),

    # Full house beats three-of-a-kind
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(WEB, '3'), Card(KEY, 'Q'), Card(KEY, 'A')],
     (Card(WEB, '2'), Card(CHAIN, '3')),
     (Card(KEY, 'K'), Card(KEY, '2')),
     1),

    # Full house beats a straight
    ([Card(CHAIN, '2'), Card(WEB, '2'), Card(LOCK, 'J'), Card(KEY, '10'), Card(CHAIN, 'Q')],
     (Card(CHAIN, 'A'), Card(CHAIN, 'K')),
     (Card(LOCK, '2'), Card(LOCK, 'Q')),
     2),

    # Full house beats a flush
    ([Card(CHAIN, '2'), Card(WEB, '2'), Card(CHAIN, 'J'), Card(KEY, '10'), Card(CHAIN, 'Q')],
     (Card(LOCK, '2'), Card(LOCK, 'Q')),
     (Card(CHAIN, 'A'), Card(CHAIN, 'K')),
     1),

    # Ties between full houses are decided by the three-of-a-kind
    ([Card(CHAIN, 'A'), Card(CHAIN, 'K'), Card(LOCK, 'J'), Card(WEB, 'J'), Card(KEY, '3')],
     (Card(LOCK, 'A'), Card(KEY, 'J')),
     (Card(LOCK, 'K'), Card(KEY, 'K')),
     2),

    # If the three-of-a-kinds of two full houses tie, then the pairs decide
    ([Card(CHAIN, 'A'), Card(LOCK, 'A'), Card(WEB, 'A'), Card(LOCK, 'J'), Card(LOCK, '10')],
     (Card(WEB, 'J'), Card(LOCK, '2')),
     (Card(WEB, '10'), Card(LOCK, 'K')),
     1),

    # Two full houses can tie when everything's the same rank
    ([Card(CHAIN, '3'), Card(LOCK, '3'), Card(WEB, '2'), Card(LOCK, '2'), Card(KEY, '4')],
     (Card(KEY, '3'), Card(CHAIN, 'A')),
     (Card(WEB, '3'), Card(LOCK, '5')),
     0),

    # Four of a kind beats a pair
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, 'A'), Card(WEB, 'J'), Card(KEY, '9')],
     (Card(KEY, '2'), Card(WEB, '2')),
     (Card(CHAIN, 'K'), Card(CHAIN, 'Q')),
     1),

    # Four of a kind beats two pair
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, 'A'), Card(WEB, 'J'), Card(KEY, '9')],
     (Card(KEY, '2'), Card(WEB, '2')),
     (Card(CHAIN, 'K'), Card(LOCK, 'A')),
     1),

    # Four of a kind beats three of a kind
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, 'Q'), Card(WEB, '2'), Card(KEY, '9')],
     (Card(KEY, '2'), Card(WEB, '3')),
     (Card(CHAIN, 'K'), Card(LOCK, 'A')),
     1),

    # Four of a kind beats a straight
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, 'Q'), Card(WEB, 'J'), Card(KEY, '10')],
     (Card(KEY, '2'), Card(WEB, '2')),
     (Card(CHAIN, 'K'), Card(LOCK, 'A')),
     1),

    # Four of a kind beats a flush
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, '7'), Card(WEB, 'J'), Card(CHAIN, '10')],
     (Card(KEY, '2'), Card(WEB, '2')),
     (Card(CHAIN, 'K'), Card(CHAIN, 'A')),
     1),

    # Four of a kind beats a full house
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, '7'), Card(WEB, 'J'), Card(KEY, 'A')],
     (Card(KEY, '2'), Card(WEB, '2')),
     (Card(KEY, '7'), Card(LOCK, '7')),
     1),

    # Ties between four of a kinds are decided by the kicker
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, '7'), Card(WEB, '2'), Card(KEY, '2')],
     (Card(KEY, 'K'), Card(WEB, 'Q')),
     (Card(CHAIN, '3'), Card(CHAIN, 'A')),
     2),

    # The kickers of four-of-a-kinds can tie
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, '7'), Card(WEB, '2'), Card(KEY, '2')],
     (Card(KEY, 'K'), Card(WEB, 'Q')),
     (Card(CHAIN, 'K'), Card(LOCK, 'K')),
     0),

    # The four-of-a-kind kickers might not be high enough to matter
    ([Card(CHAIN, '2'), Card(LOCK, '2'), Card(CHAIN, 'A'), Card(WEB, '2'), Card(KEY, '2')],
     (Card(KEY, 'K'), Card(WEB, 'Q')),
     (Card(CHAIN, '3'), Card(LOCK, '4')),
     0),

    # Straight flush beats a pair
    ([Card(CHAIN, '2'), Card(CHAIN, '3'), Card(CHAIN, '4'), Card(LOCK, 'A'), Card(LOCK, 'K')],
     (Card(CHAIN, '5'), Card(CHAIN, '6')),
     (Card(WEB, 'A'), Card(WEB, 'Q')),
     1),

    # Straight flush beats two pair
    ([Card(CHAIN, '2'), Card(CHAIN, '3'), Card(CHAIN, '4'), Card(LOCK, 'A'), Card(LOCK, 'K')],
     (Card(CHAIN, '5'), Card(CHAIN, '6')),
     (Card(WEB, 'A'), Card(WEB, 'K')),
     1),

    # Straight flush beats three-of-a-kind
    ([Card(CHAIN, '2'), Card(CHAIN, '3'), Card(CHAIN, '4'), Card(LOCK, 'A'), Card(LOCK, 'K')],
     (Card(CHAIN, '5'), Card(CHAIN, '6')),
     (Card(WEB, 'A'), Card(KEY, 'A')),
     1),

    # Straight flush beats straight
    ([Card(CHAIN, '2'), Card(CHAIN, '3'), Card(CHAIN, '4'), Card(LOCK, 'A'), Card(LOCK, 'K')],
     (Card(CHAIN, '5'), Card(CHAIN, 'A')),
     (Card(WEB, '5'), Card(WEB, '6')),
     1),

    # Straight flush beats flush
    ([Card(CHAIN, '2'), Card(CHAIN, '3'), Card(CHAIN, '4'), Card(LOCK, 'Q'), Card(LOCK, 'J')],
     (Card(CHAIN, '5'), Card(CHAIN, '6')),
     (Card(CHAIN, 'A'), Card(CHAIN, 'K')),
     1),

    # Straight flush beats full house
    ([Card(CHAIN, '2'), Card(CHAIN, '3'), Card(CHAIN, '4'), Card(LOCK, '2'), Card(LOCK, 'A')],
     (Card(CHAIN, '5'), Card(CHAIN, '6')),
     (Card(WEB, 'A'), Card(KEY, 'A')),
     1),

    # Higher straight flush beats a lower straight flush
    ([Card(CHAIN, 'Q'), Card(CHAIN, 'J'), Card(CHAIN, '10'), Card(LOCK, '2'), Card(WEB, '3')],
     (Card(CHAIN, 'K'), Card(CHAIN, 'A')),
     (Card(CHAIN, '9'), Card(CHAIN, '8')),
     1),

    # The same straight flush will tie with itself
    ([Card(CHAIN, 'A'), Card(CHAIN, '2'), Card(CHAIN, '3'), Card(CHAIN, '4'), Card(CHAIN, '5')],
     (Card(LOCK, '6'), Card(LOCK, '7')),
     (Card(WEB, 'A'), Card(LOCK, 'A')),
     0),
])

test_hand_descriptions([
    (Hand([Card(CHAIN, '2'),
           Card(WEB, '3'),
           Card(WEB, '4'),
           Card(WEB, '5'),
           Card(WEB, '7')]),
     "seven high"
    ),
    (Hand([Card(CHAIN, 'J'),
           Card(WEB, 'A'),
           Card(WEB, 'K'),
           Card(WEB, '10'),
           Card(WEB, '9')]),
     "ace high"
    ),
    (Hand([Card(CHAIN, '2'),
           Card(WEB, '2'),
           Card(WEB, '4'),
           Card(WEB, '5'),
           Card(WEB, '7')]),
     "pair of deuces"
    ),
    (Hand([Card(CHAIN, 'A'),
           Card(WEB, '6'),
           Card(WEB, 'K'),
           Card(WEB, 'Q'),
           Card(CHAIN, '6')]),
     "pair of sixes"
    ),
    (Hand([Card(CHAIN, '2'),
           Card(WEB, '6'),
           Card(WEB, '2'),
           Card(WEB, 'A'),
           Card(CHAIN, '6')]),
     "two pair, sixes and deuces"
    ),
    (Hand([Card(CHAIN, 'J'),
           Card(WEB, 'A'),
           Card(WEB, 'J'),
           Card(WEB, 'Q'),
           Card(CHAIN, 'A')]),
     "two pair, aces and jacks"
    ),
    (Hand([Card(CHAIN, 'A'),
           Card(CHAIN, '2'),
           Card(WEB, 'K'),
           Card(WEB, '2'),
           Card(CHAIN, 'K')]),
     "two pair, kings and deuces"
    ),
    (Hand([Card(CHAIN, 'A'),
           Card(WEB, '3'),
           Card(WEB, 'K'),
           Card(CHAIN, '3'),
           Card(LOCK,  '3')]),
     "three of a kind, threes"
    ),
    (Hand([Card(CHAIN, '8'),
           Card(WEB, 'K'),
           Card(WEB, '8'),
           Card(LOCK,  '8'),
           Card(WEB, 'A')]),
     "three of a kind, eights"
    ),
    (Hand([Card(CHAIN, 'Q'),
           Card(WEB, '6'),
           Card(WEB, 'K'),
           Card(WEB, 'Q'),
           Card(LOCK,  'Q')]),
     "three of a kind, queens"
    ),
    (Hand([Card(CHAIN, 'A'),
           Card(WEB, '3'),
           Card(WEB, '5'),
           Card(LOCK,  '4'),
           Card(WEB, '2')]),
     "five-high straight"
    ),
    (Hand([Card(CHAIN, '8'),
           Card(WEB, '6'),
           Card(WEB, '9'),
           Card(WEB, '5'),
           Card(LOCK,  '7')]),
     "nine-high straight"
    ),
    (Hand([Card(CHAIN, 'Q'),
           Card(WEB, 'K'),
           Card(WEB, '10'),
           Card(WEB, 'J'),
           Card(WEB, 'A')]),
     "ace-high straight"
    ),
    (Hand([Card(WEB, '2'),
           Card(WEB, '3'),
           Card(WEB, '4'),
           Card(WEB, '5'),
           Card(WEB, '7')]),
     "seven-high flush"
    ),
    (Hand([Card(CHAIN, '4'),
           Card(CHAIN, '7'),
           Card(CHAIN, '6'),
           Card(CHAIN, '9'),
           Card(CHAIN, '2')]),
     "nine-high flush"
    ),
    (Hand([Card(KEY, 'J'),
           Card(KEY, '10'),
           Card(KEY, '4'),
           Card(KEY, '3'),
           Card(KEY, '2')]),
     "jack-high flush"
    ),
    (Hand([Card(LOCK, 'A'),
           Card(LOCK, '2'),
           Card(LOCK, '3'),
           Card(LOCK, '4'),
           Card(LOCK, '6')]),
     "ace-high flush"
    ),
    (Hand([Card(LOCK, 'A'),
           Card(LOCK, '2'),
           Card(LOCK, '3'),
           Card(LOCK, '4'),
           Card(LOCK, '6')]),
     "ace-high flush"
    ),
    (Hand([Card(LOCK,  '10'),
           Card(LOCK,  '2'),
           Card(CHAIN, '2'),
           Card(WEB, '2'),
           Card(CHAIN, '10')]),
     "full house, deuces over tens"
    ),
    (Hand([Card(LOCK,  '10'),
           Card(LOCK,  '2'),
           Card(CHAIN, '2'),
           Card(WEB, '10'),
           Card(CHAIN, '10')]),
     "full house, tens over deuces"
    ),
    (Hand([Card(LOCK,    '4'),
           Card(LOCK,    'A'),
           Card(CHAIN,   '4'),
           Card(WEB,   '4'),
           Card(KEY, '4')]),
     "four of a kind, fours"
    ),
    (Hand([Card(LOCK, 'A'),
           Card(LOCK, '2'),
           Card(LOCK, '3'),
           Card(LOCK, '4'),
           Card(LOCK, '5')]),
     "five-high straight flush"
    ),
    (Hand([Card(CHAIN, '6'),
           Card(CHAIN, '2'),
           Card(CHAIN, '3'),
           Card(CHAIN, '4'),
           Card(CHAIN, '5')]),
     "six-high straight flush"
    ),
    (Hand([Card(KEY, '9'),
           Card(KEY, '8'),
           Card(KEY, '10'),
           Card(KEY, '7'),
           Card(KEY, '6')]),
     "ten-high straight flush"
    ),
    (Hand([Card(WEB, 'K'),
           Card(WEB, 'Q'),
           Card(WEB, '10'),
           Card(WEB, 'J'),
           Card(WEB, '9')]),
     "king-high straight flush"
    ),
    (Hand([Card(WEB, 'K'),
           Card(WEB, 'Q'),
           Card(WEB, '10'),
           Card(WEB, 'J'),
           Card(WEB, 'A')]),
     "royal flush"
    ),
])
