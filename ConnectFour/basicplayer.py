from util import memoize, run_search_function, INFINITY

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)
    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()

def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    bestval = []
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    for move, new_board in get_all_next_moves(board):
        val = min_value(new_board, depth - 1 , eval_fn)
        bestval.append((val,move))
        cost, column = max(bestval)
    return column


def min_value(board, depth , eval_fn=basic_evaluate):
    """
    Calculates the minimum value of a board
    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example
    """
    if is_terminal(depth, board):
        return -1*eval_fn(board) #Returning negative value to counter the -10000 returned for a max move(negamax variant)
    minVal = INFINITY
    for move, new_board in get_all_next_moves(board):
        minVal = min(minVal,max_value(new_board,depth - 1, eval_fn))
    return  minVal


def max_value(board, depth , eval_fn=basic_evaluate):
    """
    Calculates the minimum value of a board
    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example
    """
    if is_terminal(depth, board):
        return eval_fn(board)
    maxVal = -INFINITY
    for move, new_board in get_all_next_moves(board):
        maxVal = max(maxVal,min_value(new_board,depth - 1, eval_fn))
    return maxVal
        
def rand_select(board):
    """
    Pick a column by random
    """
    import random
    
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


def new_evaluate(board):  
    if board.is_game_over():
        return -1000
    else:
        #Get the total number of 2 and 3 length chains for the current player        
        length_2_current = board.longest_chain_2(board.get_current_player_id())
        length_3_current = board.longest_chain_3(board.get_current_player_id())
        score_current_player = (length_2_current * 1) + (length_3_current * 4) 
           
        #Get the total number of 2 and 3 length chains for the other  player
        length_2_other = board.longest_chain_2(board.get_other_player_id())
        length_3_other = board.longest_chain_3(board.get_other_player_id())
        score_other_player = (length_2_other * 1) + (length_3_other * 4) 
        
        #Return the weighted score by subtracting the value of the other player 
        return score_current_player - score_other_player

random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
