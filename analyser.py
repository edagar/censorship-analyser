#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from time import sleep
from random import randint, choice

import test
import const
    

def probeTorSite():
    if not siteReachable(const.TOR_SITE_URL):
        print "Tor site not reachable - running tests"
        tests = [
                test.TCPTest(target = const.TOR_BRIDGES_URL),
                test.DNSTest(),
                test.SiteProbe(target=choice(const.TOR_MIRRORS)),
                test.TCPTest()
                ]

        testcase = test.TestCase(tests=tests)
        testcase.run()
        testcase.printResults()

    else:
        print "Tor site reachable"
         
def probeDirectoryAuthorities():
    for host, port in const.TOR_DIRECTORY_AUTHORITIES.iteritems():
        url = makeURL(host, port)

        if siteReachable(url):
            print "Consensus successfully fetched"
            return

    print "Failed to fetch consensus - running tests"

    pingtests = test.TestCase()
    traceroutes = test.TestCase()

    for host in const.TOR_DIRECTORY_AUTHORITIES.keys():
        pingtests.append(test.PingTest(target=host))

    pingtests.run()
    unreachable = pingtests.getFailed()

    if unreachable:
        print "%i of the directory servers (%s) didn't respond the our ping." % ( len(unreachable), ", ".join([test.target for test in unreachable]) )
     
        for host in unreachable:
            traceroutes.append(test.Traceroute(target=host.target))
        
        traceroutes.run()
        traceroutes.printResults()

    pingtests.printResults()

def makeURL(host, port):
    if port == 80:
         url = "http://%s/tor/status-vote/current/consensus.z" % (host)
    elif port == 443:
         url = "https://%s/tor/status-vote/current/consensus.z" % (host)
    else:
         url = "http://%s:%s/tor/status-vote/current/consensus.z" % (host, str(port))
    return url

def siteReachable(url):
    probe = test.SiteProbe(target=url)
    probe.run()
    return probe.status == "OK"

if __name__ == "__main__":
    probeTorSite()
    probeDirectoryAuthorities()


