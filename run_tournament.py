import axelrod as axl
from random import randrange
from config import *


class Team:
    def __init__(self, strategy):
        self.strategy = strategy
        self.resources = 0
        self.head_count = 0

class Organization:
    def __init__(self):
        self.resources = float(randrange(COMPANY_RESOURCES_MIN, COMPANY_RESOURCES_MAX))
        self.head_count = randrange(COMPANY_HEADCOUNT_MIN, COMPANY_HEADCOUNT_MAX)
        self.teams = []

        for strategy in STRATEGIES:
            self.teams.append(Team(strategy))

        self.allocate_team_resources()

    #TODO
    def allocate_team_resources(self):
        # Some random algorithm to randomly allocate between teams
        num_teams = len(self.teams)

        # Right now it just does it equally between teams
        for team in self.teams:
            team.resources = float(self.resources/num_teams)
            team.head_count = round(self.head_count/num_teams)
    
    #TODO
    def reallocate_team_resources(self, all_matches):
        for match in all_matches:
            scores = match.scores()
            winner = match.winner()
            final_score = match.final_score()
            cooperation = match.cooperation()
            norm_cooperation = match.normalised_cooperation()
            #ranking = match.ranked_names()

            # Display Output
            #print("Teams: {}".format(ranking))
            print("Winner: {}".format(winner))
            print("Final Score: {}".format(final_score))
            print("Cooperation: {}".format(norm_cooperation))
            print("\n")

def allocate_company_resources():
    resources = float(randrange(COMPANY_RESOURCES_MIN, COMPANY_RESOURCES_MAX))
    head_count = randrange(COMPANY_HEADCOUNT_MIN, COMPANY_HEADCOUNT_MAX)
    return resources, head_count

def run_tournament(teams):
    team1 = teams[0]
    team2 = teams[1]
    num_rounds = max(team1.head_count, team2.head_count)

    # Run Match
    match = axl.Match((team1.strategy, team2.strategy), num_rounds)
    match.play()

    return match


def main():
    # Set Up Company and Teams
    my_org = Organization()

    # Run Tournament
    all_matches = []
    for games in range(0,NUM_ROUNDS):
        matches_this_round = []

        # Run tourament between teams round robin
        for i in range(0, len(my_org.teams)-1):
            for j in range(i+1, len(my_org.teams)):
                teams = (my_org.teams[i], my_org.teams[j])

                match_outcome = run_tournament(teams)
                matches_this_round.append(match_outcome)
                all_matches.append(match_outcome)

        # TODO - Relloacate resources after each round
        my_org.reallocate_team_resources(matches_this_round)

    # TODO - once game over, need to do some analysis on results

if __name__ == "__main__":
    main()