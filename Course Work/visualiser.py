"""
Visualizes network data using Graphs and Plots.
"""
import sys
import statistics
from typing import Dict, Tuple, List, Any
import networkx as nx  # type: ignore
import matplotlib.pyplot as plt  # type: ignore


def create_network_graph(ip_pairs: Dict[Tuple[str, str], int]) -> None:
    """Generates a directed graph of IP communications."""
    print("Generating Network Graph", file=sys.stdout)

    graph = nx.DiGraph()

    # Adding edges
    for (src, dst), count in ip_pairs.items():
        graph.add_edge(src, dst, weight=count)

    # Information about the graph
    print("--- Graph Statistics ---")
    print(f"Number of Nodes: {graph.number_of_nodes()}")
    print(f"Number of Edges: {graph.number_of_edges()}")

    # Drawing
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, k=3, iterations=50)

    # Making nodes show IP addresses
    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_labels(graph, pos, font_size=8)

    # Making lines be thicker based on appearances (weight)
    weights = [graph[u][v]['weight'] for u, v in graph.edges()]
    # Normalize weights to avoid massive lines
    max_w = max(weights) if weights else 1
    normalized_widths = [(w / max_w) * 4 + 0.5 for w in weights]

    nx.draw_networkx_edges(
        graph, pos, width=normalized_widths, arrowstyle='->', arrowsize=20
    )

    plt.title("Network Traffic Flow (Thickness = Packet Count)")
    plt.axis('off')

    output_file = "network_graph.png"
    plt.savefig(output_file)
    print(f"Graph saved to {output_file}", file=sys.stdout)
    plt.show()
    plt.close()


def plot_packet_timeline(packets: List[Tuple[float, int, Any]],
                         interval: int = 15) -> None:
    """Generates a timeline of packet volume."""
    print("Generating Timeline Plot", file=sys.stdout)

    if not packets:
        return
    # variables for the plot
    start_time = packets[0][0]
    end_time = packets[-1][0]
    duration = end_time - start_time

    # Grouping the packets into equal length time intervals
    num_bins = int(duration // interval) + 1
    bins = [0] * num_bins

    for ts, _, _ in packets:
        bin_idx = int((ts - start_time) // interval)
        if 0 <= bin_idx < num_bins:
            bins[bin_idx] += 1

    # Calculating the threshold for heavy traffic (Mean + 2*sd)
    if len(bins) > 1:
        mean_val = statistics.mean(bins)
        stdev_val = statistics.stdev(bins)
        threshold = mean_val + (2 * stdev_val)
    else:
        threshold = mean_val = 0

    # Making the line chart
    time_axis = [i * interval for i in range(num_bins)]

    plt.figure(figsize=(12, 6))
    plt.plot(time_axis, bins, label='Packets per Interval',
             marker='o', markersize=3)

    # Showing threshold visually
    plt.axhline(y=threshold, color='red', linestyle='--', linewidth=2,
                label=f'Threshold (Mean+2SD): {threshold:.2f}')

    plt.title(f"Traffic Volume Over Time (Bin Size: {interval}s)")
    plt.xlabel("Time (seconds relative to start)")
    plt.ylabel("Packet Count")
    plt.legend()
    plt.grid(True, alpha=0.3)

    output_file = "packet_timeline.png"
    plt.savefig(output_file)
    plt.show()
    plt.close()

    # References
    # https://www.wikitechy.com/tutorial/matplotlib/?utm_source=chatgpt.com
    # https://networkx.org/documentation/stable/tutorial.html?utm_source=chatgpt.com