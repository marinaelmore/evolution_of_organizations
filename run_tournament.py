import axelrod as axl
import random as rd
import pandas as pd
from config import *


class Employee:
    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff = 0

    def __repr__(self):
        return '{}'.format( self.strategy)

class Team:
    def __init__(self):
        self.resources = 0
        self.head_count = 0
        self.employees = []

    def __repr__(self):
        return 'Team: {} resources\nHead Count: {}\nEmployees: {}\n\n'.format(self.resources, self.head_count, self.employees)

class Organization:
    def __init__(self):
        self.resources = INIT_COMPANY_RESOURCES
        self.cost_per_head = COST_PER_HEAD
        self.head_count =  INIT_COMPANY_RESOURCES / COST_PER_HEAD
        self.num_teams = NUM_TEAMS
        self.teams = []
        self.strategy_allocation = STRATEGY_ALLOCATION

        if self.num_teams != len(STRATEGY_ALLOCATION):
            print('Error: Strategy allocation must match number of teams')
            return

        for team_id in range(0, self.num_teams):
            self.teams.append(self.allocate_team_resources(team_id))

    # Initialize: Equal division of head count and resources.
    def allocate_team_resources(self, team_id):
        team = Team()
        team.resources = float(self.resources/self.num_teams)
        team.head_count = round(team.resources/self.cost_per_head)
        team_strategy = self.strategy_allocation[team_id]

        # Create teams that probabalistically match the STRATEGY_ALLOCATION assignment
        for i in range(0, team.head_count):
            diceroll = rd.uniform(0,1)

            prob_sum = 0.0
            for t in range(len(team_strategy)):
                prob_sum += float(team_strategy[t])
                if 0.0 <= diceroll < prob_sum:
                    strategy = STRATEGIES[t]
                    team.employees.append(Employee(strategy))
                    break

        return team


    # #TODO
    # def reallocate_team_resources(self, tournament):
    #     scores = tournament.scores
    #     wins = tournament.wins
    #     final_score = tournament.scores
    #     cooperation = tournament.cooperation
    #     norm_cooperation = tournament.normalised_cooperation
    #     ranking = tournament.ranked_names
    #     payoff = tournament.payoff_matrix

    #     #Find the total payoff for each team (sum across all rounds) -- ADDED BY ELIZABETH
    #     payoff_df = pd.DataFrame(payoff)
    #     sum_payoff = payoff_df.sum(axis=0)
    #     sum_payoff = pd.DataFrame({'Team Payoff': sum_payoff})
    #     sum_payoff.index.name = 'Team Number'
    #     sum_payoff = sum_payoff.reset_index()+1

    #     #Find percent of total payoff, for each team (which will later be used to allocate resources) - ADDED BY ELIZABETH
    #     total_payoff = sum_payoff['Team Payoff'].sum()
    #     sum_payoff['Percent of Total Payoff'] = round(sum_payoff['Team Payoff'] / total_payoff * 100,2)

    #     # Display Output
    #     print("Teams: {}".format(ranking))
    #     print("Wins: {}".format(wins))
    #     print("Final Score: {}".format(final_score))
    #     print("Cooperation: {}".format(norm_cooperation))
    #     print("Payoff: {}".format(payoff))
    #     print("\nThe Payoff for each team after the tournament is: \n{}".format(sum_payoff)) # -- ADDED BY ELIZABETH
    #     print("\n")

def allocate_company_resources():
    resources = float(rd.randrange(COMPANY_RESOURCES_MIN, COMPANY_RESOURCES_MAX))
    head_count = rd.randrange(COMPANY_HEADCOUNT_MIN, COMPANY_HEADCOUNT_MAX)
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

# def run_tournament(teams):
#     tournament = axl.Tournament(teams)
#     results = tournament.play()
#     return results

def main():
    # Set Up Company and Teams
    my_org = Organization()
    # Debug
    #print(my_org.teams)

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
