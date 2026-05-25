"""    
Hanoi University of Science and Technology, School of information and communication technology
Hanoi, Vietnam

Planar graph generator for CTDP 2026 - Tiki Joint R&D Lab

This code generates a random planar graph with specified parameters, including the number of nodes, edges, and districts.
It uses Delaunay triangulation to create a planar embedding and ensures connectivity by constructing a minimum spanning tree. 
The node attributes are generated based on specified ranges, and the graph can be visualized using Matplotlib.

run the script and provide input in the format:
python planar_graph_ver2.py no-visualize <num_nodes> <num_districts> <tau>

The output will be a text representation of the graph, including node information and edges, as well as a visualization of the graph structure.
"""

import random
import numpy as np
from scipy.spatial import Delaunay
import networkx as nx
import matplotlib.pyplot as plt
import sys

class Node:
    def __init__(self, id, x_coord, y_coord, w):
        self.id = id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.w = w

    def to_text_line(self):
        return f"{self.id} {self.x_coord:.6f} {self.y_coord:.6f} {self.w[0]} {self.w[1]} {self.w[2]} "


class Graph:
    def __init__(self, num_nodes = 500, num_districts = 20, tau = [0.05, 0.05, 0.05], num_attributes = 3, coord_range = 1000, w_ranges = ((4, 20), (15, 400), (15, 100)), jitter_eps = 1e-8):
        self.num_nodes = num_nodes
        self.num_districts = num_districts
        self.tau = tau
        self.num_attributes = num_attributes
        self.coord_range = coord_range
        self.w_ranges = w_ranges
        self.jitter_eps = jitter_eps

        self.nodes = []
        self.points = None
        self.edges = []
        self.adjacency_list = {i: set() for i in range(num_nodes)}

    def _generate_points(self):
        # Generate random points and ensure uniqueness by adding jitter if necessary
        pts = np.random.uniform(0.0, self.coord_range, size = (self.num_nodes, 2))
        _, idx_counts = np.unique(np.round(pts, 8), axis = 0, return_counts = True)
        if np.any(idx_counts > 1):
            pts += np.random.normal(scale = self.jitter_eps, size = pts.shape)
        return pts

    def _delaunay_edges(self, pts):
        # Compute Delaunay triangulation and extract edges, with a fallback for degenerate cases
        try:
            tri = Delaunay(pts)
        except Exception:
            pts = pts + np.random.normal(scale = 1e-6, size = pts.shape)
            tri = Delaunay(pts)

        edge_set = set()
        for simplex in tri.simplices:
            for i in range(3):
                a = int(simplex[i])
                b = int(simplex[(i + 1) % 3])
                if a == b:
                    continue
                if a > b:
                    a, b = b, a
                edge_set.add((a, b))

        return pts, list(edge_set)

    def _choose_edges(self, pts, delaunay_edges, num_edges):
        # Build a graph from Delaunay edges and compute a minimum spanning tree to ensure connectivity
        # Then add remaining edges randomly until we reach the desired number of edges
        graph = nx.Graph()
        for u, v in delaunay_edges:
            dist = np.linalg.norm(pts[u] - pts[v])
            graph.add_edge(u, v, weight = dist)

        tree = nx.minimum_spanning_tree(graph, weight = "weight")
        chosen = set(tuple(sorted(e)) for e in tree.edges())

        remaining = []
        for u, v in delaunay_edges:
            if (u, v) in chosen:
                continue
            dist = np.linalg.norm(pts[u] - pts[v])
            remaining.append((dist, u, v))

        random.shuffle(remaining)
        for _, u, v in remaining:
            if len(chosen) >= num_edges:
                break
            chosen.add((u, v))

        return list(chosen)

    def _generate_nodes(self, pts):
        # Generate node attributes w based on specified ranges and create Node instances
        nodes = []
        for i in range(self.num_nodes):
            w = [
                random.randint(*self.w_ranges[0]),
                random.randint(*self.w_ranges[1]),
                random.randint(*self.w_ranges[2]),
            ]
            nodes.append(Node(i, float(pts[i][0]), float(pts[i][1]), w))
        return nodes

    def _build_adjacency_list(self):
        # Build an adjacency list from the edges for efficient graph representation
        self.adjacency_list = {i: set() for i in range(self.num_nodes)}
        for u, v in self.edges:
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)

    def generate(self, num_edges=None):
        # If num_edges is not provided, randomly choose a number of edges between n-1 and 3n-6 to ensure we can create a connected planar graph
        if num_edges is None:
            num_edges = random.randint(self.num_nodes - 1, 3 * self.num_nodes - 6)

        pts = self._generate_points()
        pts, delaunay_edges = self._delaunay_edges(pts)
        self.edges = self._choose_edges(pts, delaunay_edges, num_edges)
        self.points = pts
        self.nodes = self._generate_nodes(pts)
        self._build_adjacency_list()
        return self

    def to_text_lines(self):

        lines = [str(self.num_nodes)]
        for node in self.nodes:
            lines.append(node.to_text_line())

        lines.append(str(len(self.edges)))
        for u, v in self.edges:
            lines.append(f"{u} {v}")

        lines.append(f"{self.num_districts} { ' '.join(str(tau) for tau in self.tau) if self.tau is not None else 0 }")
        return lines, self.num_districts

    def visualize(self):
        if self.points is None:
            return

        fig, ax = plt.subplots(figsize = (10, 10), facecolor = "#f7f4ee")
        ax.set_facecolor("#fffdf8")

        pts = self.points
        w1 = np.array([node.w[0] for node in self.nodes], dtype=float)
        base = float(w1.min())
        span = float(np.ptp(w1)) + 1e-9
        scaled = (w1 - base) / span

        for u, v in self.edges:
            ax.plot(*pts[[u, v]].T, color = "#8a867f", lw = 1.0, alpha = 0.35, zorder = 1)

        scatter = ax.scatter(pts[:, 0], pts[:, 1], s = 80 + scaled * 180, c = scaled, cmap = "viridis", edgecolors = "#1f1f1f", linewidths = 0.8, zorder = 3)

        offset = coord_offset(pts)
        label_box = dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.8)
        for node in self.nodes:
            ax.text(node.x_coord + offset, node.y_coord + offset, str(node.id), fontsize=8, weight="semibold", color="#1a1a1a", zorder=4, bbox=label_box)

        fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04).set_label("Node weight w1", rotation=90)
        ax.set(title = f"Planar graph | num_nodes = {self.num_nodes}, num_edges = {len(self.edges)}")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.22)
        ax.tick_params(labelsize=9, colors="#444444")
        for spine in ax.spines.values():
            spine.set_color("#c8c2b8")

        fig.tight_layout()
        plt.show()

    def to_result_dict(self, visualize=True):
        lines, p = self.to_text_lines()
        if visualize:
            self.visualize()

        params = [tuple(node.w) for node in self.nodes]
        return {
            "text_lines": lines,
            "points": self.points,
            "params": params,
            "edges": self.edges,
            "p": p,
        }


def generate_planar_graph(num_nodes = 500, num_districts = 10, tau = [0.05, 0.05, 0.05], num_edges = None, coord_range = 1000, w_ranges = ((4, 20), (15, 400), (15, 100)), seed = None, visualize = True, jitter_eps = 1e-8):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    graph = Graph(num_nodes = num_nodes, num_districts = num_districts, tau = tau, coord_range = coord_range, w_ranges = w_ranges, jitter_eps = jitter_eps)
    graph.generate(num_edges = num_edges)
    return graph.to_result_dict(visualize = visualize)

def coord_offset(pts):
    rng = np.ptp(pts, axis=0)
    return max(rng[0], rng[1]) * 0.01 if rng.size > 0 else 1.0

if __name__ == "__main__":
    visualize = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == "no-visualize":
        visualize = False
    if len(sys.argv) > 4 :
        num_nodes, num_districts = map(int, sys.argv[2:4])
        tau = float(sys.argv[4])
    # num_nodes, num_districts = map(int, input().split())
    # tau = float(input())
    tau = [tau] * 3

    out = generate_planar_graph(num_nodes = num_nodes, tau = tau, num_districts = num_districts, visualize = visualize)
    print("\n".join(out["text_lines"]))
