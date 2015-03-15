# -*- coding: utf-8 -*-
from twisted.internet.error import ConnectionRefusedError
from ooni.utils import log
from ooni.templates import tcpt
from twisted.python import usage

class UsageOptions(usage.Options):
    optParameters = [
                     ['target', 't', None, 'Specify a single host to test.'],
                     ['port', 'p', None, 'Specify port.']
                     ]
 

class TCPConnect(tcpt.TCPTest):
    usageOptions = UsageOptions

    def setUp(self):
        if self.input:
            self.target = self.input
        elif self.localOptions['target']:
            self.target = self.localOptions['target']
        else:
            self.target = "www.torproject.org"
       
        if self.localOptions['port']:
            self.targetPort = int(self.localOptions['port'])
        else:
            self.targetPort = 443

        self.report['host'] = self.target
        self.report['port'] = self.targetPort

    def test_hello(self):
        """
        A TCP connection to torproject.org port 443 is attempted
        """
        def got_response(response):
            self.report['TestStatus'] = 'OK'
            self.report['response'] = response

        def connection_failed(failure):
            self.report['TestException'] = '%s' % failure.getErrorMessage() 
            self.report['TestStatus'] = 'FAILED'
            failure.trap(ConnectionRefusedError)

        self.address = self.target
        self.port = self.targetPort
        payload = "Hello \n\r"
        d = self.sendPayload(payload)
        d.addErrback(connection_failed)
        d.addCallback(got_response)
        return d
