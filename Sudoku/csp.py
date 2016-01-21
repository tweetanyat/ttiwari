###########################################
# you need to implement five functions here
###########################################
import time
import copy
import Queue as Q
import random
#Global variables
n_value = 0
m_value = 0
k_value = 0
# Will contain a dictionary, the 'key' is the empty variables and the 'value' is a list of the variables domain
dict = {}
# Used for consistency check
check = 0


def constructBoard(filename):
    '''
    Used to construct the board from the given specifications in the input file
    Returns the initial game board
    '''
    count = 0
    global n_value, m_value, k_value
    with open (filename)as f:
        board= []
        for lines in f:
            column = []
            count = count + 1
            rows = lines.rstrip('\n').rstrip(';')
            cells = rows.split(',')
            if(count == 1):
                n_value = int(cells[0])
                m_value = int(cells[1])
                k_value = int(cells[2])
                if not(n_value == m_value * k_value):
                    exitGame()
            else:
                for cell in cells:
                    if("-" in cell):
                        column.append(0)
                    else:
                        column.append(int(cell.strip()))
            if(count != 1):
                board.append(column)
            count = count + 1
        return board

def exitGame():
    '''
    Function can be used to terminate a program
    '''
    raise ValueError('Not a valid board configuration. Exiting!')

def isValidMove(board, row, column, value):
    '''
    This function will return 0 in case of an invalid move and 1 if the move is valid

    '''
    #Check if value is valid across row
    for j in range(0, n_value):
        if board[row][j] == value:
            return 0

    #Check if value is valid across column
    for i in range(0, n_value):
        if board[i][column] == value:
            return 0

    #Check if value is valid in grid
    gridStartRow = row - (row % m_value)
    gridStartColumn = column - (column % k_value)

    for i in range(0, m_value):
        for j in range(0, k_value):
            if board[i + gridStartRow][j + gridStartColumn] == value:
                return 0

    return 1


def isCompleteBoard(board):
    '''
    Used in backtracking to check if the board is completed
    :param board:
    :return: -1,-1 if the board is completed
    '''
    for i in range(0,n_value):
        for j in range(0,n_value):
            if (board[i][j] == 0):
                return i,j

    return -1,-1

def backtrackSudoku(board):
    '''
    Helper Function to run the backtrack
    :param board:
    :return: 1 on success, 0 on failure
    '''
    global check
    emptyRow,emptyColumn = isCompleteBoard(board)

    if emptyRow == -1:
        return 1

    for value in range(1,n_value + 1):
        if isValidMove(board, emptyRow, emptyColumn, value):
            check =  check + 1
            board[emptyRow][emptyColumn] = value
            if backtrackSudoku(board):
                return 1

            board[emptyRow][emptyColumn] = 0

    return 0


def backtracking(filename):
    '''
    Main Backtracking Function
    :param filename:
    :return:Board Solution on Success, and empty list on failure
    '''
    global check
    check = 0
    board = constructBoard(filename)
    ret = backtrackSudoku(board)

    if ret:
        print 'Sudoku problem solved'
        return (board, check)
    else:
        print 'Sudoku problem has no solution'
        return ([[]],0)

def getVal(board,row,column):
    '''
    getVal is used to calculate the domain of a variable(row,column)
    :param board:
    :param row:
    :param column:
    :return:The list with the domain values as entries
    '''
    domainVal = list(range(1, n_value+1))
    for j in range(0, n_value):
        if board[row][j] in domainVal:
            domainVal.remove(board[row][j])

#    Check if value is valid across column
    for i in range(0, n_value):
        if board[i][column] in domainVal:
            domainVal.remove(board[i][column])

    gridStartRow = row - (row % m_value)
    gridStartColumn = column - (column % k_value)

    for i in range(0, m_value):
        for j in range(0, k_value):
            if board[i + gridStartRow][j + gridStartColumn] in domainVal:
                domainVal.remove(board[i + gridStartRow][j + gridStartColumn])

    return domainVal

def getMRVList(board):
    '''
    Creates a priority queue, which has the length of domain, the domain and the variable coordinates
    :param board:
    :return:The priority queue
    '''
    q = Q.PriorityQueue()
    for i in range(0,n_value):
        for j in range(0,n_value):
            if (board[i][j] == 0):
                values = getVal(board,i,j)
                q.put((len(values),values,i,j))
    return q

