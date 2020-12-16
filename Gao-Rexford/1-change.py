import os
f = open("a.sh",'w')
for file in os.listdir("routeviews/decompression"):
    f.write("nohup cat routeviews/decompression/"+file+" | zebra-dump-parser/zebra-dump-parser.pl > routeviews/final2/"+file+".txt"+"\n")

f.close()
