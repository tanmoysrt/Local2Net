from scapy.all import *


# testcap = open('fuzz-2006-06-26-2594.pcap', 'rb')
# data = str(testcap.read())
# testcap.close()
# data = data[2:-1]
# data = data.encode('raw_unicode_escape')
# data = data.decode('unicode_escape')
# data = data.encode('raw_unicode_escape')
data = rdpcap('fuzz-2006-06-26-2594.pcap')
for _ in data.sessions():
    print(_)