def backtrackMRVSudoku(board):
    '''
    Helper Function to run the backtrack MRV
    :param board:
    :return: 1 on success, 0 on failure
    '''

    global check
    #mrvList contains the minimum entry returned by tge
    mrvList = getMRVList(board)

    if mrvList.empty():
        return 1
    check = check + 1
    length,values,emptyRow,emptyColumn = mrvList.get()
    for value in values:
        # check = check + 1
        board[emptyRow][emptyColumn] = value

        if backtrackMRVSudoku(board):
            return 1
        board[emptyRow][emptyColumn] = 0

    return 0

def backtrackingMRV(filename):
    '''
    Main Backtracking Function with MRV
    :param filename:
    :return:Board Solution on Success, and empty list on failure
    '''

    global check
    check = 0
    board = constructBoard(filename)
    ret = backtrackMRVSudoku(board)
    if ret:
        print 'Sudoku problem solved'
        return (board, check)
    else:
        print 'Sudoku problem has no solution'
        return ([[]], 0)

def getMRVfwdList(board):
    '''
    getMRVfwdList initializes the dict(the 'key' is the empty variables and the 'value' is a list of the variables domain)
    :param board:
    :return:The dict which will be used by many functions
    '''
    global dict
    for i in range(0,n_value):
        for j in range(0,n_value):
            if (board[i][j] == 0):
                values = getVal(board,i,j)
                dict[(i, j)] = values
    return dict

def removeConflict(board, row, column, value):
    '''
    removeConflict : removes values from other conflicting variables in the dictionary
    :param board:
    :param row:
    :param column:
    :param value: a domain entry from the variable at row,column
    :return: Returns a 0 if a variables domain reduces to 0 , else 1
    '''
    global dict
    #Remove domain entries from variables in the same row
    for j in range(0, n_value):
        if board[row][j] == 0:
            if not (j == column):
                colConflict = dict[(row,j)]
                if value in colConflict:
                    dict[(row,j)].remove(value)
                    if len(dict[(row,j)]) == 0:
                        return 0
    #Remove domain entries  from variables in the same column
    for i in range(0, n_value):
        if board[i][column] == 0:
            if not (i == row):
                rowConflict = dict[(i,column)]
                if value in rowConflict:
                    dict[(i,column)].remove(value)
                    if len(dict[(i,column)]) == 0:
                        return 0

    gridStartRow = row - (row % m_value)
    gridStartColumn = column - (column % k_value)

    #Remove domain entries  from variables in the same grid
    for i in range(0, m_value):
        for j in range(0, k_value):
            if board[i + gridStartRow][j + gridStartColumn] == 0:
                if not ((i + gridStartRow == row) and (j + gridStartColumn == column)):
                    boxConflict = dict[(i + gridStartRow,j + gridStartColumn)]
                    if value in boxConflict:
                        dict[(i + gridStartRow,j + gridStartColumn)].remove(value)
                        if len(dict[(i + gridStartRow,j + gridStartColumn)]) == 0:
                            return 0
    return 1

def backtrackMRVfwdSudoku(board):
    '''
    Helper Function to run the backtrack MRV with Forward Checking
    :param board:
    :return: 1 on success, 0 on failure
    '''

    global check,dict
    mrvList = getMRVList(board)

    if mrvList.empty():
        return 1
    check = check + 1
    length, values, emptyRow, emptyColumn = mrvList.get()
    for value in values:
        temp = copy.deepcopy(dict)
        if removeConflict(board, emptyRow, emptyColumn, value):
            board[emptyRow][emptyColumn] = value
            if backtrackMRVfwdSudoku(board):
                return 1
        dict = copy.deepcopy(temp)
        board[emptyRow][emptyColumn] = 0
    return 0

def backtrackingMRVfwd(filename):
    '''
    Main Backtracking Function with MRV and forward checking
    :param filename:
    :return:Board Solution on Success, and empty list on failure
    '''
    global check
    check = 0
    board = constructBoard(filename)
    d = getMRVfwdList(board)

    ret = backtrackMRVfwdSudoku(board)

    if ret:
        print 'Sudoku problem solved'
        return (board, check)
    else:
        print 'Sudoku problem has no solution'
        return ([[]], 0)


