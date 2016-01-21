import sys
from itertools import product, starmap, islice, combinations
rows=0
columns=0
count = 0 

def parse_file(filepath):
    # read the layout file to the board array
    global rows,columns,count
    board = []
    fin = open(filepath)
    rows,columns = str(fin.readline()).split()
    rows = int(rows)
    columns = int(columns)
    count = 1000
    
    lines = fin.readlines()
    for line in lines:
        row =[]
        r = str(line.strip()).split(',')
        for element in r:
            if 'X' in element:
                row.append(count)
                count = count + 1
            else:
                row.append(int(element))
        board.append(row)
    fin.close()
    return board

def getExplored(board):
    exp =[]
    for i in xrange(rows):
        for j in xrange(columns):
            if board[i][j] < 1000:
                exp.append((i,j))
    return exp
                
def getNeighbors(grid, x, y):
    neighbors = []
    xi = (0, -1, 1) if 0 < x < len(grid) - 1 else ((0, -1) if x > 0 else (0, 1))
    yi = (0, -1, 1) if 0 < y < len(grid[0]) - 1 else ((0, -1) if y > 0 else (0, 1))
    ni = list(islice(starmap((lambda a, b: grid[x + a][y + b]), product(xi, yi)), 1, None))
    for ne in ni:
        if ne > 999:
            neighbors.append(ne)
    return neighbors

def convert2CNF(board, output):
    global count
    explored = getExplored(board)
    clauses = set()
    for val in explored:
        base = 0
        r,c = val
        mines = board[r][c]
        neighbors = getNeighbors(board,r,c)
        nVal = len(neighbors)
        kVal = mines
        if kVal == 0:
            base = 1
            for n in neighbors:
                clauses.add(-n)
                
        if kVal == nVal:
            base = 1
            for n in neighbors:
                clauses.add(n)
                        
        if not base:
            for subset1 in combinations(neighbors, len(neighbors) - kVal + 1):
                l1 = []
                for v1 in subset1:
                    l1.append(v1)
                clauses.add(tuple(l1))
            for subset in combinations(neighbors, kVal + 1):
                l = []
                for v in subset:
                    l.append(-1*v)
                clauses.add(tuple(l))
    fout = open(output, 'w')
    fout.write('p cnf %d %d\n' % (count - 1000, len(clauses)))
    for clause in clauses:
        fout.write(str(clause).replace(',','').replace('(','').replace(')','') + ' 0\n')

    fout.close()


    fout.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])