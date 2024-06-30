import copy

# Node class to store board state data
class Node:
    def __init__(self, data, player, value, parent, height):
        self.height = height
        self.parent = parent
        self.data = data
        self.player = player
        self.children = []
        self.value = value

def getMove(state):
    board = dict()
    rows = state.split(",")
    player1Moves = 0
    player2Moves = 0

    # Parse board
    i = 1
    for column in rows:
        row = []
        states = column.split(" ")
        for state in states:
            if state == '1':
                player1Moves += 1
            elif state == '2':
                player2Moves += 1
            row.append(state)
        board[i] = row
        i += 1

    # Create tree of game states
    startPlayer = 1
    if player1Moves > player2Moves:
        startPlayer = 2
    start = Node(board, startPlayer, checkCompletion(board), None, 0)
    createTree(start)
    
    found = []
    if startPlayer == 1:
        v, node = maxValueAB(start, float("-inf"), float("inf"), found)
    else:
        v, node = minValueAB(start, float("-inf"), float("inf"), found)

    # Print Results
    path = backTrace(node)
    nextBoard = path[1]

    for row in nextBoard:
        j = 0
        for spot in nextBoard[row]:
            if spot != board[row][j]:
                return row - 1, j
            j += 1

    # if checkCompletion(node.data) > 0:
    #     print("Winner: Player 1")
    # else:
    #     print("Winner: Player 2")

    # print("Number of game tree nodes:", len(found))

    # print("Sequence of board states:")
    # for board in path:
    #     print("[[" +' '.join(board[1]) + "]")
    #     print(" [" + ' '.join(board[2]) + "]")
    #     print(" [" + ' '.join(board[3]) + "]]")
    #     print("------------")
    
    return

# Creates a tree of possible game states
def createTree(current):
    # Return if terminal state
    if current.value != 0:
        return

    i = 1
    for row in current.data:
        j = 0
        for item in current.data[row]:
            # Create the next possible board
            if item == '0':
                nextBoard = copy.deepcopy(current.data)
                nextPlayer = 1
                if current.player == 1:
                    nextBoard[i][j] = '1'
                    nextPlayer = 2
                else:
                    nextBoard[i][j] = '2'
                
                # Add node as child and recurse
                node = Node(nextBoard, nextPlayer, checkCompletion(nextBoard) / (current.height + 1), current, current.height + 1)
                current.children.append(node)
                createTree(node)
            j += 1
        i += 1

# Check if terminal node
def checkCompletion(board):

    # Use emptyCount for utility
    emptyCount = 1
    # for row in board:
    #     emptyCount += board[row].count('0')

    # Check if win by row
    for row in board:
        if board[row].count('1') == 3:
            return 1 * emptyCount
        if board[row].count('2') == 3:
            return -1 * emptyCount
    
    # Check if win by column
    for i in range(3):
        column = [board[1][i], board[2][i], board[3][i]]
        if column.count('1') == 3:
            return 1 * emptyCount
        if column.count('2') == 3:
            return -1 * emptyCount

    # Check if win by diagonal
    leftRight = [board[1][0], board[2][1], board[3][2]]
    rightLeft = [board[3][0], board[2][1], board[1][2]]
    if leftRight.count('1') == 3 or rightLeft.count('1') == 3:
        return 1 * emptyCount
    if leftRight.count('2') == 3 or rightLeft.count('2') == 3:
        return -1 * emptyCount

    return 0

# Get path from start node to current
def backTrace(node):
    path = [node.data]
    while node.parent != None:
        node = node.parent
        path.append(node.data)

    path = list(reversed(path))
    return path

# MinMax Search Max Value
def maxValue(node, found):
    # Add node to list of found nodes
    found.append(node)

    # Return if terminal node
    if node.value != 0:
        return node.value, node

    # If terminal node with no value, return draw
    if len(node.children) == 0:
        return 0, node

    # Continue MinMax Search
    v = float('-inf')
    bestNode = None
    for child in node.children:
        # Update current max value and node
        value, nextNode = minValue(child, found)
        if value > v:
            bestNode = nextNode
            v = value

    return v, bestNode

# MinMax Search Min Value
def minValue(node, found):
    # Add node to list of found nodes
    found.append(node)

    # Return if terminal node
    if node.value != 0:
        return node.value, node

    # If terminal node with no value, return draw
    if len(node.children) == 0:
        return 0, node

    # Continue MinMax Search
    v = float('inf')
    bestNode = None
    for child in node.children:
        # Update current min value and node
        value, nextNode = maxValue(child, found)
        if value < 0:
            pass
        if value < v:
            bestNode = nextNode
            v = value

    return v, bestNode

# Alpha-Beta Pruning Max Value
def maxValueAB(node, alpha, beta, found):
    # Add node to list of found nodes
    found.append(node)

    # Return if terminal node
    if node.value != 0:
        return node.value, node

    # If terminal node with no value, return draw
    if len(node.children) == 0:
        return 0, node

    # Continue MinMax Search
    v = float('-inf')
    bestNode = None
    for child in node.children:
        # Update current max value and node
        value, nextNode = minValueAB(child, alpha, beta, found)
        if value > v:
            bestNode = nextNode
            v = value

        # Prune tree if current value is greater than beta
        if v >= beta:
            return v, bestNode

        # Update alpha to current max
        alpha = max(alpha, v)

    return v, bestNode

# Alpha-Beta Pruning Min Value
def minValueAB(node, alpha, beta, found):
    # Add node to list of found nodes
    found.append(node)

    # Return if terminal node
    if node.value != 0:
        return node.value, node

    # If terminal node with no value, return draw
    if len(node.children) == 0:
        return 0, node

    # Continue MinMax Search
    v = float('inf')
    bestNode = None
    for child in node.children:
        # Update current min value and node
        value, nextNode = maxValueAB(child, alpha, beta, found)
        if value < v:
            bestNode = nextNode
            v = value

        # Prune tree if current value is less than or equal to alpha
        if v <= alpha:
            return v, bestNode

        # Update beta to current min
        beta = min(beta, v)

    return v, bestNode