def rmInconsistentValues(src, dest):
    '''
    rmInconsistentValues:Remove any inconsistent values obtained between arcs
    :param src:
    :param dest:
    :return:If a value was removed return 1, else 0
    '''
    global dict
    flag = 0
    srcList = copy.deepcopy(dict[src])

    for value in srcList:
        destList = copy.deepcopy(dict[dest])
        if value in destList:
            destList.remove(value)
        if len(destList) == 0:
            dict[src].remove(value)
            flag = 1
    return flag


def arcConsistentCheck(board, row, column):
    '''
    arcConsistentCheck: Reduces the domain of variables based on arc consistency
    :param board:
    :param row:
    :param column:
    :return:Makes changes to the global variable dict,so does not return anything
    '''
    global dict
    q = []
    for variable in dict:
        row, column = variable
        for j in range(0, n_value):
            if board[row][j] == 0:
                if not (j == column):
                    q.append(((row,column),(row,j)))
        for i in range(0, n_value):
            if board[i][column] == 0:
                if not (i == row):
                    q.append(((row,column),(i,column)))

        gridStartRow = row - (row % m_value)
        gridStartColumn = column - (column % k_value)

        for i in range(0, m_value):
            for j in range(0, k_value):
                if board[i + gridStartRow][j + gridStartColumn] == 0:
                    if not ((i + gridStartRow == row) and (j + gridStartColumn == column)):
                        q.append(((row,column),(i + gridStartRow,j + gridStartColumn)))
    while not (len(q) == 0):
        arc = q.pop(0)
        src,dest = arc
        arcRemoved = rmInconsistentValues(src, dest)
        rowSrc, colSrc = src
        rowDst, colDst = dest
        if arcRemoved:
            for j in range(0, n_value):
                if board[rowSrc][j] == 0:
                    if not (j == colSrc):
                        q.append(((rowSrc,j),src))

            for i in range(0, n_value):
                if board[i][colSrc] == 0:
                    if not (i == rowSrc):
                        q.append(((i,colSrc),src))

            gridStartRow = rowSrc - (rowSrc % m_value)
            gridStartColumn = colSrc - (colSrc % k_value)

            for i in range(0, m_value):
                for j in range(0, k_value):
                    if board[i + gridStartRow][j + gridStartColumn] == 0:
                        if not ((i + gridStartRow == rowSrc) and (j + gridStartColumn == colSrc)):
                            q.append(((i + gridStartRow,j + gridStartColumn),src))

        # for l in q:
        #     if dest in l:
        #         q.remove((dest,src))

def getMRVListDict():
    '''
    getMRVListDict: Function used to create a priority queue from the global dict , as the changes by arc consistency
    are done to the global dict
    :return:Returns the new updated priority queue
    '''
    global dict
    q = Q.PriorityQueue()
    for variable in dict:
        i,j = variable
        values = dict[variable]
        q.put((len(values),values,i,j))
    return q


def backtrackMRVcpSudoku(board):
    '''
    Helper Function to run the backtrack,MRV with constraint propagation
    :param board:
    :return: 1 on success, 0 on failure
    '''

    global check, dict
    mrvList = getMRVListDict()

    if mrvList.empty():
        return 1

    length, values, emptyRow, emptyColumn = mrvList.get()
    for value in values:
        temp = copy.deepcopy(dict)
        dict[(emptyRow,emptyColumn)] = [value]
        arcConsistentCheck(board, emptyRow, emptyColumn)
        check = check + 1
        board[emptyRow][emptyColumn] = value
        if value in dict[(emptyRow, emptyColumn)]:
            dict[(emptyRow, emptyColumn)].remove(value)
        if len(dict[(emptyRow,emptyColumn)]) == 0:
            del dict[(emptyRow,emptyColumn)]
        if backtrackMRVcpSudoku(board):
                return 1
        dict = copy.deepcopy(temp)
        board[emptyRow][emptyColumn] = 0

    return 0


def backtrackingMRVcp(filename):
    '''
    Main Backtracking Function with MRV and constraint propagation
    :param filename:
    :return:Board Solution on Success, and empty list on failure
    '''
    global check, dict
    dict = {}
    check = 0
    board = constructBoard(filename)
    d = getMRVfwdList(board)
    ret = backtrackMRVcpSudoku(board)

    if ret:
        print 'Sudoku problem solved'
        return (board, check)
    else:
        print 'Sudoku problem has no solution'
        return ([[]], 0)

