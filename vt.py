import requests
import argparse
import os
import json
import requests
import sys


def checkkey(kee):
    try:
        if len(kee) == 64:
            return kee
        else:
            print("There is something wrong with your key. Not 64 Alpha Numeric characters.")
            exit()
    except Exception as e:
        print(e)

def checkhash(hsh):
    try:
        if len(hsh) == 32:
            return hsh
        elif len(hsh) == 40:
            return hsh
        elif len(hsh) == 64:
            return hsh
        else:
            print("The Hash input does not appear valid.")
            exit()
    except Exception as e:
        print(e)

def fileexists(filepath):
    try:
        if os.path.isfile(filepath):
            return filepath
        else:
            print("There is no file at:" + filepath)
            exit()
    except Exception as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(description="As an input, this script takes a file with hashes, checks replies from Virus Total,"
                                                 " providing a list of candidates to Cylance Quarantine list as an output. ")
    parser.add_argument('-k', '--key', type=checkkey, required=True, help='Personal Virus Total API key')
    parser.add_argument('-i', '--input', type=fileexists, required=False, help='Input file location example: /Somewhere/input.txt, or, simply text filename if the script & file location match.')
    args = parser.parse_args()


    if args.input and args.key:
        with open(args.input) as o:
            for line in o.readlines():
                VT_Request(args.key, line.rstrip())


def VT_Request(key, hash):
    params = {'apikey': key, 'resource': hash}
    url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    json_response = url.json()

    try:
        response = int(json_response.get('response_code'))
        hash256 = json_response['sha256']
        allEnginesStatus = json_response['scans']
        cylanceStatus = allEnginesStatus['Cylance']
        cylanceVerdict = cylanceStatus['detected']
        if response == 0 and len(hash) == 64:
            print(hash)
        elif response != 0 and cylanceVerdict == False:
            print(hash256)
        else:
            return 0

    except KeyError:
        return 0

    except AttributeError:
        return 0

main()