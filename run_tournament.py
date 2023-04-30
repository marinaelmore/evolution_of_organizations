import axelrod as axl
import random as rd
import pandas as pd
from config import *
import numpy as np
import matplotlib.pyplot as plt


class Employee:
    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff = 0

    def __repr__(self):
        return '{}'.format( self.strategy)

class Team:
    def __init__(self, team_id):
        self.resources = 0
        self.employees = []
        self.head_count = len(self.employees)
        self.team_id = team_id

    def __repr__(self):
        return 'Team ID: {}, Resources: {}, Head Count: {}, Employees: {}'.format(self.team_id, self.resources, self.head_count, self.employees)

class Organization:
    def __init__(self):
        self.resources = INIT_COMPANY_RESOURCES
        self.cost_per_head = COST_PER_HEAD
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
        team = Team(team_id)
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

# run_match takes two Team objects and randomly assigns matches 2 * max(headcount) between
# the two teams. It then aggregates the scores and the number of times/turns each player played
# and returns both lists.
# Return format: [[team 1 scores],[team 2 scores]], [[team 1 turns],[team 2 turns]]
def run_match(team1, team2):
    scores = [[0]*team1.head_count, [0]*team2.head_count]
    num_turns = [[0]*team1.head_count, [0]*team2.head_count]
    # Have a sufficient number of rounds so that each team member is likely to have at least one match.
    rounds = 2*max(team1.head_count, team2.head_count)

    for r in range(0, rounds):
        # Pick a random player from team 1 and team 2
        player1_id = rd.randrange(0,team1.head_count)
        player2_id = rd.randrange(0,team2.head_count)

        # Match those players for a single turn with some noise (noise = variation from assigned strategy)
        match = axl.Match((team1.employees[player1_id].strategy, team2.employees[player2_id].strategy), turns = 1, noise = 0.1)
        match.play()

        scores[0][player1_id] = match.final_score_per_turn()[0]
        scores[1][player2_id] = match.final_score_per_turn()[1]
        num_turns[0][player1_id] += 1
        num_turns[1][player2_id] += 1

    #return all results from the round
    return scores, num_turns

def main():
    # Set Up Company and Teams
    my_org = Organization()

    # Track total score and total number of matches PER player PER team.
    total_scoreboard, total_matches = [], []
    normalized_scoreboard = [] # normalized scoreboard: total_scoreboard / total_matches
    for t in range(len(my_org.teams)):
        total_scoreboard.append([0]*my_org.teams[t].head_count)
        total_matches.append([0]*my_org.teams[t].head_count)
        normalized_scoreboard.append([0]*my_org.teams[t].head_count)

    # Run Tournament
    for _ in range(0,NUM_ROUNDS):
        # Run tourament between teams round robin
        for i in range(0, len(my_org.teams)-1):
            for j in range(i+1, len(my_org.teams)):
                # This will run all matches between employees on a team
                match_outcome, num_matches = run_match(my_org.teams[i], my_org.teams[j])

                # settle match scores in the total trackers
                team_i, team_j = match_outcome[0], match_outcome[1]
                num_matches_i, num_matches_j = num_matches[0], num_matches[1]
                for ti in range(len(team_i)):
                    total_scoreboard[i][ti] +=  team_i[ti]
                    total_matches[i][ti] += num_matches_i[ti]
                for tj in range(len(team_j)):
                    total_scoreboard[j][tj] += team_j[tj]
                    total_matches[j][tj] += num_matches_j[tj]

        # print("Total_scoreboard at the end of round {}: {}".format(_, total_scoreboard))
        
        # calculate team scores to determine layoffs
        score_sum = []
        for team_score in total_scoreboard:
            score_sum.append(sum(team_score))
        score_sum = np.array(score_sum)
        # find team number (lowest team_score) that will be impacted by layoffs
        layoff_team = np.argmin(score_sum)

        # iterate through LAYOFF_NUM (in config) and layoff staff one by one: 
        for nn in range(LAYOFF_NUM):
            # index of person getting laid off
            layoff_person = np.argmin(total_scoreboard[layoff_team])
            # del selected person from my_org (layoff)
            del my_org.teams[layoff_team].employees[layoff_person]
            # re-do headcount
            my_org.teams[layoff_team].head_count = len(my_org.teams[layoff_team].employees)
            # take the person out of total_scoreboard
            del total_scoreboard[layoff_team][layoff_person]

        # print('score_sum: {}'.format(score_sum))
        # print('layoff_team {}'.format(layoff_team))
        # print("teams at the end of round: {}".format(my_org.teams))

    # calculate the normalized scoreboard
    for i in range(len(total_scoreboard)):
        for s in range(len(total_scoreboard[i])):
            normalized_scoreboard[i][s] = float(total_scoreboard[i][s])/total_matches[i][s]

    # iterate through teams and print individual scores for each team
    for nn in range(len(my_org.teams)):
        plt.title('Team {} Performance'.format(nn+1))
        plt.xlabel('Players')
        plt.ylabel('Scores')
        plt.scatter(
            range(1, (my_org.teams[nn].head_count)+1),
            total_scoreboard[nn]
            )
        # visual tickmarks on x axis
        plt.xticks(
            np.arange(1, my_org.teams[nn].head_count+1)
            )
        plt.show()

    if DEBUG:
        for t in my_org.teams: print(t)
        print()
        print('Final scoreboard: {}'.format(total_scoreboard))
        print('Total matches: {}'.format(total_matches))
        print('Normalized scoreboard: {}'.format(normalized_scoreboard))

if __name__ == "__main__":
    main()
