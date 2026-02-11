#!/usr/bin/env python3

"""
GhostCat Community Edition
Lightweight cross-platform LAN discovery tool.
Authorized networks only.
"""

import argparse
import socket
import ipaddress
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import sys


VERSION = "0.1.0"
DEFAULT_PORTS = [80, 443]
MAX_WORKERS = 25


def setup_logging():
    logging.basicConfig(
        filename="ghostcat.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def print_banner():
    print("\n==============================")
    print(f"GhostCat Community v{VERSION}")
    print("Lightweight LAN Discovery Tool")
    print("Authorized Networks Only")
    print("==============================\n")


def check_host(ip, ports):
    open_ports = []

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((str(ip), port))
            sock.close()

            if result == 0:
                open_ports.append(port)

        except Exception:
            continue

    if open_ports:
        return {
            "ip": str(ip),
            "open_ports": open_ports,
            "timestamp": datetime.utcnow().isoformat()
        }

    return None


def scan_network(cidr, ports):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        print("Invalid CIDR range.")
        sys.exit(1)

    logging.info(f"Starting scan on {cidr}")
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(check_host, ip, ports): ip
            for ip in network.hosts()
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
                print(f"{result['ip']} → Open: {result['open_ports']}")

    print(f"\nScan complete. {len(results)} responsive hosts found.")
    logging.info(f"Scan complete. {len(results)} hosts found.")
    return results


def export_results(results):
    filename = f"ghostcat_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\nResults exported to {filename}")
    logging.info(f"Results exported to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="GhostCat Community - Cross-platform LAN discovery tool"
    )

    parser.add_argument(
        "-s", "--scan",
        help="Scan a network range (example: 192.168.1.0/24)"
    )

    parser.add_argument(
        "-p", "--ports",
        help="Comma-separated list of ports (default: 80,443)"
    )

    parser.add_argument(
        "-e", "--export",
        action="store_true",
        help="Export results to JSON"
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version"
    )

    args = parser.parse_args()

    if args.version:
        print(f"GhostCat Community v{VERSION}")
        sys.exit(0)

    setup_logging()
    print_banner()

    if not args.scan:
        parser.print_help()
        sys.exit(0)

    if args.ports:
        ports = [int(p.strip()) for p in args.ports.split(",")]
    else:
        ports = DEFAULT_PORTS

    results = scan_network(args.scan, ports)

    if args.export and results:
        export_results(results)


if __name__ == "__main__":
    main()
