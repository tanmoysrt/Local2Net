import subprocess
import re
from flask import Flask, request
 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


def nmap_scan(target_ip):
    nmap = subprocess.Popen(['nmap', target_ip], stdout=subprocess.PIPE)
    stdout, stderr = nmap.communicate()
    return stdout

def get_no_of_closed_ports(data:str):
    return re.findall('Not shown: ([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))? closed ports', data)[0][0]

@app.route('/closed-port-search')
def search_closed_ports():
    ip = request.args["ip"]
    
    try:
        closed_ports_count = get_no_of_closed_ports(nmap_scan(ip).decode('utf-8'))
        return f"Closed ports count: {closed_ports_count}"
    except:
        return "Invalid IP or No port found"

if __name__ == "__main__":
    # print(get_no_of_closed_ports(nmap_scan("192.168.0.1").decode("utf-8") ))
    app.run()