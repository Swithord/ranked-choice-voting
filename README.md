# ranked-choice-voting
A simple Python implementaton for a ranked choice voting election.

Import this module with `import rcvote`

Create candidates with `Candidate('name')`.

Create voting ballots with `Ballot([candidate1, candidate2, ...])`. Ballots take a list of Candidates in the order of preference, the most preferred being first.
Duplicates are allowed, and the length of the list is not limited.

Initialize the election with `RCV({candidate1, candidate2, ...}, [ballot1, ballot2, ...]).

Example:
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
)```
