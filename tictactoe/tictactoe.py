"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    if board == initial_state():
        return X

    for row in board:
        for elm in row:
            if elm == X:
                x_count += 1
            elif elm == O:
                o_count += 1
    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_available = set()
    action = (0, 0)

    # if terminal(board) == True:
    #     return None
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                action = (i, j)
                action_available.add(action)
    
    return action_available

from copy import deepcopy

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)

    # acts_available = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

    if (actions(new_board) != None) and (action not in actions(new_board)):
        raise ValueError('Action not possible')

    player_current = player(new_board)

    if player_current == X:
        new_board[action[0]][action[1]] = X
    else:
        new_board[action[0]][action[1]] = O
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if (board[i][0] == board[i][1]) and (board[i][0] == board[i][2]):
            return board[i][0]
    
    for j in range(len(board[0])):
        if (board[0][j] == board[1][j]) and (board[0][j] == board[2][j]):
            return board[0][j]
    
    if (board[0][0] == board[1][1]) and (board[1][1] == board[2][2]):
        return board[0][0]
    
    if (board[0][2] == board[1][1]) and (board[1][1] == board[2][0]):
        return board[1][1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in board:
        for elm in row:
            if elm == EMPTY:
                return False
     
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


import random

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return winner(board)
    
    
    frontier = []
    nodes  = {}
    explored_node = []
    terminal_status = bool
    terminal_nodes  = []
    #  return all action can do
    available_act = list(actions(board)) 

    # init state node or origin node
    nodes[0] = {
        'parrent': None, 
        'action': None, 
        'result': board, 
        'terminal': False, 
        'utility': None,
        'children': []
    }

    print(nodes[0])

    node_key = 1

    for action in available_act:
        node_result = result(board, action)
        terminal_status = terminal(node_result)
        if terminal_status == True:
            board_ultility = utility(node_result)
            terminal_nodes.append(node_key)
        else:
            board_ultility = 0
        
        nodes[node_key] = {
            'parent': 0,
            'action': action,
            'result': node_result,
            'terminal': terminal_status,
            'utility': board_ultility,
            'children': []
        }
        # append children id
        populated_node_parentID = nodes[node_key]['parent']
        # get parent node
        populated_node_parent   = nodes[populated_node_parentID]

        # childrenList = populate_node_parent['children]
        populated_node_parent['children'].append(node_key)
        frontier.append(node_key)
        node_key += 1
    
    explored_node.append(node_key)

    get_child = nodes[0]['children']

    if len(get_child) == 9:
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        move    = random.choice(corners)
        return move
    
    # print(nodes)
    # print(frontier)

    while len(frontier) > 0:
        node_num = frontier.pop(0)
        explored_node.append(node_num)
        draw_node = nodes[node_num]
        # node result is current board
        node_board = draw_node['result']

        new_acts = list(actions(node_board)) #TypeError: 'NoneType' object is not iterable when play as O
        node_key = len(nodes)
        
        if draw_node['terminal'] == True:
            # should not consider children anymore
            for act in new_acts:
                # In reality this not even affecting
                node_key += 1
            continue
        else:
            for act in new_acts:
                node_result     = result(node_board, act)
                terminal_status = terminal(node_result)
                if terminal_status == True:
                    board_ultility = utility(node_result)
                    terminal_nodes.append(node_key)
                else:
                    board_ultility = 0
                
                nodes[node_key] = {
                    'parent': node_num,
                    'action': act,
                    'result': node_result,
                    'terminal': terminal_nodes,
                    'utility': board_ultility,
                    'children': []
                }
                # append children id
                populated_node_parentID = nodes[node_key]['parent']
                populated_node_parent   = nodes[populated_node_parentID]

                populated_node_parent['children'].append(node_key)
                node_key += 1
    
    #  Traceback utilities
    total_nodes = len(nodes)
    node_check  = len(nodes) - 1

    for n in range(total_nodes):
        # get relevant node's data
        node = nodes[node_check]
        node_utility = node['utility']
        node_children = node['children']

        if len(node_children) == 0:
            node_check -= 1
            continue

        node_board = node['result']
        next_player = player(node_board)

        # split cases X and O
        if next_player == X:
            set_point = - math.inf
            for child in node_children:
                child_node_utility = nodes[child]['utility']

                if child_node_utility > set_point:
                    set_point = child_node_utility
                    node['utility'] = child_node_utility
                else:
                    pass
        
        elif next_player == O:
            set_point = math.inf
            for child in node_children:
                child_node_utility = nodes[child]['utility']
                if child_node_utility < set_point:
                    set_point = child_node_utility
                    node['utility'] = child_node_utility
                else:
                    pass
        
        else:
             raise NameError('No Player Found')
        
        node_check -= 1
    
    # last_index = nodes[len(node) - 1]

    next_player = player(board)
    best_play   = None
    main_child  = nodes[0]['children']

    best_child_count = math.inf
    if next_player == X:
        set_point = - math.inf
        for child in main_child:
            node = nodes[child]
            util = node['utility']
            node_child_count = len(node['children'])
            if (util >= set_point) and (node_child_count <= best_child_count):
                set_point = util
                best_play = child
    else:
        set_point = math.inf
        for child in main_child:
            node = nodes[child]
            util = node['utility']
            node_child_count = len(node['children'])
            if (util <= set_point) and (node_child_count <= best_child_count):
                set_point = util
                best_play = child
    
    return nodes[best_play]['action']