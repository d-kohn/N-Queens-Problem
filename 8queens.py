import copy
import random

QUEENS = 8
BOARD = [['_' for row in range(QUEENS)] for col in range(QUEENS)]       
BEST_FITNESS = int((QUEENS * (QUEENS-1)) / 2)
CANDIDATE_COUNT = 1000
MUTAGEN = 0.01
REPORT_FREQUENCY = 10

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
        candidate = []
        for c in range(QUEENS):
            candidate.append(random.randrange(0,QUEENS))
        candidates.append(candidate)
    return candidates

def test_fitness(candidate):
    conflicts = 0
    for i in range(QUEENS):
        left = candidate[i]
        for t in range(i+1,QUEENS):
            right = candidate[t]
            # If there are two genes on the same row: conflict
            if (left == right):
                conflicts += 1
            # if the abs value of the up/down distance == left/right distance: conflict
            if (abs(left-right) == t-i):
                conflicts += 1
    return BEST_FITNESS - conflicts

def score_candidates(candidates):
    best_score = 0
    best_candidate = []
    score_sum = 0
    scores = {}
    for i in range(CANDIDATE_COUNT):
        score = test_fitness(candidates[i])
        score_sum += score
        scores[tuple(candidates[i])] = score
        if (scores[tuple(candidates[i])] > best_score):
            best_score = scores[tuple(candidates[i])]
            best_candidate = tuple(candidates[i])
    return scores, best_candidate, score_sum

def splice(candidate1, candidate2):
    splice_spot = random.randrange(0,QUEENS)
    new_candidate1 = candidate1[:splice_spot] + candidate2[splice_spot:]
    new_candidate2 = candidate2[:splice_spot] + candidate1[splice_spot:]
    return mutate(new_candidate1), mutate(new_candidate2)

def mutate(candidate):
    for c in range(0, QUEENS):
        if (random.random() < MUTAGEN):
            candidate[c] = random.randrange(0,QUEENS)
    return candidate

def generate_next_generation(scores, sum_scores):
    next = 0
    scores_hist = {}
    best_score = 0
    best_candidate = []
    new_sum_score = 0
    new_scores = {}

#    new_candidates = []
    for candidate in scores:
        p = int((scores[candidate]/sum_scores)*CANDIDATE_COUNT*10)
        for i in range(next,next+p):
            scores_hist[i] = candidate
        next = next+p    
    for q in range(0,CANDIDATE_COUNT,2):
        new_candidate1 = list(scores_hist[random.randrange(0,len(scores_hist))])
        new_candidate2 = list(scores_hist[random.randrange(0,len(scores_hist))])
        new_candidate1, new_candidate2 = splice(new_candidate1, new_candidate2)

        score = test_fitness(new_candidate1)
        new_sum_score += score
        new_scores[tuple(new_candidate1)] = score
        if (new_scores[tuple(new_candidate1)] > best_score):
            best_score = score
            best_candidate = tuple(new_candidate1)

        score = test_fitness(new_candidate2)
        new_sum_score += score
        new_scores[tuple(new_candidate2)] = score
        if (new_scores[tuple(new_candidate2)] > best_score):
            best_score = score
            best_candidate = tuple(new_candidate2)
#        new_candidates.append(new_candidate1)
#        new_candidates.append(new_candidate2)
    return new_scores, best_candidate, new_sum_score

#f = open("candidates.txt", "a")
#g = open("generations.csv", "a")
generation = 0
best_fitness = 0
best_candidate = ()
candidates = generate_initial_candidates()
scores, best_candidate, score_sum = score_candidates(candidates)

while(True):
    generation += 1
#    scores, best_candidate, score_sum = score_candidates(candidates)
#    f.write(f"{generation}, {scores}\n")
    best_fitness = scores[best_candidate]
    if (best_fitness == BEST_FITNESS):
        break
    if (generation % REPORT_FREQUENCY == 0):
#        g.write(f"{generation},{best_fitness},{best_candidate}\n")
        print(f"Generation: {generation}   Best Fitness: {best_fitness}  Best Candidate: {best_candidate}")
    scores, best_candidate, score_sum = generate_next_generation(scores, score_sum)    

#g.write(f"{generation},{best_fitness},{best_candidate}\n")
print_board(best_candidate)
print(f"Generation: {generation}   Best Fitness: {best_fitness}  Best Candidate: {best_candidate}")

#f.write(f"Generation: {generation}  Solution: {best_candidate}")
#f.close()
#g.close()
