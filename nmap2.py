
import nmap

# Create an nmap object
nm = nmap.PortScanner()

# Scan google.com for common ports
nm.scan('google.com', arguments='-p 1-1024')

# Print the results
print(nm.csv())
