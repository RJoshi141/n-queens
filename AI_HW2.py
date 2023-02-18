import random 

#INPUTS
m = 10
reach = 6
start_state = [(1, 7), (2, 4), (2, 5), (3, 8), (4, 1), (4,6), (5, 5), (6, 2), (7,2), (8,3)]

def num_conflicts(state, reach):
    """Counts the number of conflicts in the given state"""
    conflicts = 0
    for i in range(len(state)):
        for j in range(i+1, len(state)):
            if state[i][0] == state[j][0] or state[i][1] == state[j][1]:
                conflicts += 1
            elif abs(state[i][0]-state[j][0]) == abs(state[i][1]-state[j][1]):
                conflicts += 1
            elif abs(state[i][0] - state[j][0]) <= reach and abs(state[i][1] - state[j][1]) <= reach and abs(state[i][0] - state[j][0]) != abs(state[i][1] - state[j][1]):
                conflicts += 1

    return conflicts


def new_neighbors(state):
    """Generates all neighboring states of the given state"""
    neighbors = []
    for i in range(len(state)):
        for j in range(1, 10):
            if (i+1, j) != state[i]:
                neighbor = state[:i] + [(i+1, j)] + state[i+1:]
                neighbors.append(neighbor)
    return neighbors


def best_neighbor(neighbors, reach):
    """Returns the neighbor with the lowest number of conflicts"""
    #If there is only one best neighbor with the lowest number of conflicts, it will be returned. 
    #If there are multiple best neighbors with the same number of conflicts, one of them 
    #will be chosen at random using the random.choice() function.
    best_neighbors = []
    best_conflicts = float("inf")
    for neighbor in neighbors:
        conflicts = num_conflicts(neighbor, reach)
        if conflicts < best_conflicts:
            best_neighbors = [neighbor]
            best_conflicts = conflicts
        elif conflicts == best_conflicts:
            best_neighbors.append(neighbor)
    return random.choice(best_neighbors), best_conflicts


def hill_climbing(start_state, r, max_transitions=60, sideways_moves=0):
    current_state = start_state
    current_conflicts = num_conflicts(current_state, r)
    transitions = 0
    examined = 0

    while True:
        if current_conflicts == 0:
            return current_state, 0, transitions, examined, "Solution found"

        if transitions >= max_transitions:
            return current_state, current_conflicts, transitions, examined, "Maximum transitions reached"

        neighbors = new_neighbors(current_state)
        examined += len(neighbors)
        next_state, next_conflicts = best_neighbor(neighbors, r)

        if next_conflicts >= current_conflicts:
            if transitions < sideways_moves:
                # Sideways move
                current_state = next_state
                current_conflicts = next_conflicts
            else:
                return current_state, current_conflicts, transitions, examined, "Local minimum reached"
        else:
            current_state = next_state
            current_conflicts = next_conflicts
            transitions += 1


#CHESS BOARD
def chess_board(state):
    n = len(state)
    board = []
  
    for i in range(n):
        row = ['.'] * n
        row[state[i][1]-1] = 'Q'
        board.append(row)

    for row in board:
        print(' '.join(row))


#OUTPUTS
# Starting state
print("STARTING STATE:")
print(start_state)
chess_board(start_state)
print("Number of conflicts:", num_conflicts(start_state, reach))
print()

# Next 4 states
state = start_state
for i in range(4):
    neighbors = new_neighbors(state)
    next_state, next_conflicts = best_neighbor(neighbors, reach)
    print("NEXT STATE:")
    print(next_state)
    chess_board(next_state)
    
    print("Number of conflicts:", next_conflicts)
    state = next_state
    print()

# Solution state, if FOUND and if NOT Found
solution_state, conflicts, transitions, examined, reason = hill_climbing(start_state, reach, max_transitions=60)

#If there is a solution
if reason == "Solution found": 
    print("SOLUTION STATE:")
    chess_board(solution_state)
    print("Number of conflicts:", conflicts)
  
#if there is no solution
elif reason != "Solution found": 
    print(f"NO SOLUTION FOUND. \nReason: {reason}.")
    print(f"Search stopped at state: \n{solution_state}")
    chess_board(solution_state)
    print("Number of conflicts:", conflicts)

# Total number of state transitions
print(f"Total number of state transitions: {transitions}")

# Total number of neighboring states examined
print(f"Total number of neighboring states examined: {examined}")
