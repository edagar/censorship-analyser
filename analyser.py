#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from time import sleep
from random import randint, choice

from test import *
from const import *
    

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
    for host, port in TOR_DIRECTORY_AUTHORITIES.iteritems():
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




