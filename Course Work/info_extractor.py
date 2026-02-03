"""
Extracts specific information like emails and images from TCP payloads.
"""
import re
import os
from typing import List, Tuple, Any, Set
import dpkt  # type: ignore


def extract_packet_details(packets: List[Tuple[float, int, Any]]) -> None:
    """Scans TCP packets for emails and image GET requests."""
    # We use set to avoid a repeated email appearing more than once
    emails_to: Set[str] = set()
    emails_from: Set[str] = set()
    image_urls: Set[str] = set()
    image_filenames: Set[str] = set()

    # Regex for an email
    re_email = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    # Regex for Image GET request. Split into two lines for PEP8 compliance
    re_img_ext = re.compile(
        rb'GET\s+(.*?\.([jJ][pP][gG]|[jJ][pP][eE][gG]|'
        rb'[pP][nN][gG]|[gG][iI][fF]))\s+HTTP'
    )

    # Regex for the host website where the image file is in
    re_host = re.compile(rb'Host:\s+(.*?)\r\n')

    for _, _, eth in packets:
        ip_obj = eth.data
        # We only want to look inside TCP packets
        if not isinstance(ip_obj.data, dpkt.tcp.TCP):
            continue

        tcp = ip_obj.data
        if len(tcp.data) == 0:
            continue

        try:
            # Decode to skip unreadable characters
            payload_str = tcp.data.decode('utf-8', errors='ignore')

            if "To:" in payload_str or "From:" in payload_str:
                raw_emails = re_email.findall(payload_str)
                for email in raw_emails:
                    if (f"To: <{email}>" in payload_str or
                            f"To: {email}" in payload_str):
                        emails_to.add(email)
                    elif (f"From: <{email}>" in payload_str or
                          f"From: {email}" in payload_str):
                        emails_from.add(email)
        except Exception:  # pylint: disable=broad-exception-caught
            pass

        # Now we extract the image file
        try:
            payload_bytes = tcp.data
            match_path = re_img_ext.search(payload_bytes)

            if match_path:
                path_bytes = match_path.group(1)

                # We try to find Host for full URL
                host_match = re_host.search(payload_bytes)
                if host_match:
                    host_bytes = host_match.group(1)
                    full_url = b"http://" + host_bytes + path_bytes
                    full_url_str = full_url.decode('utf-8', errors='ignore')
                    image_urls.add(full_url_str)

                    # Now we extract the filename
                    path_decoded = path_bytes.decode('utf-8', errors='ignore')
                    filename = os.path.basename(path_decoded)
                    image_filenames.add(filename)
        except Exception:  # pylint: disable=broad-exception-caught
            continue

    # Output findings
    print(f"Unique Emails from: "
          f"{', '.join(emails_from) if emails_from else 'None'}")
    print(f"Unique Emails to:   "
          f"{', '.join(emails_to) if emails_to else 'None'}")

    print("\nImage URLs:")
    for url in image_urls:
        print(f"  {url}")

    print("\nImage Filenames:")
    for fname in image_filenames:
        print(f"  {fname}")