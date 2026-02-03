"""
Calculates statistics and IP pairings from packet data.
"""
import socket
from collections import defaultdict
from typing import List, Tuple, Any, Dict
from packet_parser import get_protocol_name


def print_protocol_summary(packets: List[Tuple[float, int, Any]]) -> None:
    """Prints a table summarizing protocol usage."""
    # Dictionary structure:
    # { "count": 0, "first_ts": inf, "last_ts": 0.0, "total_bytes": 0 }
    stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "count": 0,
        "first_ts": float('inf'),
        "last_ts": 0.0,
        "total_bytes": 0
    })

    for ts, length, eth in packets:
        ip_obj = eth.data
        proto_name = get_protocol_name(ip_obj.p)

        entry = stats[proto_name]
        entry["count"] += 1
        entry["total_bytes"] += length
        if ts < entry["first_ts"]:
            entry["first_ts"] = ts
        if ts > entry["last_ts"]:
            entry["last_ts"] = ts

    # Creating the output table
    print("\n" + "=" * 80)
    print(f"{'Protocol':<10} {'Count':<10} {'First Timestamp':<20} "
          f"{'Last Timestamp':<20} {'Mean Len':<10}")
    print("-" * 80)

    for proto, data in stats.items():
        mean_len = data["total_bytes"] / data["count"]
        print(f"{proto:<10} {data['count']:<10} "
              f"{data['first_ts']:<20.4f} {data['last_ts']:<20.4f} "
              f"{mean_len:<10.2f}")
    print("=" * 80 + "\n")


def get_ip_pairs(packets: List[Tuple[float, int, Any]]) -> Dict[Tuple[str, str], int]:
    """Extracts Source -> Dest IP pairs and counts occurrences."""
    ip_map: Dict[Tuple[str, str], int] = defaultdict(int)

    for _, _, eth in packets:
        ip_obj = eth.data

        try:
            # Convert binary IP to string
            src = socket.inet_ntoa(ip_obj.src)
            dst = socket.inet_ntoa(ip_obj.dst)
            ip_map[(src, dst)] += 1
        except (ValueError, AttributeError):
            continue

    # Printing the results sorted by higher to lower frequency
    sorted_pairs = dict(
        sorted(ip_map.items(), key=lambda item: item[1], reverse=True)
    )

    print("Source IP            Destination IP       Packet Count")
    print("-" * 50)
    for (src, dst), count in sorted_pairs.items():
        print(f"{src:<20} {dst:<20} {count:<10}")

    return sorted_pairs

# References: 
# https://dpkt.readthedocs.io/en/latest/examples.html?utm_source=chatgpt.com
# https://medium.com/%40toxic.foundersorg/analyzing-networking-traffic-using-dpkt-library-2580b929a04
# https://docs.python.org/3/tutorial/inputoutput.html?utm_source=chatgpt.com