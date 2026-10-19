from icecream import ic
import ipaddress
import sys
import subprocess
from datetime import  datetime
from tqdm import tqdm
from libnmap.parser import NmapParser
import os
from concurrent.futures import ThreadPoolExecutor


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
        tqdm.write(f"{ip} is up")
        return True, ip
    else:
        return False, ip


def portscan(ip):
    epoch = datetime.timestamp(datetime.now())
    output = f"output/nmap_{ip}_{epoch}.xml"
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
            return []

        proto_list = [f"{port}/{proto}" for port, proto in host.get_open_ports()]
        portstr = ", ".join(proto_list)
        tqdm.write(f"{ip} has open ports ({portstr})")

        portlist = [str(port) for port, _ in host.get_open_ports()]
        return portlist, ip


def servicescan(ip, portlst):
    epoch = datetime.timestamp(datetime.now())
    output = f"output/nmap_{ip}_{epoch}/{ip}"
    os.makedirs(f"output/nmap_{ip}_{epoch}", exist_ok=True)
    tqdm.write(' '.join([
        "nmap", "-p", ",".join(portlst),
        "-A", "-oA", output, ip
    ]))
    executor(
        [
            "nmap",
            "-p",
            ",".join(portlst),
            "-oA",
            output,
            ip
        ],
    )


def main(net):
    scanned = {}
    tqdm.write(f"Scanning network {net}")
    net = ipaddress.IPv4Network(net, strict=False)

    with ThreadPoolExecutor(max_workers=min(20, len(list(net.hosts())))) as exec:
        res = exec.map(ping, [str(h) for h in net.hosts()])

    for future in res:
        status, host = future
        scanned[host] = {
                "ports": [],
                "live": status
            }

    live_targets = len([k for k, v in scanned.items() if v.get("live", False)])
    tqdm.write(f"Scanning 65535 ports for {live_targets} hosts up")
    with ThreadPoolExecutor(max_workers=min(5, live_targets)) as exec:
        futures = []
        for ip, details in scanned.items():
            if details.get("live", False):
                futures.append(exec.submit(portscan, ip))


    for future in futures:
        ports, ip = future.result()
        if not ports:
            continue
        scanned[ip]["ports"] = ports

    hot_targets = len([k for k, v in scanned.items() if v.get("ports", [])])
    tqdm.write(f"Scanning open ports on {hot_targets} targets")
    with ThreadPoolExecutor(max_workers=min(5, hot_targets)) as exec:
        futures = []
        for ip, details in scanned.items():
            if details.get("ports", []):
                futures.append(exec.submit(servicescan, ip, details.get("ports", [])))

    sys.exit(0)


if __name__ == '__main__':
    subnet = sys.argv[1]
    main(subnet)
