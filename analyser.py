#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from time import sleep
from random import randint, choice


OONI_BINARY = " "  # Path to ooniprobe binary. 
PROBE_TEST = "siteprobe.py"
DNS_TEST = "dnscompare.py"
TCP_TEST = "tcpconnect.py"
PING_TEST = "ping.py"
TRACEROUTE_TEST = "traceroute.py"
TOR_MIRRORS = ["https://www.unicorncloud.org/public/torproject.org/", "https://mirror.ml/tor/", "https://www.oignon.net/", "https://tor.hackthissite.org/"]
TOR_DIRECTORY_AUTHORITIES = [
                             { "86.59.21.38": 80 },
                             { "86.59.21.38": 443 },
                             { "76.73.17.194": 9030 },
                             { "76.73.17.194": 9090 },
                             { "171.25.193.9": 443 },
                             { "171.25.193.9": 80 },
                             { "dannenberg.ccc.de": 80 },
                             { "193.23.244.244": 443 },
                             { "208.83.223.34": 443 }, 
                             { "208.83.223.34": 80 },
                             { "128.31.0.34": 9131 },
                             { "128.31.0.34": 9101 },
                             { "194.109.206.212": 80 },
                             { "194.109.206.212": 443 },
                             { "212.112.245.170": 80 },
                             { "212.112.245.170": 443 },
                             { "154.35.32.5": 80 },
                             { "154.35.32.5": 443 }
                            ]

class Analyser():
        
    def runTest(self, test, argv):
        if len(argv) > 1:
            args = (OONI_BINARY, "-n", test, argv[0], argv[1])
        else:
            args = (OONI_BINARY, "-n", test)
        print "Running test %s" % test
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        return output
        
    def probeSite(self, args):
        return self.runTest(PROBE_TEST, args)
    
    def compareDNS(self, args):
        return self.runTest(DNS_TEST, args)
        
    def testTCPConnection(self):
        return self.runTest(TCP_TEST, [])
    
    def ping(self, argv):
        return self.runTest(ICMP_TEST, argv)
        
def probeTorSite():
    if not "Site reachable" in analyser.probeSite([]):
        print "Tor site not reachable - running tests"
        tests = [
                    { TCP_TEST: ["-t", "bridges.torproject.org"] },
                    {  DNS_TEST: [] },
                    {  PROBE_TEST: ["-u", choice(TOR_MIRRORS)] },
                    {  TCP_TEST: [] }
                ]
        runTests(tests)
    else:
        print "Tor site reachable"
         
def probeDirectoryAuthorities():
    reachable = False
    for server in TOR_DIRECTORY_AUTHORITIES:
        host = server.keys()[0]
        port = server[host] 
        url = makeURL(host, port)

        if "Site reachable" in analyser.probeSite(["-u", url]):
            print "Consensus successfully fetched"
            reachable = True
            break

    if not reachable:
        print "Failed to fetch consensus - running tests"
        tests = [ 
                { PING_TEST: ["-f", "directory_authorities.txt"] },
                { TRACEROUTE_TEST : ["-f", "directory_authorities.txt"] }
                ]
        runTests(tests)

def makeURL(host, port):
    if port == 80: 
         url = "http://%s/tor/status-vote/current/consensus.z" % (host)
    elif port == 443:
         url = "https://%s/tor/status-vote/current/consensus.z" % (host)
    else:
         url = "http://%s:%s/tor/status-vote/current/consensus.z" % (host, str(port))
    return url 

def runTests(tests):
    for x in range(len(tests)):
        test, args = randPop(tests)
        analyser.runTest(test, args)
        sleep(randint(1, 20))
    
def randPop(tests):
    t = choice(tests)
    test = t.keys()[0]
    args = t[test]
    tests.remove(t)
    return test, args

if __name__ == "__main__":
    analyser = Analyser()
    probeTorSite()               
    probeDirectoryAuthorities()