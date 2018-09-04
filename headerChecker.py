#!/usr/bin/env python
"""This script verifies BitSight required headers"""

import urllib.request
import urllib.error
import ssl
import argparse
PARSER = argparse.ArgumentParser(description='Process URL\'s')
PARSER.add_argument('url', type=str, nargs='+',
                    help='Add urls to check for common security headers')
PARSER.add_argument('--proxy', type=str,
                    help='Pass proxy info ex. http://proxy:8080')
ARGS = PARSER.parse_args()
HEADERTYPES = ['Content-Security-Policy', 'Strict-Transport-Security',
               'X-Content-Type-Options', 'Expires', 'X-Frame-Options',
               'Cache-Control', 'Access-Control-Allow-Origin', 'Set-Cookie',
               'X-XSS-Protection']
PROXY = urllib.request.ProxyHandler({'http': ARGS.proxy})
for u in ARGS.url:
    print('Testing:', u, '\n')
    opener = urllib.request.build_opener(PROXY)
    urllib.request.install_opener(opener)
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        req = urllib.request.urlopen(u)
    except urllib.error.HTTPError as response:
        pass
    headers = req.info()
    for t in HEADERTYPES:
        if t in headers:
            print(t, 'Header Found Value=', req.getheader(t))
        else:
            print(t, 'Header Missing!!!!')
    print('\n')
