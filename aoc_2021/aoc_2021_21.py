import itertools
from typing import List, Tuple
from collections import Counter


def deterministic_die(positions: List[int], winner_score: int) -> int:
    scores = [0, 0]
    die = itertools.cycle(range(1, 101))
    turns = itertools.cycle(range(0, 2))
    turn = next(turns)
    rolled_times = 0
    while max(scores) < winner_score:
        positions[turn] = mod_with_offset(positions[turn] + sum(itertools.islice(die, 3)), 10)
        scores[turn] += positions[turn]
        turn = next(turns)
        rolled_times += 3

    return min(scores) * rolled_times


def mod_with_offset(value: int, maximum: int) -> int:
    _division, remainder = divmod(value, maximum)
    return remainder if remainder else maximum


def dirac_die_outcomes() -> Tuple[Tuple[int]]:
    results = Counter([d1 + d2 + d3 for d1, d2, d3 in itertools.product(range(1, 4), repeat=3)])
    return tuple((key, val) for key, val in results.items())


die_outcomes = dirac_die_outcomes()
memoization = dict()


def winning_universes(positions: Tuple[int], scores: Tuple[int], winner_score: int) -> Tuple[int]:
    pos_scores_key = (positions, scores)
    if scores[0] >= winner_score:
        memoization[pos_scores_key] = (1, 0)
    if scores[1] >= winner_score:
        memoization[pos_scores_key] = (0, 1)

    if (positions, scores) in memoization:
        return memoization[(positions, scores)]

    universes_player1_wins, universes_player2_wins = (0, 0)

    player1_position, player2_position = positions
    player1_score, player2_score = scores

    for dice_outcome, possibilities in die_outcomes:
        player1_new_pos = mod_with_offset(player1_position + dice_outcome, 10)
        player1_new_score = player1_score + player1_new_pos

        other_player_wins, current_player_wins = winning_universes(
            (player2_position, player1_new_pos),
            (player2_score, player1_new_score),
            winner_score,
        )

        universes_player1_wins += current_player_wins * possibilities
        universes_player2_wins += other_player_wins * possibilities

    memoization[pos_scores_key] = (universes_player1_wins, universes_player2_wins)

    return universes_player1_wins, universes_player2_wins


if __name__ == "__main__":
    print(deterministic_die([7, 5], winner_score=1000))
    universes = winning_universes((7, 5), (0, 0), winner_score=21)
    print(universes)
    print(max(universes))
