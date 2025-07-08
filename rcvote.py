"""A module implementing ranked choice voting."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Candidate:
    """A candidate in the election.

    Instance Attributes:
    - name: the name of the candidate.
    """
    name: str

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Candidate):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Ballot:
    """A voting ballot.

    Instance Attributes:
    - ranks: the ranking of all candidates. The last element is the first choice.
    """
    ranks: list[Candidate]
    valid: bool

    def __init__(self, ranks: list[Candidate]) -> None:
        self.ranks = ranks
        self.valid = True

    def __repr__(self) -> str:
        return f"({', '.join(map(str, self.ranks))})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ballot):
            return NotImplemented
        return self.ranks == other.ranks and self.valid == other.valid

    def __hash__(self) -> int:
        return hash(tuple(self.ranks)) ^ hash(self.valid)

    def shift(self, candidates: set[Candidate]) -> None:
        """Remove eliminated candidates from the ballot, until the first choice is an un-eliminated candidate
        or all candidates in the ballot have been eliminated already.
        """
        while len(self.ranks) > 0 and self.ranks[0] not in candidates:
            self.ranks.pop(0)

        if len(self.ranks) == 0:
            self.valid = False


class RCV:
    """A ranked choice voting election.

    Instance Attributes:
    - candidates: a list of candidates running.
    - ballots: a list of the ballots cast.
    """
    candidates: set[Candidate]
    ballots: list[Ballot]

    def __init__(self, candidates: set[Candidate], ballots: list[Ballot]) -> None:
        self.candidates = candidates
        self.ballots = ballots

    def get_winner(self, stats: bool = False) -> Candidate | bool:
        """Returns the winner of the election. (Without mutating instance attributes)
        """
        candidates = self.candidates
        ballots = self.ballots

        if stats:
            print(f'beginning elections with {[x for x in self.candidates]}\n')

        while len(candidates) > 1:
            for ballot in ballots:
                ballot.shift(candidates)

            vote_tally = self._tally_votes(ballots)
            least = self._count_valid_ballots()
            assert(least > 0), "There should be at least one valid ballot"
            eliminated = None

            if stats:
                print(f'first choice votes: {vote_tally}')

            for candidate, count in vote_tally.items():
                if count / self._count_valid_ballots() > 0.5:
                    if stats:
                        print(f'winner found: {candidate} with {count} votes')
                    return candidate
                elif count < least:
                    if stats:
                        print(f'new least candidate: {candidate} with {count} votes')
                    least = count
                    eliminated = candidate
                elif count == least and eliminated:
                    # Resolve tie
                    if stats:
                        print(f'tie between {candidate} and {eliminated}, resolving...')
                    ballot_subset_1 = [ballot for ballot in ballots if ballot.valid and
                                              ballot.ranks[0] == candidate]
                    ballot_subset_2 = [ballot for ballot in ballots if ballot.valid and
                                                ballot.ranks[0] == eliminated]

                    curr_level = 2
                    # As long as we have 'valid' ballots, look for the least preferred candidate
                    while any(len(ballot.ranks) >= curr_level for ballot in ballot_subset_1) or \
                            any(len(ballot.ranks) >= curr_level for ballot in ballot_subset_2):
                        votes_1 = self._tally_votes(ballot_subset_1, curr_level)
                        votes_2 = self._tally_votes(ballot_subset_2, curr_level)
                        if stats:
                            print(f'votes at level {curr_level}: {votes_2[candidate]} for {candidate}, '
                                  f'{votes_1[eliminated]} for {eliminated}')
                        if votes_2[candidate] < votes_1[eliminated]:
                            eliminated = candidate
                            break
                        elif votes_2[candidate] > votes_1[eliminated]:
                            eliminated = eliminated
                            break
                        # The policy is that if there is a genuine tie, the original candidate is eliminated
                        curr_level += 1

            if eliminated is None:
                raise ValueError("No candidate was eliminated, but there are still multiple candidates remaining.")

            candidates.remove(eliminated)

            if stats:
                print(f'eliminated {eliminated}, remaining candidates: {candidates}\n')

        return list(candidates)[0] if len(candidates) == 1 else False

    def _tally_votes(self, ballots: list[Ballot], i: int = 1) -> dict[Candidate, int]:
        """Counts the number of i-th choice votes that a candidate has.
        """
        tally = {candidate: 0 for candidate in self.candidates}
        for ballot in ballots:
            if ballot.valid and len(ballot.ranks) >= i and ballot.ranks[i - 1] in self.candidates:
                tally[ballot.ranks[i - 1]] += 1
        return tally

    def _count_valid_ballots(self) -> int:
        """Counts the number of valid ballots in the election.
        """
        return sum(1 for ballot in self.ballots if ballot.valid)
