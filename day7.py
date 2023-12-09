from __future__ import annotations
import os
from inputreader import aocinput
from collections import Counter


class Hand:
    def __init__(self, cards: list[int], bid: int):
        self.cards = cards
        self.bid = bid
        self.hand_type = self._get_hand_type()

    def _get_hand_type(self) -> int:
        card_counts = Counter(self.cards)
        if card_counts[0] > 0:  # joker(s) in hand
            joker_count = card_counts.pop(0)
            if joker_count == 5:  # if only jokers, avoid errors
                card_counts[0] = 5
            else:
                card_counts[card_counts.most_common(1)[0][0]] += joker_count

        if 5 in card_counts.values():
            return 6
        elif 4 in card_counts.values():
            return 5
        elif 3 in card_counts.values() and 2 in card_counts.values():
            return 4
        elif 3 in card_counts.values():
            return 3
        elif Counter(card_counts.values())[2] == 2:
            return 2
        elif 2 in card_counts.values():
            return 1
        else:
            return 0

    def __lt__(self, other: Hand) -> bool:
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        for i in range(len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] < other.cards[i]
        return False

    def __repr__(self) -> str:
        return ' '.join([str(value) for value in self.cards])


def winnings(data: list[str], card_values: dict[str, int]) -> int:
    hands = []
    for line in data:
        cards, bid = line.split()
        cards = [int(card) if card.isnumeric() else card_values[card] for card in cards]
        hands.append(Hand(cards, int(bid)))
    return sum(i * hand.bid for i, hand in enumerate(sorted(hands), start=1))


cardConvert = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
cardConvert2 = {'A': 14, 'K': 13, 'Q': 12, 'J': 0, 'T': 10}  # use jokers instead of jacks


def main(day: int):
    data = aocinput(day)
    result = winnings(data, cardConvert)
    result2 = winnings(data, cardConvert2)
    print(result, result2)


if __name__ == '__main__':
    main(int(os.path.basename(__file__)[3:-3]))
