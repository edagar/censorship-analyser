import subprocess
from random import choice, randint
from time import sleep

from const import *

class Test(object):

    def __init__(self, testfile, args=[]):
        self.testfile = testfile
        self.args = args
        self.output = None 
        self.status = None
        self.errorMessage = None
        self.parser = None

    def run(self):
        self.output = runTest(self)
        self.parseResults()

    def parseResults(self):
        self.parser = TestParser(self)
        self.parser.parseOutput(self.output)

    def printResults(self):
        self.parser.printResults()

    def getResults(self):
        return {
                "Status": self.status,
                "ErrorMessage": self.errorMessage,
                }

class SiteProbe(Test):
    def __init__(self, testfile=PROBE_TEST, target=TOR_SITE_URL):
        super(SiteProbe, self).__init__(testfile=testfile, args = ["-u", target])
        self.target = target

class TCPTest(Test):
    def __init__(self, testfile=TCP_TEST, target=TOR_DOMAIN, port="443"):
        super(TCPTest, self).__init__(testfile=testfile, args=["-t", target, "-p", port])
        self.target = target

class PingTest(Test):
    def __init__(self, testfile=PING_TEST,target=None):
        args = ["-t", target] if target is not None else [] 
        super(PingTest, self).__init__(testfile=testfile, args=args)
        self.target = target
        self.packets = None

    def parseResults(self):
        self.parser = TestParser(self)
        self.packets = self.parser.findValue("ReceivedPackets: ")
        if "echo-reply" in self.packets:
            self.status = "OK"
        else:
            self.status = "FAILED"
            self.errorMessage = "Host unreachable"

class DNSTest(Test):
    def __init__(self, testfile=DNS_TEST, target=TOR_DOMAIN):
        super(DNSTest, self).__init__(testfile=testfile, args=["-t", target])
        self.target = target

class Traceroute(Test):
    def __init__(self, testfile=TRACEROUTE_TEST, target=None):
        args = ["-b", target] if target is not None else []
        super(Traceroute, self).__init__(testfile=testfile,args=args)
        self.target = target


class TestParser(object):
    def __init__(self, test):
        self.test = test

    def findValue(self, key):
        """
        The ooniprobe tests include simple key/value pairs
        in their output, indicating the test results. 
        
        To avoid false positives, the format "key: [ VALUE ]"
        is used. This method takes "key" as a parameter,
        and returns VALUE.
        """
        output = self.test.output
        if not key in output:
            return "NOT FOUND"

        start = output.find(key) + len(key)  
        value = output[start:].split(" ]")[0][1:].strip()    
        return value

    def parseOutput(self, output):
        self.test.status = self.findValue("TestStatus: ")
        if not self.test.status == "OK":
            self.test.errorMessage = self.findValue("TestException: ")
    
    def printResults(self):
        print "Test: %s" % self.test.testfile
        if hasattr(self.test, "target") and self.test.target is not None:
            print "Target: %s" % self.test.target

        results = self.test.getResults()
        for key, value in results.iteritems():
            if key and value:
                print "%s: %s" % (key, value)


class TestCase(list):
    def __init__(self, tests=[], sleep_interval=SLEEP_INTERVAL):
        super(TestCase, self).__init__(tests)
        self.sleepInterval = sleep_interval

    def run(self):
        tests = testCaseGenerator(list(self))
        for test in tests:
            test.run()
            sleep(randint(self.sleepInterval[0], self.sleepInterval[1]))

    def printResults(self):
        for test in self:
            test.printResults()
            print

    def getFailed(self):
        failed = [test for test in self if test.status != "OK"]
        return failed

def testCaseGenerator(seq):
    for x in range(len(seq)):
        test = choice(seq)
        seq.remove(test)
        yield test

def runTest(test):
    binary = OONI_BINARY
    args = [binary, "-n", test.testfile]

    if test.args:
        args += test.args
        
    print "Running test %s" % test.testfile
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

    output = popen.stdout.read()
    return output
