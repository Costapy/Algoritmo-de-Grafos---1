from grafo import Graph

def criar_grafo(vertices_nomes, arestas_dados):
    g = Graph(directed=False)
    mapeamento_vertices = {}

    for nome in vertices_nomes:
        vertice_obj = g.insert_vertex(nome)
        mapeamento_vertices[nome] = vertice_obj

    for u_nome, v_nome, peso in arestas_dados:
        u = mapeamento_vertices[u_nome]
        v = mapeamento_vertices[v_nome]
        g.insert_edge(u, v, peso)

    return g

if __name__ == "__main__":
    lista_vertices = ["A", "B", "C", "D", "E", "F", "G"]
    
    lista_arestas = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11)
    ]

    G = criar_grafo(lista_vertices, lista_arestas)

    print(f"Número de vértices: {G.vertex_count()}")
    print(f"Número de arestas: {G.edge_count()}")
    
    print("\nArestas e seus pesos:")
    for aresta in G.edges():
        origem, destino = aresta.endpoints()
        print(f"  - Aresta ({origem.element()}, {destino.element()}) com peso {aresta.element()}")