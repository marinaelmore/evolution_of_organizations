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
    def reallocate_team_resources(self, tournament):
        scores = tournament.scores
        wins = tournament.wins
        final_score = tournament.scores
        cooperation = tournament.cooperation
        norm_cooperation = tournament.normalised_cooperation
        ranking = tournament.ranked_names
        payoff = tournament.payoff_matrix
        
        #Find the total payoff for each team (sum across all rounds) -- ADDED BY ELIZABETH
        payoff_df = pd.DataFrame(payoff)
        sum_payoff = payoff_df.sum(axis=0)
        sum_payoff = pd.DataFrame({'Team Payoff': sum_payoff})
        sum_payoff.index.name = 'Team Number'
        sum_payoff = sum_payoff.reset_index()+1
        
        # Display Output
        print("Teams: {}".format(ranking))
        print("Wins: {}".format(wins))
        print("Final Score: {}".format(final_score))
        print("Cooperation: {}".format(norm_cooperation))
        print("Payoff: {}".format(payoff))
        print("The Payoff for each team is: \n{}".format(sum_payoff)) # -- ADDED BY ELIZABETH
        print("\n")

def allocate_company_resources():
    resources = float(randrange(COMPANY_RESOURCES_MIN, COMPANY_RESOURCES_MAX))
    head_count = randrange(COMPANY_HEADCOUNT_MIN, COMPANY_HEADCOUNT_MAX)
    return resources, head_count

def run_match(teams):
    team1 = teams[0]
    team2 = teams[1]
    num_rounds = max(team1.head_count, team2.head_count)

    # Run Match
    match = axl.Match((team1.strategy, team2.strategy), num_rounds)
    match.play()

    return match

def run_tournament(teams):
    tournament = axl.Tournament(teams)
    results = tournament.play()
    return results

def main():
    # Set Up Company and Teams
    my_org = Organization()

    # Run Tournament
    all_rounds = []
    for round in range(0,NUM_ROUNDS):

        tournament_results = run_tournament([team.strategy for team in my_org.teams])

        all_rounds.append(tournament_results)

        # TODO - Relloacate resources after each round
        my_org.reallocate_team_resources(tournament_results)

    # TODO - once game over, need to do some analysis on results

if __name__ == "__main__":
    main()