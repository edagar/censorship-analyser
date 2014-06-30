
from twisted.python import usage
from ooni.utils import log
from scapy.all import IP, ICMP
from ooni.templates import scapyt

class UsageOptions(usage.Options):
    optParameters = [['target', 't', '127.0.0.1', "Specify the target to ping"]]

class ICMPPing(scapyt.BaseScapyTest):
        usageOptions = UsageOptions
        inputFile = ['file', 'f', None,
                 'Input file containing urls to probe']

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
                for snd, rcv in answered:
                    rcv.show()
            self.report['target'] = self.target
            packets = IP(dst=self.target)/ICMP()
            d = self.sr(packets)
            d.addCallback(finished)
            return d
