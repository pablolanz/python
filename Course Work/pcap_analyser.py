"""
Main entry point for the Network Trace Analyser. To run the code,
user will be asked to enter a file which must be a valid pcap file
located in the same folder as the modules
"""
import sys
import os
import packet_parser
import stats_manager
import info_extractor
import visualiser


def main() -> None:
    """Orchestrates the analysis modules."""
    # Asking for a valid pcap file
    try:
        user_input = input("Enter the name of the pcap file: ").strip()
        pcap_filename = user_input.strip('"').strip("'")
    except KeyboardInterrupt:
        print("\nUser cancelled input.")
        sys.exit(0)

    if not os.path.isfile(pcap_filename):
        print(f"File '{pcap_filename}' not found.", file=sys.stderr)
        sys.exit(1)

    # Open and Parse
    packets = packet_parser.load_pcap(pcap_filename)
    if not packets:
        sys.exit(0)

    # Summarise Contents
    stats_manager.print_protocol_summary(packets)

    # Extract email information
    info_extractor.extract_packet_details(packets)

    # Extract IP pairs
    ip_pairs = stats_manager.get_ip_pairs(packets)

    # Make network graphic
    visualiser.create_network_graph(ip_pairs)

    # Make time plot
    visualiser.plot_packet_timeline(packets, interval=2)

    print("Analysis Finished.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("User aborted program.", file=sys.stderr)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Critical Error: {e}", file=sys.stderr)