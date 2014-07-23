
# Interval for random sleep periods between tests.
SLEEP_INTERVAL = (1, 25)  

OONI_BINARY = "ooniprobe"

PROBE_TEST = "siteprobe.py"

DNS_TEST = "dnscompare.py"

TCP_TEST = "tcpconnect.py"

PING_TEST = "ping.py"

TRACEROUTE_TEST = "traceroute.py"

TOR_SITE_URL = "https://www.torproject.org"

TOR_DOMAIN = "torproject.org"

TOR_BRIDGES_URL =  "bridges.torproject.org"

TOR_MIRRORS = ["https://www.unicorncloud.org/public/torproject.org/", "https://mirror.ml/tor/", "https://www.oignon.net/", "https://tor.hackthissite.org/"]

TOR_DIRECTORY_AUTHORITIES = {
                              "128.31.0.34": 9131,
                              "86.59.21.38": 80,
                              "194.109.206.212": 80,
                              "76.73.17.194": 9030,
                              "212.112.245.170": 80,
                              "193.23.244.244": 80,
                              "208.83.223.34": 443, 
                              "171.25.193.9": 443,
                              "154.35.32.5": 80, 
                              }
                            
 
