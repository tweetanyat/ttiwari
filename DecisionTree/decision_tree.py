
def parse_file (filepath):
    data = []
    flag = 0
    fin = open(filepath)
    lines = fin.readlines()

    for line in lines:
        flag = 0
        row = []
        entry = str(line.strip()).split(',')
        for e in entry:            
            if '?' in e:
                flag = 1
                break
        if flag == 1:
            pass
        else:
            for e in entry: 
                row.append(e)
            data.append(row)
        
    fin.close()
    print data
    
parse_file('F:\Study\MS\AI\Assignments\hw5\hw5\decision tree\crx.data.txt')
    