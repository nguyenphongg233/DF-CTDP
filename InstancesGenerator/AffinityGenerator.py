"""
Hanoi University of Science and Technology, School of information and communication technology
Hanoi, Vietnam

Affinity generator for CTDP 2026 - Tiki Joint R&D Lab

run_script and provide input in the format:
python AffinityGenerator.py <input_file> <output_file> <type>
Example input: Python AffinityGenerator.py input.txt output.txt I1
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
    def __init__(self, num_nodes = 500, num_districts = 20, tau = [0.05, 0.05, 0.05], num_attributes = 3):
        self.num_nodes = num_nodes
        self.num_districts = num_districts
        self.num_edges = 0
        self.tau = tau
        self.num_attributes = num_attributes
        self.nodes = []
        self.edges = []
        self.adjacency_list = {i: set() for i in range(num_nodes)}
        self.familiarity_matrix = np.zeros((num_districts, num_nodes), dtype = int)

    def read_input(self, filename):
        with open(filename, 'r') as f:
            # Read graph parameters from input
            self.num_nodes = int(f.readline())
            for _ in range(self.num_nodes):
                line = f.readline().strip().split()
                id = int(line[0])
                x_coord = float(line[1])
                y_coord = float(line[2])
                w = list(map(float, line[3:3 + self.num_attributes]))
                self.nodes.append(Node(id, x_coord, y_coord, w))
            
            self.num_edges = int(f.readline())
            for _ in range(self.num_edges):
                u, v = map(int, f.readline().strip().split())
                self.adjacency_list[u].add(v)
                self.adjacency_list[v].add(u)
                self.edges.append((u, v))

            line = f.readline().strip().split()
            self.num_districts = int(line[0])
            self.tau = list(map(float, line[1:1 + self.num_attributes]))
            # self.num_districts, self.tau[0], self.tau[1], self.tau[2] = map(float, f.readline().strip().split())
        
        self.familiarity_matrix.resize((self.num_districts, self.num_nodes), refcheck = False)

    def H_generate_graph(self):
        # Homogeneous graph generation logic
        for i in range(self.num_districts):
            for j in range(self.num_nodes):
                self.familiarity_matrix[i][j] = 1 
    def I1_generate_graph(self):
        # choose unique random centers among nodes
        if self.num_nodes >= self.num_districts:
            centers = random.sample(range(self.num_nodes), self.num_districts)
        else:
            centers = [random.randrange(self.num_nodes) for _ in range(self.num_districts)]

        HighestFamilarityRatio = max(1, self.num_nodes // self.num_districts)
        SecondHighestFamilarityRatio = max(1, (self.num_nodes // self.num_districts) * 2)

        for idx in range(self.num_districts):
            center = centers[idx]
            visited = [False] * self.num_nodes
            q = [center]
            visited[center] = True
            cnt = 1
            while q:
                u = q.pop(0)
                cnt += 1
                if cnt <= HighestFamilarityRatio:
                    self.familiarity_matrix[idx][u] = 1
                elif cnt <= HighestFamilarityRatio + SecondHighestFamilarityRatio:
                    self.familiarity_matrix[idx][u] = 2
                else:
                    self.familiarity_matrix[idx][u] = 3

                for v in self.adjacency_list[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)

    def I2_generate_graph(self):
        HighestFamilarityRatio = max(1,self.num_nodes // self.num_districts)
        SecondHighestFamilarityRatio = max(1, (self.num_nodes // self.num_districts) * 2)
        
        for _ in range(self.num_districts):
            root_ratio = random.randint(1, HighestFamilarityRatio)
            root_nodes = [np.random.randint(0, self.num_nodes - 1) for _ in range(root_ratio)]

            visited = [False] * self.num_nodes
            q = root_nodes[:]
            for node in root_nodes:
                visited[node] = True
                self.familiarity_matrix[_][node] = 1
            cnt = root_nodes.__len__()
            while q:               
                u = q.pop(0)
                for v in self.adjacency_list[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)
                        cnt += 1
                        if cnt <= HighestFamilarityRatio:
                            self.familiarity_matrix[_][v] = 1
                        elif cnt <= HighestFamilarityRatio + SecondHighestFamilarityRatio:
                            self.familiarity_matrix[_][v] = 2
                        else:
                            self.familiarity_matrix[_][v] = 3
    def generate_graph(self, type):
        if type == "H":
            self.H_generate_graph()
        elif type == "I1":
            self.I1_generate_graph()
        elif type == "I2":
            self.I2_generate_graph()
        else:
            raise ValueError("Invalid graph type. Use 'H', 'I1', or 'I2'.")

    def visualize(self):
        if not self.nodes or self.familiarity_matrix is None:
            return

        xs = np.array([node.x_coord for node in self.nodes], dtype=float)
        ys = np.array([node.y_coord for node in self.nodes], dtype=float)
        edges = np.array(self.edges, dtype=int) if self.edges else None
        cmap = plt.cm.viridis

        for district in range(self.num_districts):
            fig, ax = plt.subplots(figsize=(8, 8), facecolor="#f7f4ee")
            ax.set_facecolor("#fffdf8")

            if edges is not None and len(edges) > 0:
                for u, v in edges:
                    ax.plot(
                        [xs[u], xs[v]],
                        [ys[u], ys[v]],
                        color="#c7c2bb",
                        linewidth=0.8,
                        alpha=0.45,
                        zorder=1,
                    )

            fam = self.familiarity_matrix[district]
            scatter = ax.scatter(
                xs,
                ys,
                c=fam,
                cmap=cmap,
                vmin=1,
                vmax=3,
                s=60,
                edgecolors="#1f1f1f",
                linewidths=0.6,
                zorder=2,
            )

            offset = max(np.ptp(xs), np.ptp(ys)) * 0.01 if self.num_nodes > 0 else 1.0
            for node in self.nodes:
                ax.text(
                    node.x_coord + offset,
                    node.y_coord + offset,
                    str(node.id),
                    fontsize=8,
                    color="#1a1a1a",
                    zorder=3,
                )

            cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_ticks([1, 2, 3])
            cbar.set_label(f"Familiarity - district {district + 1}")

            ax.set_title(f"District {district + 1}", fontsize=14, weight="bold", pad=12)
            ax.set_aspect("equal", adjustable="box")
            ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.2)
            fig.tight_layout()
            plt.show()
            plt.close(fig)

        
    def write_output(self, filename):
        with open(filename, 'w') as f:
            f.write(f"{self.num_nodes}\n")
            for node in self.nodes:
                f.write(node.to_text_line() + "\n")
            f.write(f"{self.num_edges}\n")
            for u, v in self.edges:
                f.write(f"{u} {v}\n")
            f.write(f"{self.num_districts} {' '.join(map(str, self.tau))}\n")
            for i in range(self.num_districts):
                f.write(' '.join(map(str, self.familiarity_matrix[i])) + "\n")
            

def main():

    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    type = sys.argv[3] if len(sys.argv) > 3 else "H"
    # type = "H" for homongeneous, "I1" for Inhomogeneous with 1 centroids, "I2" for Inhomogeneous with 2 centroids
    graph = Graph()
    graph.read_input(input_file)
    graph.generate_graph(type)
    graph.write_output(output_file)
    # graph.visualize()

if __name__ == "__main__":
    main()


    