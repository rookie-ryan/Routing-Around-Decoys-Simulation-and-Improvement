import os
f = open("b.sh",'w')
for file in os.listdir("RIPE/de"):
    f.write("nohup cat RIPE/de/"+file+" | zebra-dump-parser/zebra-dump-parser.pl > RIPE/final2/"+file+".txt"+"\n")

f.close()
