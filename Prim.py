import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def create_graph():
    try:
        num_vertices = int(entry_vertices.get()) #so dinh cua do thi
        matrix_values = scrolledtext_matrix.get("1.0", tk.END).strip().split('\n') #gia tri cua ma tran ke

        # tach matri ra
        adjacency_matrix = []
        for row in matrix_values:
            values = list(map(int, row.split()))
            adjacency_matrix.append(values)

        #neu nguoi nhap de null thi xuat ra man hinh
        if len(adjacency_matrix) != num_vertices or any(len(row) != num_vertices for row in adjacency_matrix):
            raise ValueError("Invalid input. Please make sure the matrix is square and has the correct number of vertices.")

        #tao do thi G tu adjicency_matri
        G = nx.from_numpy_array(np.array(adjacency_matrix))

        # Yêu cầu người dùng nhập đỉnh xuất phát
        start_vertex = simpledialog.askinteger("Start Vertex", "Enter the starting vertex (0 to {}):".format(num_vertices - 1), minvalue=0, maxvalue=num_vertices - 1)

        if start_vertex is None:
            return  # Nếu người dùng nhấn Cancel

        #dung ham minimum_spanning_tree de tim cay khung nho nhat bang thuan toan prim
        min_spanning_tree = nx.minimum_spanning_tree(G, algorithm='prim')

        # Tạo cửa sổ mới để hiển thị biểu đồ
        graph_window = tk.Toplevel(root)
        graph_window.title("Graph and Minimum Spanning Tree")

        # Tạo đồ thị và cây khung trên Canvas
        figure, ax = plt.subplots(figsize=(5, 5))
        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        # Vẽ đồ thị và cây khung
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        ax.set_title("Graph and Minimum Spanning Tree")
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black', ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
        nx.draw(min_spanning_tree, pos, edge_color='red', with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black', ax=ax)

        # Đánh dấu đỉnh xuất phát
        nx.draw_networkx_nodes(G, pos, nodelist=[start_vertex], node_size=700, node_color='red', ax=ax)

        canvas.draw()

    except ValueError as e:
        tk.messagebox.showerror("Error", str(e))

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Minimum Spanning Tree Visualization")
root.geometry('500x300')

# Tạo các thành phần giao diện người dùng

#Tao label hien thi chu nhau dinh cua do thi
label_vertices = tk.Label(root, text="Number of Vertices:", font = ('Verdena', 14))
label_vertices.place(x = 20, y = 30)

#tao mot entry de nhap dinh cua do thi
entry_vertices = tk.Entry(root)


#tao lable nhac nhap trong so
label_matrix = tk.Label(root, text="Adjacency Matrix:")


#tao crolledtext de nhap cac trong so
scrolledtext_matrix = scrolledtext.ScrolledText(root, width=30, height=10)


#tao button de bat dau tao graph
button_create_graph = tk.Button(root, text="Create Minimum Spanning Tree", command=create_graph)


root.mainloop()