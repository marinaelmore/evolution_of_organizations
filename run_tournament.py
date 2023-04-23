import axelrod as axl
from random import randrange
from config import *


class Employee:
    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff = 0

class Team:
    def __init__(self):
        self.resources = 0
        self.head_count = 0
        self.employees = []

class Organization:
    def __init__(self):
        self.resources = float(randrange(COMPANY_RESOURCES_MIN, COMPANY_RESOURCES_MAX))
        self.head_count = randrange(COMPANY_HEADCOUNT_MIN, COMPANY_HEADCOUNT_MAX)
        self.num_teams = NUM_TEAMS
        self.teams = []

        for i in range(0, self.num_teams):
            self.teams.append(self.allocate_team_resources())        

    #TODO Right now it just does it equally between teams
    def allocate_team_resources(self):
        team = Team()
        team.resources = float(self.resources/self.num_teams)
        team.head_count = round(self.head_count/self.num_teams)

        for i in range(0, team.head_count):
            diceroll = randrange(0,len(STRATEGIES))
            strategy = STRATEGIES[diceroll]
            team.employees.append(Employee(strategy))

        return team


    #TODO
    def reallocate_team_resources(self, tournament):
        scores = tournament.scores
        wins = tournament.wins
        final_score = tournament.scores
        cooperation = tournament.cooperation
        norm_cooperation = tournament.normalised_cooperation
        ranking = tournament.ranked_names
        payoff = tournament.payoff_matrix

        # Display Output
        print("Teams: {}".format(ranking))
        print("Wins: {}".format(wins))
        print("Final Score: {}".format(final_score))
        print("Cooperation: {}".format(norm_cooperation))
        print("Payoff: {}".format(payoff))
        print("\n")

def allocate_company_resources():
    resources = float(randrange(COMPANY_RESOURCES_MIN, COMPANY_RESOURCES_MAX))
    head_count = randrange(COMPANY_HEADCOUNT_MIN, COMPANY_HEADCOUNT_MAX)
    return resources, head_count

# TODO - create a tournament where each employee on team1 plays each employee on team2
def run_match(team1, team2):
    matches_this_round = []
    num_rounds = max(team1.head_count, team2.head_count)

    #  TODO Run Match
    # for all employees:
        #match = axl.Match((employee1.strategy, employee2.strategy), num_rounds)
        #match.play()
        #matches_this_round.append(match outcome)

    #return all results from the round
    return matches_this_round

def run_tournament(teams):
    tournament = axl.Tournament(teams)
    results = tournament.play()
    return results

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
                # This will run all matches between employees on a team
                match_outcome = run_match(my_org.teams[i], my_org.teams[j])
                matches_this_round.append(match_outcome)

            all_matches.append(matches_this_round)

        # TODO - Relloacate resources after each round
        #my_org.reallocate_team_resources(matches_this_round)


    # TODO - once game over, need to do some analysis on results

if __name__ == "__main__":
    main()