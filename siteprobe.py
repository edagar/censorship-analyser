# -*- coding: utf-8 -*-
from ooni.utils import log
from ooni.utils.net import userAgents
from ooni.templates import httpt
from twisted.python import usage
from twisted.internet import defer
import random

class UsageOptions(usage.Options):
    optParameters = [
                     ['url', 'u', None, 'Specify a single URL to test.']
                     ]
    
class WebsiteProbe(httpt.HTTPTest):
    name = "WebsiteProbeTest"
    author = "Tobias Rang"
    version = 0.1
    
    usageOptions = UsageOptions
    
    inputFile = ['file', 'f', None,
                 'Input file containing urls to probe']
        
    def setUp(self):
        """
        Check for inputs.
        """
        if self.input:
            self.url = self.input
        elif self.localOptions['url']:
            self.url = self.localOptions['url']
        else:
            self.url = "https://www.torproject.org"

        self.headers = {'User-Agent': [random.choice(userAgents)]}
        self.report['site_to_probe'] = self.url
    
    @defer.inlineCallbacks
    def test_probe_site(self):
        """
        Sends a GET-requests to specified URL.
        Defaults to "https://www.torproject.org".
        """
        try:
            response = yield self.doRequest(self.url, method="GET",
                use_tor=False, headers=self.headers)
        except Exception, e:
            log.exception(e)
            
        if not response:
            log.err("Site unreachable")
            self.report['Site_reachable'] = "No"
 
        else:
            log.msg("Site reachable")
            self.report['Site_reachable'] = "Yesk"
