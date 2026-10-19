from icecream import ic
import ipaddress
import sys
import subprocess
from datetime import  datetime
from tqdm import tqdm
from libnmap.parser import NmapParser


def executor(cmd):
    process = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return process


def ping(ip):
    pr = executor(
        [
            'ping', 
            '-c1', 
            '-n', 
            '-w3', 
            ip
        ]
    )
    if pr.returncode == 0:
        return True
    else:
        return False


def portscan(ip):
    epoch = datetime.timestamp(datetime.now())
    output = f"nmap_{ip}_{epoch}.xml"
    executor(
        [
            "nmap",
            "-p-",
            "-oX",
            output,
            ip
        ],
    )
    nmap_report = NmapParser.parse_fromfile(output)
    for host in nmap_report.hosts:
        if not host.get_open_ports():
            tqdm.write(f"{ip} has no open ports")
            return []

        proto_list = [f"{port}/{proto}" for port, proto in host.get_open_ports()]
        portstr = ", ".join(proto_list)
        tqdm.write(f"{ip} has open ports ({portstr})")

        portlist = [port for port, _ in host.get_open_ports()]
        return portlist


def main(net):
    tqdm.write(f"Scanning network {net}")
    net = ipaddress.IPv4Network(net, strict=False)
    for host in tqdm(list(net.hosts())):
        if not ping(str(host)):
            tqdm.write(f"{host} is down")
            continue  # Host is down

        # Host is up
        tqdm.write(f"Scanning 65535 port for {host}")
        ports = portscan(str(host))
        if not ports:
            continue
        sys.exit(0)

    pass


if __name__ == '__main__':
    subnet = sys.argv[1]
    main(subnet)


"""
service ?
"""