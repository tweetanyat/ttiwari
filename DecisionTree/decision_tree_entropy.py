import math
import numpy as np
import pandas as pd


class node(object):
    def __init__(self, value = None, children = [], result = "/",type = None):
        self.value = value
        self.children = children
        self.result = result
        self.type = type

main_columns = [x for x in range(0,16)]

def getDict(data,column):
    d =dict()
    for row in data:
        d.setdefault(row[column],[]).append(row)
    return d

def calculate_hx(data):
    count_yes = 0
    count_no = 0
    for row in data:
        if '+' in row[-1]:
            count_yes = count_yes + 1
        if '-' in row[-1]:
            count_no = count_no + 1
    total = count_no + count_yes
    p_yes = float(count_yes)/ float(total)
    p_no = float(count_no) / float(total)
    if (p_yes == 0):
        p_yes = 0.0001
    if (p_no == 0):
        p_no = 0.0001
    entropy = -p_yes * math.log(p_yes,2) - p_no * math.log(p_no,2)
    return entropy

def calculate_ig(data, column):
    count_yes = 0
    count_no = 0
    cond_entropy = []
    prob_key = []
    hxy = 0
    d = getDict(data, column)
        
    for key in d:
        count_yes = 0
        count_no = 0
        for row in d[key]:    
            if '+' in row[-1]:
                count_yes = count_yes + 1
            if '-' in row[-1]:
                count_no = count_no + 1

        p_yes = count_yes/float(len(d[key]))
        p_no = count_no/float(len(d[key]))
        if (p_yes == 0):
            p_yes = 0.0001
        if (p_no == 0):
            p_no = 0.0001
        entropy = -p_yes * math.log(p_yes,2) - p_no * math.log(p_no,2)
        cond_entropy.append(entropy)
        prob_key.append(len(d[key])/float(len(data)))
#     print d
    for i in range(0, len(cond_entropy)):
        hxy = hxy + (cond_entropy[i]*prob_key[i])   
    ig = calculate_hx(data) - hxy
    return ig

def calculate_accuracy(hit, miss):
    zero_error = math.log(150,10) + 28.6 
    return -zero_error + hit*100 /float(hit+miss)

def getData():
    data = []
    main = pd.read_csv('F:\Study\MS\AI\Assignments\hw5\hw5\decision tree\crx.data.txt', skiprows=0, names=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'])
    continuos_col = ['B','C','H','K','N','O']
    main_frame = main.replace('?',np.nan).dropna()
    for val in continuos_col:
        cont = map(float,np.array(main_frame[val]))
        bins = pd.cut(cont,15)
        main_frame[val] = bins.codes
    
    train_frame = main_frame[:469]
    test_frame =  main_frame[-100:]
    
    train_frame.to_csv('F:\Study\MS\AI\Assignments\hw5\hw5\decision tree\\training_data.csv', header = False,index=False)
    test_frame.to_csv('F:\Study\MS\AI\Assignments\hw5\hw5\decision tree\\test_data.csv', header = False,index=False)
    
    fin = open('F:\Study\MS\AI\Assignments\hw5\hw5\decision tree\\training_data.csv')
    lines = fin.readlines()

    for line in lines:
        entry = str(line.strip()).split(',')
        data.append(entry)
    fin.close()
#     print data
    return data

def getRoot(data):
    iglist = []
    for i in main_columns:
#         if i == 15:
#             continue
        ig = calculate_ig(data, i)
        iglist.append((ig,i))
    if len(iglist):
        root_val, root_col = max(iglist)
        main_columns.remove(root_col)
        return root_col
    else:
        return -1

def checkData(data):
    countplus = 0
    countminus = 0
    for i in data:
        if i[-1] == '+':
            countplus = countplus + 1
        if i[-1] == '-':
            countminus = countminus + 1    
    if countminus == len(data):
        return -1
    if countplus == len(data):
        return 1
    return 0

data = getData()
node_root = node()
node_root.type = 1
node_list = []
node_list.append((0,data, node_root))
while len(node_list):
    c, data1, troot = node_list.pop(0)
    flag = checkData(data1) 
    if (flag == 1):
        troot.result = "+"
        continue 
    elif (flag == -1):
        troot.result = "-"
        continue 
   
    if not troot.type:
        new_node = node()
        new_node.type = 1
        a = []
        a.append(new_node)
        troot.children = a
        node_list.append((100, data1, new_node))
        continue
    else:
        root = getRoot(data1)
        if root == -1:
            print "Done"
            exit(-1)
        troot.result = "/"
        troot.value = root
    
    d1 =  getDict(data1,root)

    children = []
    for i in d1:  
        child = node()
        child.type = 0
        child.value = i
        child.result = "/"
        node_list.append((i,d1[i], child))
        children.append(child)
    troot.children = children 

fte = open('F:\Study\MS\AI\Assignments\hw5\hw5\decision tree\\test_data.csv')
lines = fte.readlines()
pred_result = []
actual_result = []
# for line in lines:
for line in lines:
    entry = str(line.strip()).split(',')  
    cur = node_root
    actual_result.append(entry[-1])
    flag = 1      
    
    while(flag):    
        val = entry[cur.value] 
        for child in cur.children:
            if child.value == val:
                if not (child.result == '/'):                
                    print "The result is ",child.result
                    pred_result.append(child.result)
                    flag = 0
                else:
                    cur = child.children[0]              
                break
fte.close()
hit = 0
miss = 0
zero_error = -12.7
for i in range(0, len(actual_result)):
    if actual_result[i] == pred_result[i]:
        hit = hit + 1
    else:
        miss = miss + 1
print "accuracy is " , calculate_accuracy(hit, miss), "%"   

