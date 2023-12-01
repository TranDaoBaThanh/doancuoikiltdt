import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tkinter import ttk
import heapq

def dijkstra_algorithm(graph, start_vertex, target_vertex):
    # Initialize distances and predecessors
    distances = {vertex: float('infinity') for vertex in graph.nodes}
    distances[start_vertex] = 0
    predecessors = {vertex: None for vertex in graph.nodes}

    # Priority queue to store vertices with their distances
    priority_queue = [(0, start_vertex)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Check if the current distance is greater than the known distance
        if current_distance > distances[current_vertex]:
            continue

        # Explore neighbors
        for neighbor, edge_data in graph[current_vertex].items():
            distance = distances[current_vertex] + edge_data['weight']

            # Update distance and predecessor if a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct the shortest path
    shortest_path = []
    current_vertex = target_vertex

    while current_vertex is not None:
        shortest_path.insert(0, current_vertex)
        current_vertex = predecessors[current_vertex]

    return shortest_path, distances[target_vertex]

# Modify your existing dijkstra function
def dijkstra():
    try:
        num_vertices = int(entry_vertices.get())
        matrix_values = scrolledtext_matrix.get("1.0", tk.END).strip().split('\n')

        adjacency_matrix = []
        for row in matrix_values:
            values = list(map(int, row.split()))
            adjacency_matrix.append(values)

        if len(adjacency_matrix) != num_vertices or any(len(row) != num_vertices for row in adjacency_matrix):
            raise ValueError("Invalid input. Please make sure the matrix is square and has the correct number of vertices.")

        G = nx.from_numpy_array(np.array(adjacency_matrix))

        source_node = simpledialog.askinteger("Start Vertex", "Enter the starting vertex (0 to {}):".format(num_vertices - 1),
                                               minvalue=0, maxvalue=num_vertices - 1)
        target_node = simpledialog.askinteger("Target Vertex", "Enter the target vertex (0 to {}):".format(num_vertices - 1),
                                               minvalue=0, maxvalue=num_vertices - 1)

        if source_node is None or target_node is None:
            return  # If the user presses Cancel

        # Call the dijkstra_algorithm function
        shortest_path, shortest_path_length = dijkstra_algorithm(G, source_node, target_node)

        # Tạo cửa sổ mới để hiển thị biểu đồ
        graph_window = tk.Toplevel(root)
        graph_window.title("Đồ thị và đường đi ngắn nhất")

        # Tạo đồ thị và đường đi ngắn nhất trên Canvas
        figure, ax = plt.subplots(figsize=(5, 5))
        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        # Vẽ đồ thị và đường đi ngắn nhất
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        ax.set_title("Thuật toán Dijkstra")
        #plt.text(0.2, 1.1, f"Đường đi ngắn nhất từ đỉnh {source_node} đến đỉnh {target_node} : {shortest_path} = {shortest_path_length}", fontsize=10, color='red', ha='center', va='center')
        plt.text(0.5, -0.1, f"Đường đi ngắn nhất từ đỉnh {source_node} đến đỉnh {target_node}: {shortest_path} = {shortest_path_length}", fontsize=10, color='red', ha='center', va='center', transform=plt.gca().transAxes)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black', ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=[(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)], edge_color='red', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_size=700, node_color='red', ax=ax)

        canvas.draw()

    except ValueError as e:
        tk.messagebox.showerror("Error", str(e))

def prim_algorithm(graph, start_vertex):
    # Hàm thực hiện thuật toán Prim bắt đầu từ đỉnh start_vertex
    min_spanning_tree = nx.Graph()
    visited = set([start_vertex])

    while len(visited) < len(graph.nodes):
        possible_edges = []

        for node in visited:
            possible_edges.extend(graph.edges(node, data=True))

        # Lọc ra các cạnh mà không kết nối đỉnh đã thăm
        possible_edges = [edge for edge in possible_edges if edge[1] not in visited]

        # Tìm cạnh có trọng số nhỏ nhất
        min_edge = min(possible_edges, key=lambda x: x[2]['weight'])

        # Thêm cạnh vào cây khung nhỏ nhất
        min_spanning_tree.add_edge(min_edge[0], min_edge[1], weight=min_edge[2]['weight'])
        visited.add(min_edge[1])

    return min_spanning_tree

def prim():
    try:
        num_vertices = int(entry_vertices.get())
        matrix_values = scrolledtext_matrix.get("1.0", tk.END).strip().split('\n')

        adjacency_matrix = []
        for row in matrix_values:
            values = list(map(int, row.split()))
            adjacency_matrix.append(values)

        if len(adjacency_matrix) != num_vertices or any(len(row) != num_vertices for row in adjacency_matrix):
            raise ValueError("Invalid input. Please make sure the matrix is square and has the correct number of vertices.")

        G = nx.from_numpy_array(np.array(adjacency_matrix))

        root.withdraw()
        start_vertex = simpledialog.askinteger("Start Vertex", "Enter the starting vertex (0 to {}):".format(num_vertices - 1),
                                               minvalue=0, maxvalue=num_vertices - 1)

        if start_vertex is None:
            return  # If the user presses Cancel

        min_spanning_tree = prim_algorithm(G, start_vertex)

        # Create a new window to display the Minimum Spanning Tree
        graph_window = tk.Toplevel(root)
        graph_window.title("Minimum Spanning Tree")

        # Create a graph and minimum spanning tree on the Canvas
        figure, ax = plt.subplots(figsize=(5, 5))
        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        pos = nx.spring_layout(G)

        # Draw the Minimum Spanning Tree
        nx.draw(min_spanning_tree, pos, edge_color='red', with_labels=True, font_weight='bold', node_size=700,
                node_color='skyblue', font_color='black', ax=ax)

        # Draw edge labels (weights)
        labels = nx.get_edge_attributes(min_spanning_tree, 'weight')
        nx.draw_networkx_edge_labels(min_spanning_tree, pos, edge_labels=labels, ax=ax)
        nx.draw_networkx_nodes(min_spanning_tree, pos, nodelist=[start_vertex], node_size=700, node_color='green', ax=ax)

        canvas.draw()

    except ValueError as e:
        tk.messagebox.showerror("Error", str(e))

def perform_algorithm():
    selected_algorithm = combobox.get()
    if selected_algorithm == 'Prim':
        prim()
    elif selected_algorithm == 'Dijkstra':
        dijkstra()

root = tk.Tk()
root.title("Mo phong truc quan thuat toan")
root.geometry('450x300')
root['bg'] = 'pink'

label_vertices = tk.Label(root, text="Nhập số đỉnh:", font = ('Verdena', 14), bg = 'pink')
label_vertices.place(x = 20, y = 30)

entry_vertices = tk.Entry(root,width= 10, font= ('Verdena',12))
entry_vertices.place(x = 170, y = 33)

label_matrix = tk.Label(root, text="Nhập ma trận kề:", font = ('Verdena', 14), bg = 'pink')
label_matrix.place(x = 20, y = 80 )

scrolledtext_matrix = scrolledtext.ScrolledText(root, width=30, height=8, font = ('Verdena',10))
scrolledtext_matrix.place(x=170, y=80)

lable_chon = tk.Label(root, text= "Thuật toán:", font= ('Verdena',14), bg= 'pink')
lable_chon.place(x = 20, y = 250)

combobox = ttk.Combobox(root, font = ('Verdena'), width= 10)
combobox['value'] = ('Prim', 'Dijkstra')
combobox.place(x = 150, y = 250)

button_do = tk.Button(root, text="Thực hiện", font = ('verdena',12), command= perform_algorithm )
button_do.place(x = 300, y = 250)
    

root.mainloop()