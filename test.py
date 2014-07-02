import subprocess
from random import choice, randint
from time import sleep

class Test(object):
    def __init__(self, testfile, args, ooni_binary):
        self.testfile = testfile
        self.args = args
        self.binary = ooni_binary
        self.output = None 
        self.status = None

    def run(self):
        if self.args:
            args = (self.binary, "-n", self.testfile, self.args[0], self.args[1])
        else:
            args = (self.binary, "-n", self.testfile)
        print "Running test %s" % self.testfile
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        self.parseOutput(popen.stdout.read())

    def parseOutput(self, output):
        self.output = output
        key = "status: "
        start = output.find(key) + len(key)  
        status = output[start:].split(" ")[0]
        self.status = status

class TestCase(object):
    def __init__(self, tests=[], sleep_interval=(1,20)):
        self.tests = tests
        self.sleepInterval = sleep_interval

    def addTests(self, tests):
        self.tests += tests

    def run(self):
        for test in self.tests:
            test.run()
            sleep(randint(self.sleepInterval[0], self.sleepInterval[1]))

    def verifyResults(self):
        for test in self.tests:
            print test.status 

