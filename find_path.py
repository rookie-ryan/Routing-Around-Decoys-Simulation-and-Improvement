import time

path_dict = {}
key_set = set()


def path(s, d):
    s=str(s)
    d=str(d)
    d_file = "path/" + str(d) + ".txt"
    try:
        file = open(d_file, "r")
    except IOError:
        return "nopath"
    for line in file:
        line=line.replace("\n","")
        value = line.split(" ")
        src = value[0]
        next_hop = value[1]
        path_dict[src] = next_hop
        key_set.add(src)
    return_path = str(s)
    current_hop = ""
    if s in key_set:
        current_hop = path_dict[s]
        return_path += ","
        return_path += current_hop
    else:
        return "nopath"
    count=1
    while current_hop != str(d):
        if count>20 or current_hop not in key_set:
            return "nopath"
        count+=1
        current_hop = path_dict[current_hop]
        return_path += ","
        return_path += current_hop
    return return_path

# t1=time.time()
# p=path(29386,1)
# t2=time.time()
# print(t2-t1)
# print(p)
