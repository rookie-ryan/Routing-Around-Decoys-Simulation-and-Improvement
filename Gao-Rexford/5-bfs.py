import queue as Queue
import os
#有多少AS
n = 400000
#记载所有的AS号
ASN = set()
#初始化annotated AS graph
graph = [{} for i in range(n)]
#导入AS relationships
ASReFile = open("20201101.as-rel.txt","r")
for i in ASReFile:
    if i.find("#") > -1:
        continue
    i = i.strip()
    info = i.split('|')
    as1 = int(info[0])
    as2 = int(info[1])
    re = int(info[2])
    #AS1 is provider,AS2 is customer
    if re == -1:
        graph[as1][as2] = 1
        graph[as2][as1] = -1
    #AS1 is peer,AS2 is peer
    elif re == 0:
        graph[as1][as2] = 0
        graph[as2][as1] = 0
    #ASN添加as1和as2
    ASN.add(as1)
    ASN.add(as2)
#关闭文件
ASReFile.close()
#Three-Stage BFS
def bfs(des):
    #记录到达指定AS的路径
    path = {}
    pathlen = {}
    rawbgp = open("inference/"+str(des)+".txt")
    baseas = []
    for line in rawbgp:
        line = line.strip()
        parts = line.split(' ')
        as1 = int(parts[0])
        as2 = int(parts[1])
        if as1 == des:
            continue
        if as1 >=n or as2 >= n:
            continue
        if as2 not in graph[as1]:
            graph[as1][as2] = 2
            graph[as2][as1] = 2
        path[as1] = int(as2)
        baseas.append(int(as1))
    path[des] = des
    pathlen[des] = 0
    #visit数组记载各AS是否被访问
    visit1 = [0 for i in range(n)]
    visit2 = [0 for i in range(n)]
    visit3 = [0 for i in range(n)]
    visit1[des] = 1
    visit2[des] = 1
    visit3[des] = 1
    #初始化队列,三个队列用于三个阶段
    que1 = Queue.Queue()
    que2 = Queue.Queue()
    que3 = Queue.Queue()
    que1.put(des)
    que2.put(des)
    que3.put(des)
    #First Stage:Customer Paths
    while not que1.empty():
        AS = que1.get()
        for key in graph[AS]:
            if visit1[key] == 0 and key in baseas:
                pathlen[key] = pathlen[AS] + 1
                visit1[key] = 1
                visit2[key] = 1
                que1.put(key)
                que2.put(key)
            if visit1[key] == 0 and graph[AS][key] == -1:
                path[key] = AS
                pathlen[key] = pathlen[AS] + 1
                visit1[key] = 1
                visit2[key] = 1
                que1.put(key)
                que2.put(key)
            #Tie Break
            elif visit1[key] == 1 and graph[AS][key] == -1 and key not in baseas:
                if pathlen[key] == pathlen[AS] + 1:
                    if int(AS) < int(path[key]):
                        path[key] = AS
    #Second Stage:Peer paths
    while not que2.empty():
        AS = que2.get()
        for key in graph[AS]:
            if visit2[key] == 0 and graph[AS][key] == 0:
                path[key] = AS
                pathlen[key] = pathlen[AS] + 1
                visit2[key] = 1
            #Tie Break
            elif visit1[key] == 0 and visit2[key] == 1 and graph[AS][key] == 0:
                if pathlen[key] == pathlen[AS] + 1:
                    if int(AS) < int(path[key]):
                        path[key] = AS
    #Third Stage:Provider paths
    while not que3.empty():
        AS = que3.get()
        for key in graph[AS]:
            if visit2[key] == 1 and visit3[key] == 0:
                visit3[key] = 1
                que3.put(key)
            elif visit3[key] == 0 and graph[AS][key] == 1:
                path[key] = AS
                pathlen[key] = pathlen[AS] + 1
                visit3[key] = 1
            #Tie Break
            elif visit3[key] == 1 and graph[AS][key] == 1 and key not in baseas:
                if pathlen[key] == pathlen[AS] + 1:
                    if int(AS) < int(path[key]):
                        path[key] = AS
    #输出path
    #输出路径结果的文件
    PathFile = open("path/" + str(des) + ".txt","w")
    for key in path:
        if key != des:
            PathFile.write(str(key)+" " + str(path[key]) + "\n")
    PathFile.close()
#对每一个AS都进行路径推断
aslist = []
for fname in os.listdir("inference/"):
    aslist.append(int(fname[:-4]))
aslist = sorted(aslist)
for i in aslist:
    #print(i)
    bfs(int(i))


