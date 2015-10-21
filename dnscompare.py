# -*- coding: utf-8 -*-
from ooni.utils import log
from twisted.python import usage
from twisted.internet import defer
from ooni.templates import dnst


class UsageOptions(usage.Options):
    optParameters = [
        ['target', 't', None, 'Specify a single hostname to query.'],
        ['expected', 'e', None,
         'Speficy file containing expected lookup results'],
    ]


class DNSLookup(dnst.DNSTest):
    name = "DNSLookupTest"
    version = 0.1

    usageOptions = UsageOptions

    def setUp(self):
        self.expected_results = []
        self.dns_servers = []
        if self.input:
            self.hostname = self.input
        elif self.localOptions['target']:
            self.hostname = self.localOptions['target']
        else:
            self.hostname = "torproject.org"

        if self.localOptions['expected']:
            with open(self.localOptions['expected']) as file:
                for line in file:
                    self.expected_results.append(line.strip())
        else:
            self.expected_results = [
                '154.35.132.70',
                '38.229.72.14',
                '38.229.72.16',
                '82.195.75.101',
                '86.59.30.40',
                '93.95.227.222'
            ]

        self.report['expected_results'] = self.expected_results

        with open('/etc/resolv.conf') as f:
            for line in f:
                if line.startswith('nameserver'):
                    self.dns_servers.append(line.split(' ')[1].strip())
            self.report['dns_servers'] = self.dns_servers

    def verify_results(self, results):
        for result in results:
            if result not in self.expected_results:
                return False
        return True

    @defer.inlineCallbacks
    def test_dns_comparison(self):
        """
        Performs A lookup on specified host and matches the results
        against a set of expected results. When not specified, host and
        expected results default to "torproject.org" and
        ['38.229.72.14', '38.229.72.16', '82.195.75.101', '86.59.30.40',
        '93.95.227.222'].
        """
        for s in self.dns_servers:
            dnsServer = (s, 53)
            results = yield self.performALookup(self.hostname, dnsServer)

            if results:
                if self.verify_results(results):
                    self.report['TestStatus'] = 'OK'
                else:
                    self.report['TestStatus'] = 'FAILED'
                    self.report['TestException'] = 'unexpected results'

    @defer.inlineCallbacks
    def test_control_results(self):
        """
        Googles 8.8.8.8 server is queried, in order to generate
        control data.
        """
        results = yield self.performALookup(self.hostname, ("8.8.8.8", 53))

        if results:
            self.report['control_results'] = results
