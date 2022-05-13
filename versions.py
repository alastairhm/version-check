#!/usr/bin/env python3
"""Get latest versions."""

import os
import sys
import argparse
import requests
import yaml
from loguru import logger
from yaml.loader import SafeLoader


def generate_url_github(details):
    """Format URL for API call"""
    source = details["source"].split('/')
    api = 'https://api.github.com/repos/' + source[3] + '/' + source[4] + '/releases/latest'
    return api


def generate_url_gitlab(details):
    """Format URL for API call"""
    source = details["source"].split('/')
    tail = source[3]
    for elem in source[4:]:
        tail = tail + '%2F' + elem
    api = 'https://' + source[2] + '/api/v4/projects/' + tail + '/releases'
    return api


def main():
    """Update Terrafile to latest versions."""

    requests.packages.urllib3.disable_warnings()
    parser = argparse.ArgumentParser(description='Upgrade Terrafile module versions')
    parser.add_argument("-i", "--input", type=str, help="Input Terrafile YAML, default=Terrafile",
                        default="Terrafile.yml")
    parser.add_argument("-v", "--verbose", action='store_true', help="Verbose output")
    args = parser.parse_args()
    if args.verbose:
        logger.debug('Arguments : {a}', a=args)

    if os.path.isfile(args.input):
        terrafile = []
        with open(args.input, "r") as input_file:
            terrafile = list(yaml.load_all(input_file, Loader=SafeLoader))
            terrafile = terrafile[0]

        print('Checking versions...')
        for repo in terrafile:
            print('Repo [', repo, ']', end=', ')
            details = terrafile[repo]
            if 'github' in details['source']:
                api = generate_url_github(details)
                if args.verbose:
                    logger.debug('URL : {u}', u=api)
                response = requests.get(api, verify=False)
                print(response.json()['name'])
            else:
                api = generate_url_gitlab(details)
                if args.verbose:
                    logger.debug('URL : {u}', u=api)
                response = requests.get(api, verify=False)
                print(response.json()[0]['tag_name'])

    else:
        logger.error('Error : Input file not found {file}', file=args.input)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(e)
        sys.exit(1)