def getConflicts(board,variable,value):
    '''
    getConflicts: Calculates the conflict  a value can cause when added to variable
    :param board:
    :param variable:
    :param value: The Domain Value
    :return:Returns the conflict count
    '''
    count = 0
    row,column = variable
    for j in range(0, n_value):
        if board[row][j] == value:
            if not (j == column):
                count = count + 1

#    Check if value is valid across column
    for i in range(0, n_value):
        if board[i][column] == value:
            if not (i == row):
                count = count + 1

    gridStartRow = row - (row % m_value)
    gridStartColumn = column - (column % k_value)

    for i in range(0, m_value):
        for j in range(0, k_value):
            if board[i + gridStartRow][j + gridStartColumn] == value:
                if not ((i + gridStartRow == row) and (j + gridStartColumn == column)):
                    count = count + 1

    return count

def getminConflictsVal(board,variable):
    '''
    getminConflictsVal: Calculates the minimum conflicting value the given variable
    :param board:
    :param variable:
    :return:The value for which the variable has minimum conflict and also the conflicting count
    '''
    values = dict[variable]
    existingVal=[]
    row, column = variable
    for j in range(0, n_value):
        existingVal.append(board[row][j])
    minimum = -1
    value = 0
    flag = 0
    for val in values:
        if val in existingVal:
            continue
        count = getConflicts(board,variable,val)
        if minimum == -1:
            minimum = count
            value = val
        elif count < minimum:
            minimum = count
            value = val

    return value,minimum

def assignVariables(board):
    '''
    assignVariables: Sets the base for the min conflict algorithm, by assigning values to variables intelligently
    :param board:
    :return:
    '''
    global dict
    singleElement = []
    for variable in dict:

        row,column = variable
        if len(dict[variable]) == 1:
            singleElement.append(variable)
            board[row][column] = dict[variable][0]
        else:
            value,count = getminConflictsVal(board,variable)
            board[row][column] = value

    for s in singleElement:
        del dict[s]

    for row in board:
        if 0 in row:
            id = 0
            tmp = 0
            allVal = list(range(1, n_value+1))
            for val in row:
                if val == 0:
                    tmp = id
                id = id + 1
                if val in allVal:
                    allVal.remove(val)
            row[tmp] = allVal[0]

def isConflict(board):
    '''
    isConflict : Used to check if there are conflicting values in any of the variables
    :param board:
    :return:True if conflicts exists , else false
    '''

    global dict
    for j in range(0, n_value):
        for i in range(0, n_value):
            count = getConflicts(board,(j,i),board[j][i])
            if count > 0:
                return True
    return False

def getswapVariable(board,variable):
    '''
    getswapVariable: Returns a variables with less number of conflicts w.r.t to value in the variable parameter
    :param board:
    :param variable:
    :return:The variable with less number of conflicts fot the value in the variable parameter.
    '''
    global dict
    row, column = variable
    validTuples = []
    value = board[row][column]
    minimumConflicts = getConflicts(board, variable, value)
    swapVariable = variable

    for d in dict:
        x, y = d
        if x == row:
            validTuples.append(d)

    for v in validTuples:
        count = getConflicts(board, v, value)
        if minimumConflicts > count:
            minimumConflicts = count
            swapVariable = v

    return swapVariable

def minConflict(filename):
    '''
    Main Function for minconflict csp
    :param filename:
    :return:Board Solution on Success, and empty list on failure
    '''
    global check, dict
    check = 0
    dict = {}
    board = constructBoard(filename)
    d = getMRVfwdList(board)
    assignVariables(board)
    i = 0
    temp = 0
    prev = (20,20)
    while i < 50000:
        if not isConflict(board):
            print 'Sudoku problem solved'
            return (board, check)

        variable = random.sample(dict, 1)
        i = i + 1
        row, column = variable[0]
        swapVariable = getswapVariable(board,variable[0])
        if not (variable[0] == swapVariable):
            swapRow, swapColumn = swapVariable
            temp = copy.deepcopy(board[swapRow][swapColumn])
            board[swapRow][swapColumn] = copy.deepcopy(board[row][column])
            board[row][column] = copy.deepcopy(temp)
    print 'No Solution to the problem'
    return ([[]], 0)