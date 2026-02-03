"""
Parses a PCAP file and extracts raw packet data.
"""
import sys
import socket
from typing import List, Tuple, Any
import dpkt  # type: ignore

# Dictionary for fast protocol mapping
PROTOCOL_MAP = {
    socket.IPPROTO_TCP: 'TCP',
    socket.IPPROTO_UDP: 'UDP',
    socket.IPPROTO_ICMP: 'ICMP',
    socket.IPPROTO_IGMP: 'IGMP'
}


def get_protocol_name(protocol_num: int) -> str:
    """Map protocol numbers to names."""
    # Check our dictionary first
    if protocol_num in PROTOCOL_MAP:
        return PROTOCOL_MAP[protocol_num]

    # Check the system for new protocol.
    # Note: getprotobynumber is not available on all Windows Python builds
    try:
        func = getattr(socket, 'getprotobynumber', None)
        if func:
            return func(protocol_num)
        return f"Other({protocol_num})"
    except (OSError, AttributeError):
        return f"Other({protocol_num})"


def load_pcap(filename: str) -> List[Tuple[float, int, Any]]:
    """
    Load a PCAP file.
    Returns: List of (timestamp, packet_length, dpkt_ethernet_object)
    """
    packet_data: List[Tuple[float, int, Any]] = []

    try:
        with open(filename, 'rb') as f:
            pcap = dpkt.pcap.Reader(f)

            for ts, buf in pcap:
                # Ensure if there is a bad packet program continues
                try:
                    total_len = len(buf)
                    # Transforms bits into readable eth frame
                    eth = dpkt.ethernet.Ethernet(buf)

                    # Checking if it is a valid IP packet
                    if isinstance(eth.data, (dpkt.ip.IP, dpkt.ip6.IP6)):
                        packet_data.append((ts, total_len, eth))

                except (dpkt.dpkt.UnpackError, IndexError):
                    continue
            return packet_data

    except FileNotFoundError:
        print(f"File {filename} not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Invalid format - {e}", file=sys.stderr)
        return []
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Unexpected Error: {e}", file=sys.stderr)
        return []
    
# References
# https://realpython.com/python-sockets/?utm_source=chatgpt.com
# https://docs.python.org/3.12/library/socket.html?utm_source=chatgpt.com