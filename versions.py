#!/usr/bin/env python3
"""Get latest versions."""

import os
import sys
import argparse
import requests
import yaml
from yaml.loader import SafeLoader

def generate_url(details):
    """Format URL for API call"""
    source = details["source"].split('/')
    api = 'https://api.github.com/repos/'+source[3]+'/'+source[4]+'/releases/latest'
    return api


def main():
    """Update Terrafile to latest versions."""

    requests.packages.urllib3.disable_warnings()
    parser = argparse.ArgumentParser(description='Upgrade Terrafile module versions')
    parser.add_argument("-i","--input",type=str,help="Input Terrafile YAML, default=Terrafile",
                        default="Terrafile")
    parser.add_argument("-v","--verbose", action='store_true',help="Verbose output")
    args = parser.parse_args()
    if args.verbose:
        print("Arguements :",args)

    if os.path.isfile(args.input):
        terrafile = []
        with open(args.input, "r") as input_file:
            terrafile = list(yaml.load_all(input_file, Loader=SafeLoader))
            terrafile = terrafile[0]

        print('Checking versions...')
        for repo in terrafile:
            print('Repo [',repo,']', end=', ')
            details = terrafile[repo]
            api = generate_url(details)
            response = requests.get(api, verify=False)
            print(response.json()['name'])
    else:
        print('Error : Input file not found')
        return 1
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(e)
        sys.exit(1)
