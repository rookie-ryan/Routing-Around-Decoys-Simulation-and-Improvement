import os

dic = {}
def work(root): 
    for fn in os.listdir(root):
        file = open(root+fn,'r')
        for line in file:
            line = line.strip()
            parts = line.split(' ')
            jump = False
            for i in range(len(parts)-1):
                if parts[i+1].find('{') > -1 or int(parts[i+1]) == 0 or int(parts[i+1]) > 400000:
                    jump = True
                    break
            if jump == True:
                continue
            if len(parts) <= 2:
                continue
            desas = parts[-1]
            if desas not in dic:
                dic[desas] = {}
            for j in range(len(parts)-2):
                if parts[j+1] == desas:
                    break
                if parts[j+1] in dic[desas]:
                    continue
                if parts[j+1] == parts[j+2]:
                    continue
                else:
                    dic[desas][parts[j+1]] = parts[j+2]
        file.close()
work('routeviews/final2/')
work('RIPE/final2/')
# print(dic)
for key in dic:
    outfile = open("inference/"+key+".txt","w")
    for item in dic[key]:
        outfile.write(item + " " + dic[key][item]+"\n")
    outfile.close()
