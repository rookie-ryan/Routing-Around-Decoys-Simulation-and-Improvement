import urllib.request
file = open('bgp.txt','r')
outfile = open('downloadlist-1.txt','w')
for line in file:
    line = line.strip()
    url = line+'2020.11/RIBS/rib.20201101.0200.bz2'
    outfile.write(url+'\n')
file.close()
outfile.close()