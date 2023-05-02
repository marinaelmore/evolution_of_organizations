import axelrod as axl

STRATEGIES = [axl.Cooperator(), axl.Alternator(), axl.BackStabber()]

# COMPANY
INIT_COMPANY_RESOURCES = 300
COST_PER_HEAD = 10
NUM_TEAMS = 3

# number of people you'll layoff per round
LAYOFF_NUM = 1
LAYOFF_PCT = 0.2
LAYOFF_ALL_THRESHOLD = 3 # If there are ever fewer than 3 employees on a team, lay them all off.

# HIRING
HIRING_PCT = 0.2
HIRING_INFLATION = 0.07

# Format: [Team 1: [Cooperator %, Alternator %, Backstabber %], Team 2... , Team 3]
STRATEGY_ALLOCATION = [[0.8, 0.1, 0.1], [0.6, 0.3, 0.1], [0.6, 0.1, 0.3]]

# NUMBER OF ROUNDS
NUM_ROUNDS = 3
TOTAL_YEARS = 15

DEBUG = True
