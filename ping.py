
from twisted.python import usage
from ooni.utils import log
from scapy.all import IP, ICMP
from ooni.templates import scapyt

class UsageOptions(usage.Options):
    optParameters = [['target', 't', '127.0.0.1', "Specify the target to ping"]]

class ICMPPing(scapyt.BaseScapyTest):
        usageOptions = UsageOptions
        inputFile = ['file', 'f', None,
                 'Input file containing hosts to ping']

        def setUp(self):
            if self.input:
                self.target = self.input
            elif self.localOptions['target']:
                self.target = self.localOptions['target']
            else:
                self.target = '127.0.0.1'

        def test_icmp_ping(self):
            def finished(packets):
                self.report['packets'] = packets
                answered, unanswered = packets
                stuff = []
                for snd, rcv in answered:
                    stuff.append(rcv)
                log.msg("ReceivedPackets: [ %s ]" % stuff) 
            def failed(failure):
                log.msg("TestStatus: [ FAILED ]")
                log.msg("TestException: [ %s ]" % failure.getErrorMessage() )
            self.report['target'] = self.target
            packets = IP(dst=self.target)/ICMP()
            d = self.sr(packets)
            d.addCallback(finished)
            d.addErrback(failed)
            return d
