#!/usr/bin/python

import argparse
import json
import os
import random
import signal
import string
import sys

import threading
import requests

DEBUG_MODE = False

# Set HTTP Header info.
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate'
           }

# Command line input
parser = argparse.ArgumentParser(description="This standalone script will look up a single username using the JSON file"
                                             " or will run a check of the JSON file for bad detection strings.")
parser.add_argument('-u', '--username', help='[OPTIONAL] If this param is passed then this script will perform the '
                                             'lookups against the given user name instead of running checks against '
                                             'the JSON file.')
parser.add_argument('-s', '--site', nargs='*',
                    help='[OPTIONAL] If this parameter is passed the script will check only the named site or list of '
                         'sites.')
parser.add_argument('-d', '--debug', help="Enable debug output", action="store_true")

# check operating system ot adjust output color formatting
if os.name == "posix":
    class Colors:
        YELLOW = "\033[93m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        ENDC = "\033[0m"
else:
    class Colors:
        YELLOW = ""
        RED = ""
        GREEN = ""
        ENDC = ""


def warn(msg):
    print(Colors.YELLOW + msg + Colors.ENDC)


def error(msg):
    print(Colors.RED + msg + Colors.ENDC)


def positive(msg):
    print(Colors.GREEN + msg + Colors.ENDC)


def neutral(msg):
    print(msg)


def signal_handler(*_):
    """
    If user pressed Ctrl+C close all connections and exit
    """
    error(' !!!  You pressed Ctrl+C. Exiting script.')
    sys.exit(0)


def web_call(location):
    try:
        # Make web request for that URL, timeout in X secs and don't verify SSL/TLS certs
        return requests.get(location, headers=HEADERS, timeout=60, verify=False, allow_redirects=False)
    except requests.exceptions.Timeout as caught:
        raise Exception("Connection time out. Try increasing the timeout delay.") from caught
    except requests.exceptions.TooManyRedirects as caught:
        raise Exception("Too many redirects. Try changing the URL.") from caught
    except Exception as caught:
        raise Exception("Critical error.") from caught


def random_string(length):
    return ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(length))


def find_sites_to_check(args, data):
    if args.site:
        # cut the list of sites down to only the requested one
        args.site = [x.lower() for x in args.site]
        sites_to_check = [x for x in data['sites'] if x['name'].lower() in args.site]
        if sites_to_check == 0:
            error('Sorry, none of the requested site or sites were not found in the list')
            sys.exit()
        sites_not_found = len(args.site) - len(sites_to_check)
        if sites_not_found:
            warn('WARNING: %d requested sites were not found in the list' % sites_not_found)
        neutral(' Checking %d sites' % len(sites_to_check))
        return sites_to_check
    else:
        neutral('%d sites found in file.' % len(data['sites']))
        return data['sites']


def message_to_print(url, status, run_type):
    if run_type == 'username':
        if status == 'found':
            return positive("[+] User found at %s" % url)
        elif status == 'not found':
            return neutral("[-] User not found at %s" % url)
        elif status == 'neither':
            return error("[!] Error. The check implementation is broken for %s" % url)

    elif run_type == 'non_existent':
        if status == 'found':
            return error("[!] False positive for %s" % url)
        elif status == 'not found':
            return neutral("    As expected, no user found at %s" % url)
        elif status == 'neither':
            return error("[!] Neither conditions matched for %s" % url)

    elif run_type == 'known_account':
        if status == 'found':
            return neutral("    As expected, profile found at %s" % url),
        elif status == 'not found':
            return error("[!] Profile not found at %s" % url),
        elif status == 'neither':
            return error("[!] Neither conditions matched for %s" % url)


def check_site(site, username, run_type):
    url = site['check_uri'].replace("{account}", username)
    try:
        resp = web_call(url)

        code_match = resp.status_code == int(site['account_existence_code'])
        string_match = resp.text.find(site['account_existence_string']) > 0

        if DEBUG_MODE:
            neutral("- HTTP status (match %s): %s " % (code_match, resp.status_code))
            neutral("- HTTP response (match: %s): %s" % (string_match, resp.content))

        if code_match and string_match:
            return message_to_print(url, 'found', run_type)

        code_missing_match = resp.status_code == int(site['account_missing_code'])
        string_missing_match = resp.text.find(site['account_missing_string']) > 0

        if code_missing_match or string_missing_match:
            return message_to_print(url, 'not found', run_type)

        return message_to_print(url, 'neither', run_type)

    except Exception as caught:
        error("Error when looking up %s (%s)" % (url, str(caught)))


###################
# Main
###################

def main():
    args = parser.parse_args()

    if args.debug:
        global DEBUG_MODE
        DEBUG_MODE = True
        print('Debug output enabled')

    # Add this in case user presses CTRL-C
    signal.signal(signal.SIGINT, signal_handler)

    # Suppress HTTPS warnings
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    with open('web_accounts_list.json') as data_file:
        data = json.load(data_file)

    sites_to_check = find_sites_to_check(args, data)

    # Start threads
    threads = list()
    for site in sites_to_check:
        if not site['valid']:
            warn("[!] Skipping %s - Marked as not valid." % site['name'])
            continue

        if args.username:
            run_type = 'username'
            x = threading.Thread(target=check_site, args=(site, args.username, run_type), daemon=True)
            threads.append(x)
            x.start()

        else:
            non_existent = random_string(20)
            n = threading.Thread(target=check_site, args=(site, non_existent, 'non_existent'), daemon=True)
            threads.append(n)
            n.start()

            for known_account in site['known_accounts']:
                k = threading.Thread(target=check_site, args=(site, known_account, 'known_account'), daemon=True)
                threads.append(k)
                k.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # execute only if run as a script
    main()

