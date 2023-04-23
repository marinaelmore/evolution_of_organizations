import axelrod as axl

STRATEGIES = [axl.Cooperator(), axl.Alternator(), axl.BackStabber()]

# COMAPANY
INIT_COMPANY_RESOURCES = 300
COST_PER_HEAD = 10
NUM_TEAMS = 3

# Format: [Team 1: [Cooperator %, Alternator %, Backstabber %], Team 2... , Team 3]
STRATEGY_ALLOCATION = [[0.8, 0.1, 0.1], [0.6, 0.3, 0.1], [0.6, 0.1, 0.3]]

#COMPANY_RESOURCES_MIN = 1000
#COMPANY_RESOURCES_MAX = 1000000
#COMPANY_HEADCOUNT_MIN = 10
#COMPANY_HEADCOUNT_MAX = 20

# NUMBER OF ROUNDS
NUM_ROUNDS = 2


