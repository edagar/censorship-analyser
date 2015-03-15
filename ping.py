
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
            self.report['TestStatus'] = ''
            if self.input:
                self.target = self.input
            elif self.localOptions['target']:
                self.target = self.localOptions['target']
            else:
                self.target = '127.0.0.1'

        def test_icmp_ping(self):
            def finished(packets):
                self.report['TestStatus'] = 'OK'
                self.report['packets'] = packets
                answered, unanswered = packets
                pkts = []
                for snd, rcv in answered:
                    pkts.append(rcv)
                self.report['ReceivedPackets'] = pkts

            def failed(failure):
                self.report['TestStatus'] = 'FAILED'
                self.report['TestException'] = '%s' % ( failure.getErrorMessage() )

            self.report['target'] = self.target
            packets = IP(dst=self.target)/ICMP()
            d = self.sr(packets)
            d.addCallback(finished)
            d.addErrback(failed)
            return d
