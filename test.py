import subprocess
from random import choice, randint
from time import sleep
import yaml

from ooni.otime import timestamp
import const

class Test(object):
    def __init__(self, testfile, args=[]):
        self.testfile = testfile
        self.args = args
        self.output = None 
        self.status = None
        self.errorMessage = None
        self.parser = None
        self.report = None
        self.reportName = None

    def run(self):
        self.reportName = "report-%s-%s.yamloo" % (self.testfile, timestamp())
        self.output = runTest(self)
        self.parseResults()

    def parseResults(self):
        self.parser = TestParser(self)
        self.parser.parseReport()

    def printResults(self):
        self.parser.printResults()

    def getResults(self):
        return {
                "Status": self.status,
                "ErrorMessage": self.errorMessage,
                }

class SiteProbe(Test):
    def __init__(self, testfile=const.PROBE_TEST, target=const.TOR_SITE_URL):
        super(SiteProbe, self).__init__(testfile=testfile, args = ["-u", target])
        self.target = target

class TCPTest(Test):
    def __init__(self, testfile=const.TCP_TEST, target=const.TOR_DOMAIN, port="443"):
        super(TCPTest, self).__init__(testfile=testfile, args=["-t", target, "-p", port])
        self.target = target

class PingTest(Test):
    def __init__(self, testfile=const.PING_TEST,target=None):
        args = ["-t", target] if target is not None else [] 
        super(PingTest, self).__init__(testfile=testfile, args=args)
        self.target = target
        self.packets = None

    def parsePackets(self, report):
        try:
            return 'echo-reply' in report['ReceivedPackets'][0][0]['summary']
        except:
            return False

    def parseResults(self):
        self.parser = TestParser(self)
        self.parser.loadReport()

        if self.report['TestStatus'] == 'OK':
            self.packets = self.report['packets']

            if self.parsePackets(self.report):
                self.status = "OK"
                return

        self.status = "FAILED"
        self.errorMessage = "Host unreachable"
        raise TestException(self)

class DNSTest(Test):
    def __init__(self, testfile=const.DNS_TEST, target=const.TOR_DOMAIN):
        super(DNSTest, self).__init__(testfile=testfile, args=["-t", target])
        self.target = target

class Traceroute(Test):
    def __init__(self, testfile=const.TRACEROUTE_TEST, target=None):
        args = ["-b", target] if target is not None else []
        super(Traceroute, self).__init__(testfile=testfile,args=args)
        self.target = target


class TestParser(object):
    def __init__(self, test):
        self.test = test
    
    def loadReport(self):
        with open(self.test.reportName, 'r') as f:
            entries = yaml.safe_load_all(f)

            headers = entries.next()
            self.test.report = entries.next()


    def parseReport(self):
        self.loadReport()
        self.test.status = self.test.report['TestStatus']

        if not self.test.status == "OK":
            self.test.errorMessage = self.test.report['TestException']
            raise TestException(self.test)


    def printResults(self):
        print "Test: %s" % self.test.testfile
        if hasattr(self.test, "target") and self.test.target is not None:
            print "Target: %s" % self.test.target

        results = self.test.getResults()
        for key, value in results.iteritems():
            if key and value:
                print "%s: %s" % (key, value)


class TestCase(list):
    def __init__(self, tests=[], sleep_interval=const.SLEEP_INTERVAL):
        super(TestCase, self).__init__(tests)
        self.sleepInterval = sleep_interval

    def run(self):
        tests = testCaseGenerator(list(self))

        for test in tests:
            try:
                test.run()
            except TestException, e:
                print e

            sleep(randint(self.sleepInterval[0], self.sleepInterval[1]))

    def printResults(self):
        for test in self:
            test.printResults()
            print

    def getFailed(self):
        return [test for test in self if test.status != "OK"]

def testCaseGenerator(seq):
    for x in range(len(seq)):
        test = choice(seq)
        seq.remove(test)
        yield test

def runTest(test):
    binary = const.OONI_BINARY
    args = [binary, "-o", test.reportName, "-n", test.testfile]

    if test.args:
        args += test.args
        
    print "Running test %s" % test.testfile
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

    output = popen.stdout.read()
    return output

class TestException(Exception):
    def __init__(self, test):
        self.testInstance = test

    def __str__(self):
        return "%s: %s  (%s)" % (self.testInstance.testfile, self.testInstance.status, self.testInstance.errorMessage)
