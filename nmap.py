
import nmap

target = 'google.com'

nm = nmap.PortScanner()
nm.scan(target, '22-443')

for host in nm.all_hosts():
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    print('State : %s' % nm[host].state())

    for proto in nm[host].all_protocols():
        print('----------')
        print('Protocol : %s' % proto)

        lport = nm[host][proto].keys()
        lport = sorted(lport)
        for port in lport:
            print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
