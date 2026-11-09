from icecream import ic
import ipaddress
import sys
import subprocess
from tqdm import tqdm
from libnmap.parser import NmapParser
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def executor(cmd):
    process = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return process


def ping(argtup):
    ip, out = argtup
    upfile = Path(f"output/{out}/ping/{ip}.up")
    downfile = Path(f"output/{out}/ping/{ip}.down")
    if upfile.exists():
        tqdm.write(f"{ip} is up")
        return True, ip
    if downfile.exists():
        return False, ip

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
        upfile.touch()
        return True, ip
    else:
        downfile.touch()
        return False, ip


def portscan(ip, out):
    output = f"output/{out}/portscan/{ip}.xml"
    if not Path(output).exists():
        executor(
            [
                "nmap",
                "-p-",
                "-oX", output,
                "--host-timeout", "1h",
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


def servicescan(ip, portlst, out):
    output = f"output/{out}/servicescan/{ip}"
    os.makedirs(output, exist_ok=True)
    tqdm.write(' '.join([
        "nmap", "-p", ",".join(portlst),
        "-A", "-oA", output, ip
    ]))
    if not Path(f"{output}/{ip}.xml").exists():
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


def main(net, proj):
    scanned = {}
    tqdm.write(f"Scanning network {net}")
    if not os.path.isdir(f'output/{proj}'):
        os.makedirs(f'output/{proj}', exist_ok=True)
        os.makedirs(f'output/{proj}/ping', exist_ok=True)
        os.makedirs(f'output/{proj}/portscan', exist_ok=True)
        os.makedirs(f'output/{proj}/servicescan', exist_ok=True)

    net = ipaddress.IPv4Network(net, strict=False)

    with ThreadPoolExecutor(max_workers=min(20, len(list(net.hosts())))) as exec:
        res = exec.map(ping, [(str(h), proj) for h in net.hosts()])

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
                futures.append(exec.submit(portscan, ip, proj))


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
                futures.append(exec.submit(servicescan, ip, details.get("ports", []), proj))

    sys.exit(0)


if __name__ == '__main__':
    subnet = sys.argv[1]
    project = sys.argv[2]
    main(subnet, project)
    """
    proj
        ping
            1.up
            2.down
        portscan
            1.xml
        servicescan
            1
                1.nmap
                1.gnmap
                1.xml   
    """
