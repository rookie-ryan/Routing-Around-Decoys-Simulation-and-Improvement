import urllib.request
outfile = open('downloadlist-2.txt','w')
for i in range(25):
    if i < 10:
        num = '0'+str(i)
    else:
        num = str(i)

    url = 'http://data.ris.ripe.net/rrc'+num+'/2020.11/bview.20201101.0000.gz'

    outfile.write(url+'\n')
outfile.close()
