#!  /usr/bin/env python3

import re
import argparse
import sys
import json
import requests

URL = "https://api.asrank.caida.org/v2/graphql"
decoder = json.JSONDecoder()
encoder = json.JSONEncoder()

f = open("20201101.as-rel.txt")
AS_name="AS_Size.txt"
AS_out = open(AS_name,"a+")

# method to print how to run script
def print_help():
    print(sys.argv[0], "-u as-rank.caida.org/api/v1")


######################################################################
## Parameters
######################################################################
# parser = argparse.ArgumentParser()
# parser.add_argument("asn", type=int, help="ASN we are looking up")
# args = parser.parse_args()

def main():
    total_AS = 0
    AS_list = []
    AS_set = set()  # used to speed search
    size_list=[]

    for line in f.readlines():
        if line[0] == '#':
            continue
        line_value = line.split("|")
        src_AS = line_value[0]
        dst_AS = line_value[1]
        relationship = line_value[2]
        if src_AS not in AS_set:
            total_AS += 1;
            AS_list.append(src_AS)
            AS_set.add(src_AS)
        if dst_AS not in AS_set:
            total_AS += 1
            AS_list.append(dst_AS)
            AS_set.add(dst_AS)
    print(total_AS)
    count=1
    for AS in AS_list:
        # if count<1412:
        #     count+=1
        #     continue
        # if(count%10==0):
        #     print(count)
        print(count)
        count+=1
        query = AsnQuery(int(AS))
        request = requests.post(URL, json={'query': query})
        if request.status_code == 200:
            # print(request.json());
            # print(request.json()['data']['asn']['cone'])
            if (request.json() is None) or (request.json()['data'] is None) or (request.json()['data']['asn'] is None) or (request.json()['data']['asn']['cone'] is None) or (request.json()['data']['asn']['cone']['numberAsns'] is None):
                size=1
                size_list.append(1)
                AS_out.write(str(AS) + "," + str(size) + "\n")
            else:
                size=request.json()['data']['asn']['cone']['numberAsns']
                size_list.append(size)
                AS_out.write(str(AS)+","+str(size)+"\n")
        else:
            print("Query failed to run returned code of %d " % (request.status_code))
            AS_out.write(str(AS) + "," + str(size) + "\n")

    # query = AsnQuery(args.asn)
    # request = requests.post(URL, json={'query': query})
    # if request.status_code == 200:
    #     print(request.json());
    # else:
    #     print("Query failed to run returned code of %d " % (request.status_code))


    # if args.asn is None:
    #     parser.print_help()
    #     sys.exit()
    # for AS in AS_list:
    #     query = AsnQuery(int(AS))
    #     request = requests.post(URL, json={'query': query})
    #     if request.status_code == 200:
    #         print(request.json());
    #     else:
    #         print("Query failed to run returned code of %d " % (request.status_code))


######################################################################
## Queries
######################################################################

def AsnQuery(asn):
    return """{
        asn(asn:"%i") {
            asn
            asnName
            rank
            organization {
                orgId
                orgName
            }
            cliqueMember
            seen
            longitude
            latitude
            cone {
                numberAsns
                numberPrefixes
                numberAddresses
            }
            country {
                iso
                name
            }
            asnDegree {
                provider
                peer
                customer
                total
                transit
                sibling
            }
            announcing {
                numberPrefixes
                numberAddresses
            }
        }
    }""" % (asn)


# run the main method
main()