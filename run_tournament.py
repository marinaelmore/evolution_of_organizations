import axelrod as axl
import random as rd
import pandas as pd
from config import *
import numpy as np
import matplotlib.pyplot as plt
import math


class Employee:
    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff = 0

    def __repr__(self):
        return '{}'.format(self.strategy)

class Team:
    def __init__(self, team_id):
        self.resources = 0
        self.employees = []
        self.head_count = len(self.employees)
        self.team_id = team_id

    def layoff_random(self):
        self.employees.pop(rd.randrange(self.head_count))
        self.head_count = len(self.employees)

    def hire_employees(self, payoff):
        new_headcount = math.ceil(payoff)

        for i in range(0, new_headcount):
            strategy = STRATEGIES[rd.randint(0,len(STRATEGIES)-1)]
            self.employees.append(Employee(strategy))
            self.head_count = len(self.employees)


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

    def remove_team(self, idx):
        self.teams.pop(idx)
        self.num_teams = len(self.teams)

    def execute_hiring(self, payoff_per_team_normalized, hiring_pct):
        max_payoff = 0
        max_team = None

        # Determine team with highest normalized score. They will receive more resources
        for i in range(0,len(self.teams)):
            team_payoff = payoff_per_team_normalized[i]
            team = self.teams[i]

            if team_payoff > max_payoff:
                max_payoff = team_payoff
                max_team = team

        max_team.hire_employees(max_payoff)

    def execute_layoffs(self, payoff_per_team_normalized, layoff_pct, layoff_all_threshold):
        # Determine team with lowest normalized score. They will be impacted by layoffs.
        m = min(i for i in payoff_per_team_normalized if i > 0)
        layoff_team_idx = payoff_per_team_normalized.index(m)

        # Lay off layoff_pct percentage as defined in config
        layoff_team = self.teams[layoff_team_idx]
        total_layoff_count = int(math.ceil(layoff_pct * layoff_team.head_count))

        # If there will be fewer than layoff_all_threshold employees on a team, lay them all off.
        if (layoff_team.head_count - total_layoff_count) < layoff_all_threshold:
            total_layoff_count = layoff_team.head_count

        for i in range(total_layoff_count):
            layoff_team.layoff_random()

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

