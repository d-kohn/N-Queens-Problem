import copy
import random

QUEENS = 9
BOARD = [['_' for row in range(QUEENS)] for col in range(QUEENS)]       
BEST_FITNESS = (QUEENS * (QUEENS-1)) / 2
CANDIDATE_COUNT = 100

def print_board(solution):   
    display_board = copy.deepcopy(BOARD)
    for i in range(QUEENS):
        display_board[int(solution[i])][i] = 'Q'

    print(" _",end="")
    for i in range(QUEENS-1):
        print("__",end="")
    print()

    for y in range(QUEENS):
        print("|",end="")
        for x in range(QUEENS):
            print(f"{display_board[y][x]}|",end="")
        print()
    print()

def generate_initial_candidates():
    candidates = []
    for i in range(CANDIDATE_COUNT):
        candidate = ""
        for c in range(QUEENS):
            candidate += str(random.randrange(0,QUEENS))
        candidates.append(candidate)
    return candidates

def test_fitness(candidate):
    conflicts = 0
    for i in range(QUEENS):
        left = int(candidate[i])
        for t in range(i+1,QUEENS):
            right = int(candidate[t])
            # If there are two genes on the same row: conflict
            if (left == right):
                conflicts += 1
            # if the abs value of the up/down distance == left/right distance: conflict
            if (abs(left-right) == t-i):
                conflicts += 1
    return BEST_FITNESS - conflicts

def score_candidates(candidates):
    scores = {}
    for i in range(CANDIDATE_COUNT):
        scores[candidates[i]] = test_fitness(candidates[i])
    return scores

def test_goal_state(scores):
    goal_found = "-1"
    for candidate in scores:
        if (scores[candidate] == BEST_FITNESS):
            goal_found = candidate
            break
    return goal_found

#test_candidate = "41050463"
#fitness = test_fitness(test_candidate)
#print_board(test_candidate, fitness)

generation = 0
f = open("test_data.txt", "a")
candidates = generate_initial_candidates()
f.write("Initial Candidates\n")
f.write(f"{candidates}\n\n")

while(True):
    scores = score_candidates(candidates)
    goal_check = test_goal_state(scores)
    if (goal_check != "-1"):
        print_board(goal_check)
        break

