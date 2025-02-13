import copy
import random
import multiprocessing as mp
import time

QUEENS = 8
CANDIDATE_COUNT = 50
MUTAGEN = 1/(QUEENS/2)
REPORT_FREQUENCY = 1
TRIALS = 1
SHOW_BOARD = True
OUTPUT = False

BOARD = [['_' for row in range(QUEENS)] for col in range(QUEENS)]       
BEST_FITNESS = int((QUEENS * (QUEENS-1)) / 2)
#ODD_OR_EVEN = sum(range(QUEENS)) % 2 # 0 if even, 1 if odd

# Map of CANDIDATE_COUNTS to be used in a trial
candidate_count_list = {
#    0 : 25,
    1 : 50,
#    2 : 75,
#    3 : 100,
#    4 : 250,
#    5 : 500,
#    6 : 750,
#    7 : 1000,
#    8 : 1250,
#    9 : 1500,
#    10 : 1750,
#    11 : 2500,
#    12 : 3750,
#    13 : 5000,
#    14 : 7500,
#    15 : 10000
}

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
    return new_candidate1, new_candidate2

def mutate(candidate):
    for c in range(0, QUEENS):
        if (random.random() < MUTAGEN):
            candidate[c] = random.randrange(0,QUEENS)
    return candidate

# def parity_check(candidate):
#     if (sum(candidate) % 2 != ODD_OR_EVEN):
#         index = random.randrange(0, QUEENS)
#         candidate[index] += 1
#         if (candidate[index] >= QUEENS):
#             candidate[index] = ODD_OR_EVEN
# #        candidate[index] = index
# #        candidate = parity_check(mutate(candidate))
#     return candidate

def create_candidates(candidates):
    candidates[0], candidates[1] = splice(candidates[0], candidates[1])
    candidates[0] = mutate(candidates[0])
    candidates[1] = mutate(candidates[1])
#    candidates[0] = parity_check(candidates[0])
#    candidates[1] = parity_check(candidates[1])
    candidates.append(test_fitness(candidates[0]))
    candidates.append(test_fitness(candidates[1]))
    return candidates

def generate_next_generation(scores, sum_scores, prev_best_candidate, prev_best_score):
    next = 0
    scores_hist = {}
    best_score = 0
    best_candidate = []
    new_sum_score = 0
    new_scores = {}
    candidate_list = []

    for candidate in scores:
        p = int((scores[candidate]/sum_scores)*CANDIDATE_COUNT*10)
        for i in range(next,next+p):
            scores_hist[i] = candidate
        next = next+p    
    for q in range(0,CANDIDATE_COUNT-2,2):
        new_candidate1 = list(scores_hist[random.randrange(0,len(scores_hist))])
        new_candidate2 = list(scores_hist[random.randrange(0,len(scores_hist))])
        candidate_list.append([new_candidate1, new_candidate2])
        candidate_list.append([list(prev_best_candidate), list(prev_best_candidate)])
    new_candidates = pool.map(create_candidates, candidate_list)

    for q in range(0,int(CANDIDATE_COUNT/2)):
        new_sum_score += new_candidates[q][2]
        new_scores[tuple(new_candidates[q][0])] = new_candidates[q][2]
        if (new_scores[tuple(new_candidates[q][0])] > best_score):
            best_score = new_candidates[q][2]
            best_candidate = tuple(new_candidates[q][0])

        new_sum_score += new_candidates[q][3]
        new_scores[tuple(new_candidates[q][1])] = new_candidates[q][3]
        if (new_scores[tuple(new_candidates[q][1])] > best_score):
            best_score = new_candidates[q][3]
            best_candidate = tuple(new_candidates[q][1])           
    return new_scores, best_candidate, new_sum_score

def run_test():
    generation = 0
    best_fitness = 0
    avg_fitness = []
    best_candidate = ()
    candidates = generate_initial_candidates()
    scores, best_candidate, score_sum = score_candidates(candidates)
    avg_fitness.append(score_sum / CANDIDATE_COUNT)

    while(True):
        generation += 1
    #    f.write(f"{generation}, {scores}\n")
        best_fitness = scores[best_candidate]
        if (best_fitness == BEST_FITNESS):
            break
        if (generation % REPORT_FREQUENCY == 0):
#            g.write(f"{generation},{best_fitness},{best_candidate}\n")
            print(f"Generation: {generation}   Best Fitness: {best_fitness}   Avg Fitness: {avg_fitness[generation-1]}   Best Candidate: {best_candidate}")
        scores, best_candidate, score_sum = generate_next_generation(scores, score_sum, best_candidate, best_fitness) 
        avg_fitness.append(score_sum / CANDIDATE_COUNT)
#        if (OUTPUT == True):
#            g.write(f"{generation},{best_fitness},{avg_fitness[generation]},{best_candidate}\n")
    if (SHOW_BOARD == True):
        print_board(best_candidate)
    print(f"Generation: {generation}   Best Fitness: {best_fitness}  Best Candidate: {best_candidate}")
#    if (OUTPUT == True):
#        g.write(f"{generation},{best_fitness},{best_candidate}\n\n\n")
#    f.write(f"Generation: {generation}  Solution: {best_candidate}")
    return generation

if (OUTPUT == True):
    f = open("candidates.txt", "a")
#    g = open("generations.csv", "a")

if __name__ == '__main__':
    mp.freeze_support()
    pool = mp.Pool(mp.cpu_count())
    for key in candidate_count_list:
        generation_count_total = 0
        search_time_total = 0
        CANDIDATE_COUNT = candidate_count_list[key]
        for i in range(TRIALS):
            start_time = time.perf_counter()
            generation_count_total += run_test()
            end_time = time.perf_counter()
            search_time_total += end_time-start_time
        print()
        print(f"Queens: {QUEENS}  Candidate Count: {CANDIDATE_COUNT}  Mutagen: {round(MUTAGEN, 5)}  Trials: {TRIALS}")
        print(f"Average number of generations: {round(generation_count_total/TRIALS, 3)}   Average search time: {round(search_time_total/TRIALS, 3)}")
        print()
        if (OUTPUT == True):
            f.write(f"Queens: {QUEENS}  Candidate Count: {CANDIDATE_COUNT}  Mutagen: {round(MUTAGEN, 5)}  Trials: {TRIALS}\n")
            f.write(f"Average number of generations: {round(generation_count_total/TRIALS, 3)}   Average search time: {round(search_time_total/TRIALS, 3)}\n\n")
if (OUTPUT == True):
    f.close()
 #   g.close()
