#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from time import sleep
from random import randint, choice
from test import *

SLEEP_INTERVAL = (1, 25)  # Interval for random sleep periods between tests.
OONI_BINARY = "ooniprobe"
PROBE_TEST = "siteprobe.py"
DNS_TEST = "dnscompare.py"
TCP_TEST = "tcpconnect.py"
PING_TEST = "ping.py"
TRACEROUTE_TEST = "traceroute.py"
TOR_SITE_URL = "https://www.torproject.org"
TOR_BRIDGES_URL =  "bridges.torproject.org"
TOR_MIRRORS = ["https://www.unicorncloud.org/public/torproject.org/", "https://mirror.ml/tor/", "https://www.oignon.net/", "https://tor.hackthissite.org/"]
TOR_DIRECTORY_AUTHORITIES = [
                             { "128.31.0.34": 9131 },
                             { "86.59.21.38": 80 },
                             { "194.109.206.212": 80 },
                             { "76.73.17.194": 9030 },
                             { "212.112.245.170": 80 },
                             { "193.23.244.244": 80 },
                             { "208.83.223.34": 443 }, 
                             { "171.25.193.9": 443 },
                             { "154.35.32.5": 80 },
                            ]
    

def probeTorSite():
    if not siteReachable(TOR_SITE_URL):
        print "Tor site not reachable - running tests"
        tests = [
                TCPTest(target = TOR_BRIDGES_URL),
                DNSTest(),
                SiteProbe(target=choice(TOR_MIRRORS)),
                TCPTest()
                ]

        testcase = TestCase()
        map(lambda test: testcase.append(test), tests)
        testcase.run()
        testcase.printResults()

    else:
        print "Tor site reachable"
         
def probeDirectoryAuthorities():
    for server in TOR_DIRECTORY_AUTHORITIES:
        host = server.keys()[0]
        port = server[host] 
        url = makeURL(host, port)

        if siteReachable(url):
            print "Consensus successfully fetched"
            return

    print "Failed to fetch consensus - running tests"
    tests = [
            PingTest(),
            Traceroute()
            ]

    testcase = TestCase()
    map(lambda test: testcase.append(test), tests)
    testcase.run()
    testcase.printResults()

def makeURL(host, port):
    if port == 80: 
         url = "http://%s/tor/status-vote/current/consensus.z" % (host)
    elif port == 443:
         url = "https://%s/tor/status-vote/current/consensus.z" % (host)
    else:
         url = "http://%s:%s/tor/status-vote/current/consensus.z" % (host, str(port))
    return url 

def siteReachable(url):
    probe = SiteProbe(target=url)
    probe.run()
    return probe.status == "OK"

if __name__ == "__main__":
    probeTorSite()               
    probeDirectoryAuthorities()




