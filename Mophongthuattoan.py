import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tkinter import ttk

def dijkstra():
    try:
        num_vertices = int(entry_vertices.get()) # số đỉnh của đồ thị
        matrix_values = scrolledtext_matrix.get("1.0", tk.END).strip().split('\n') # giá trị của ma trận kề
        #strip() ham xoa khoang trang
        #split('\n') ham chia chuoi thanh nhieu dong tai noi \n

        # tách ma trận ra
        adjacency_matrix = []
        for row in matrix_values:
            values = list(map(int, row.split()))
            adjacency_matrix.append(values)

        # nếu người nhâp để trống thì xuất ra màn hình
        if len(adjacency_matrix) != num_vertices or any(len(row) != num_vertices for row in adjacency_matrix):
            raise ValueError("Đầu vào không hợp lệ. Hãy đảm bảo ma trận là hình vuông và có số đỉnh chính xác.")

        # tạo đồ thị G từ adjacency_matrix
        G = nx.from_numpy_array(np.array(adjacency_matrix))
        '''
        0 4 3 0 0 0 0 0
        4 0 2 5 0 0 0 0
        3 2 0 3 6 0 0 0
        0 5 3 0 1 5 0 0
        0 0 6 1 0 0 5 0 
        0 0 0 5 0 0 2 7 
        0 0 0 0 5 2 0 4
        0 0 0 0 0 7 4 0
        '''

        '''
        0 0 0 0 0 0
        7 0 0 2 0 0
        0 4 0 0 0 2
        8 0 0 0 0 6
        0 2 0 2 0 0
        0 1 0 0 3 0
        '''
        # Nhập đỉnh bắt đầu và đỉnh kết thúc
        source_node = simpledialog.askinteger("Đỉnh bắt đầu", "Nhập đỉnh bắt đầu (0 đến {}):".format(num_vertices - 1), minvalue=0, maxvalue=num_vertices - 1)
        target_node = simpledialog.askinteger("Đỉnh kết thúc", "Nhập đỉnh kết thúc (0 đến {}):".format(num_vertices - 1), minvalue=0, maxvalue=num_vertices - 1)

        if source_node and target_node is None:
            return  # Nếu người dùng nhấn Cancel

        # tìm đường đi từ đỉnh bắt đầu đến đỉnh kết thúc bằng thuật toán dijkstra
        shortest_path = nx.dijkstra_path(G, source_node, target_node)
        shortest_path_length = nx.dijkstra_path_length(G, source_node, target_node)

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

def prim():
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
        root.withdraw()
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

button_do = tk.Button(root, text="Thực hiện", font = ('verdena',12), command= perform_algorithm)
button_do.place(x = 300, y = 250)
    

root.mainloop()