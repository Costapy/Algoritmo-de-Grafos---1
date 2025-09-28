import matplotlib.pyplot as plt
import networkx as nx

def desenhar_grafo_mst(grafo, mst, usar_prim=True):
    """
    Desenha o grafo original e a árvore geradora mínima (MST).

    Parâmetros:
    - grafo: objeto Graph (do seu grafo.py)
    - mst: lista de arestas retornadas por Prim ou Kruskal
    - usar_prim: True se o mst veio do Prim (formato diferente do Kruskal)
    """
    # Converter o grafo customizado em um grafo do networkx
    G = nx.Graph()
    for v in grafo.vertices():
        G.add_node(v.element())
    for e in grafo.edges():
        u, v = e.endpoints()
        G.add_edge(u.element(), v.element(), weight=e.element())

    # Converter a MST para networkx
    T = nx.Graph()
    if usar_prim:
        # Prim retorna (u, v, peso)
        for u, v, peso in mst:
            T.add_edge(u.element(), v.element(), weight=peso)
    else:
        # Kruskal retorna arestas (Edge)
        for e in mst:
            u, v = e.endpoints()
            T.add_edge(u.element(), v.element(), weight=e.element())

    pos = nx.spring_layout(G, seed=42)  # Layout fixo para consistência

    plt.figure(figsize=(10, 6))

    # Desenha grafo completo (G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", 
            node_size=800, font_size=10, edge_color="gray", width=1.5)
    nx.draw_networkx_edge_labels(G, pos, 
                                 edge_labels=nx.get_edge_attributes(G, "weight"))

    # Desenha MST em destaque (T)
    nx.draw_networkx_edges(T, pos, edge_color="red", width=2.5)

    plt.title("Grafo Original (azul) e Árvore Geradora Mínima (arestas vermelhas)")
    plt.show()
