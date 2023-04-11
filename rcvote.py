"""A module implementing ranked choice voting."""


class Candidate:
    """A candidate in the election.

    Instance Attributes:
    - name: the name of the candidate.
    """
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


class Ballot:
    """A voting ballot.

    Instance Attributes:
    - ranks: the ranking of all candidates.
    """
    ranks: list[Candidate]
    valid: bool

    def __init__(self, ranks: list[Candidate]) -> None:
        self.ranks = ranks
        self.valid = True

    def __repr__(self) -> str:
        return '(' + ', '.join([str(candidate) for candidate in self.ranks]) + ')'

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
        import random

        if stats:
            print(f'beginning elections with {[x for x in self.candidates]}\n')

        while len(ballots) > 0 and len(candidates) > 0:
            for ballot in ballots:
                ballot.shift(candidates)

            n = len([ballot for ballot in ballots if ballot.valid])
            first_choices = [ballot.ranks[0] for ballot in ballots if ballot.valid]
            vote_tally = self._tally_winner(first_choices)
            least = n
            elimination_candidates = []

            if stats:
                print(f'first choice votes: {vote_tally}')

            for candidate in vote_tally:
                if vote_tally[candidate] / n > 0.5:
                    return candidate
                elif vote_tally[candidate] < least:
                    least = vote_tally[candidate]
                    elimination_candidates = [candidate]
                elif vote_tally[candidate] == least:
                    elimination_candidates.append(candidate)

            eliminated = random.choice(elimination_candidates)
            candidates.remove(eliminated)

            if stats:
                print(f'eliminated {eliminated}, remaining candidates: {candidates}\n')

        return False

    def _tally_winner(self, first_choices: list[Candidate]) -> dict[Candidate, int]:
        """Counts the number of first choice votes that a candidate has.
        """
        counts = dict()
        for choice in first_choices:
            counts[choice] = counts.get(choice, 0) + 1

        for candidate in self.candidates:
            if candidate not in counts.keys():
                counts[candidate] = 0

        return counts


if __name__ == "__main__":
    print('printing test results\n==========')
    david = Candidate('david liu')
    tom = Candidate('thomas fairgrieve')
    mario = Candidate('mario badr')
    gazzale = Candidate('robert gazzale')
    election = RCV({david, tom, mario, gazzale}, [
        Ballot([david, david, david, david, david]),  # DAVID LIU FTW (ALSO BORIS KHESIN >>>>> JASON SIEFKEN)
        Ballot([tom]),
        Ballot([david, tom]),
        Ballot([tom, david]),
        Ballot([tom, mario]),
        Ballot([mario, david, tom]),
        Ballot([mario, tom, david]),
        Ballot([mario]),
        Ballot([mario])
    ])
    print(election.get_winner(True).name)
