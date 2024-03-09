
import socket

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        return "Error: " + str(e)

domain = "google.com"
ip_address = get_ip_address(domain)
print("IP Address of", domain, "is:", ip_address)
