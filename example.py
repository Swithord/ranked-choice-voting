from rcvote import RCV, Candidate, Ballot

if __name__ == "__main__":
    print('printing test results\n==========')
    david = Candidate('david l.')
    steve = Candidate('steve e.')
    mario = Candidate('mario b.')
    marsha = Candidate('marsha c.')
    jack = Candidate('jack s.')
    election = RCV({david, steve, mario, marsha, jack}, [
        Ballot([david, david, david, david, david]),
        Ballot([steve]),
        Ballot([david, steve]),
        Ballot([steve, david]),
        Ballot([steve, mario]),
        Ballot([mario, david, steve]),
        Ballot([mario, steve, david]),
        Ballot([mario]),
        Ballot([mario]),
        Ballot([marsha, david]),
        Ballot([jack, marsha, david]),
        Ballot([jack])
    ])
    print(f"winner: {election.get_winner(True).name}")