# run_match takes two Team objects and randomly assigns matches 2 * max(headcount) between
# the two teams. It then aggregates the scores and the number of times/turns each player played
# and returns both lists.
# Return format: [[team 1 scores],[team 2 scores]], [[team 1 turns],[team 2 turns]]
def run_match(team1, team2):
    scores = [[0]*team1.head_count, [0]*team2.head_count]
    num_turns = [[0]*team1.head_count, [0]*team2.head_count]

    # If either team has 0 players, there is no match to run. Skip.
    if team1.head_count == 0 or team2.head_count == 0:
        return scores, num_turns

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

    # each index represents a year
    lifetime_scoreboard_normalized = [[] for i in range(len(my_org.teams))] # avg payoff for employees on a specific team
    lifetime_team_size = [[] for i in range(len(my_org.teams))] # number of team members per team
    lifetime_org_score_normalized = [] # avg employee payoff in the organization

    # Run it for TOTAL_YEARS iterations or until there is one team remaining.
    year = 0
    while year < TOTAL_YEARS:

        #if my_org.num_teams == 1:
        #    break

        # Track total score and total number of matches PER player PER team.
        annual_scoreboard, annual_matches = [], []
        normalized_scoreboard = [] # normalized scoreboard: annual_scoreboard / annual_matches
        for t in range(len(my_org.teams)):
            annual_scoreboard.append([0]*my_org.teams[t].head_count)
            annual_matches.append([0]*my_org.teams[t].head_count)
            normalized_scoreboard.append([0]*my_org.teams[t].head_count)

        # Run Tournament
        for _ in range(0,NUM_ROUNDS):
            # Run tourament between teams round robin
            for i in range(0, len(my_org.teams)-1):
                for j in range(i+1, len(my_org.teams)):
                    # This will run all matches between employees on a team
                    match_outcome, num_matches = run_match(my_org.teams[i], my_org.teams[j])

                    # settle match scores in the annual trackers
                    team_i, team_j = match_outcome[0], match_outcome[1]
                    num_matches_i, num_matches_j = num_matches[0], num_matches[1]
                    for ti in range(len(team_i)):
                        annual_scoreboard[i][ti] +=  team_i[ti]
                        annual_matches[i][ti] += num_matches_i[ti]
                    for tj in range(len(team_j)):
                        annual_scoreboard[j][tj] += team_j[tj]
                        annual_matches[j][tj] += num_matches_j[tj]

        # calculate the normalized scoreboard
        for i in range(len(annual_scoreboard)):
            for s in range(len(annual_scoreboard[i])):
                if annual_matches[i][s] == 0: # player was randomly not assigned to match
                    normalized_scoreboard[i][s] = 0 # While it is possible that this player did not play, it's highly unlikely considering we are iterating NUM_ROUNDS times. Set it to 0 for the case where the team has 0 players and therefore 0 matches too.
                else:
                    normalized_scoreboard[i][s] = float(annual_scoreboard[i][s])/annual_matches[i][s]

        # Find the annualized team and organization payoff (for normalized final scores)
        payoff_per_team_normalized = []
        current_team_size = []
        for i in range(len(normalized_scoreboard)):
            current_team_size.append(len(normalized_scoreboard[i]))
            if len(normalized_scoreboard[i]) == 0:
                payoff_per_team_normalized.append(0)
            else:
                payoff_per_team_normalized.append(np.sum(normalized_scoreboard[i])/len(normalized_scoreboard[i]))

        org_payoff_normalized = np.sum(payoff_per_team_normalized)

        # Track lifetime metrics for reporting purposes
        for x in range(len(payoff_per_team_normalized)):
            lifetime_scoreboard_normalized[x].append(payoff_per_team_normalized[x])
        for y in range(len(current_team_size)):
            lifetime_team_size[y].append(current_team_size[y])
        lifetime_org_score_normalized.append(org_payoff_normalized)

        if DEBUG:
            print('Year {}:'.format(year))
            for t in my_org.teams: print(t)
            print('Normalized scoreboard: {}'.format(normalized_scoreboard))
            print('Normalized payoff per team: {}'.format(payoff_per_team_normalized))
            print('Annual normalized organization payoff: {}'.format(org_payoff_normalized))
            print('\n')

        # Lay off from worst team
        my_org.execute_layoffs(payoff_per_team_normalized, LAYOFF_PCT, LAYOFF_ALL_THRESHOLD)

        # Allow best team to hire more employees
        my_org.execute_hiring(payoff_per_team_normalized, HIRING_PCT)

        # Only continue if there are at least 2 teams in the organization
        active_teams = 0
        for t in my_org.teams:
            if t.head_count > 0:
                active_teams += 1

        if active_teams == 1:
            print('Simulation ended after {} years'.format(year))
            break

        year += 1

    # Create plots for reporting purposes
    fig, ax = plt.subplots(3, figsize=(5, 10))
    fig.subplots_adjust(hspace=0.5)
    for i in range(len(lifetime_scoreboard_normalized)):
        name = 'team {}'.format(i+1)
        ax[0].plot(lifetime_scoreboard_normalized[i], label=name)

    ax[0].legend(loc='upper right')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Points')
    ax[0].set_xticks(np.arange(0, year+1))
    ax[0].set_title('Normalized Points for a Team per Interaction vs Time')

    for i in range(len(lifetime_team_size)):
        name = 'team {}'.format(i+1)
        ax[1].plot(lifetime_team_size[i], label=name)

    ax[1].legend(loc='upper right')
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Team Size')
    ax[1].set_xticks(np.arange(0, year+1))
    ax[1].set_title('Number of Team Members vs Time')

    ax[2].plot(lifetime_org_score_normalized)
    ax[2].set_xlabel('Year')
    ax[2].set_ylabel('Points')
    ax[2].set_xticks(np.arange(0, year+1))
    ax[2].set_yticks(np.arange(0, max(lifetime_org_score_normalized),step=0.5))
    ax[2].set_title('Average points across the organization vs Time')

    plt.show()

if __name__ == "__main__":
    main()
