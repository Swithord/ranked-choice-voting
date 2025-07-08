# ranked-choice-voting
A simple Python implementaton for a [ranked choice voting](https://en.wikipedia.org/wiki/Ranked_voting) election: a fairer, more representative single-winner voting system.


### Instructions 

Import this module with `import rcvote`

Create candidates with `Candidate('name')`.

Create voting ballots with `Ballot([candidate1, candidate2, ...])`. Ballots take a list of Candidates in the order of preference, the most preferred being first (i.e. at index 0).
Duplicates are allowed, and the length of the list is not limited.

Initialize the election with `RCV({candidate1, candidate2, ...}, [ballot1, ballot2, ...])`. Return the winner with `RCV.get_winner()`, which evaluates the votes and returns the winning Candidate. Pass in `True` for a break-down of the computation.

### Example:
```
alfonso = Candidate('alfonso grazia-saz')
siefken = Candidate('jason siefken')
boris = Candidate('boris khesin')

ballot1 = Ballot([alfonso, boris, siefken])
ballot2 = Ballot([boris, boris])
ballot3 = Ballot([alfonso])
ballot4 = Ballot([boris, siefken])
ballot5 = Ballot([alfonso, alfonso, alfonso, alfonso, boris, siefken, boris, alfonso])

rcv = RCV(
  {alfonso, siefken, boris},
  [ballot1, ballot2, ballot3, ballot4, ballot5]
)

print(rcv.get_winner().name)
```

### Tie-breaking
Ties in first-choice votes are broken according to the following rule: Between candidates A and B, we consider the ballot sets S_A and S_B, consisting of ballots where candidates A and B respectively are the first-choice. If there are more second-choice votes for A in S_B than for B in S_A, then A wins. If there are more second-choice votes for B in S_A than for A in S_B, then B wins. If the number of second-choice votes is equal, then the candidate with more third-choice votes wins, and so on. Genuine ties are broken by eliminating the candidate which was iterated over first.
