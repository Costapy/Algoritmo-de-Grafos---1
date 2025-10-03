import matplotlib.pyplot as plt
import networkx as nx
import os

def desenhar_grafo_mst(grafo, mst, usar_prim=True, titulo="Grafo com MST", salvar=False):
    """
    Desenha o grafo original e a árvore geradora mínima (MST).

    Parâmetros:
    - grafo: objeto Graph (do seu grafo.py)
    - mst: lista de arestas retornadas por Prim ou Kruskal
    - usar_prim: True se o mst veio do Prim (formato diferente do Kruskal)
    - titulo: título do gráfico
    - salvar: se True, salva em arquivo PNG ao invés de mostrar
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
        for u, v, peso in mst:
            T.add_edge(u.element(), v.element(), weight=peso)
    else:
        for e in mst:
            u, v = e.endpoints()
            T.add_edge(u.element(), v.element(), weight=e.element())

    # Layout
    pos = nx.spring_layout(G, seed=42)

    n = G.number_of_nodes()
    plt.figure(figsize=(10, 7))

    # Desenha grafo completo
    nx.draw(G, pos,
            with_labels=(n <= 30),          # mostra labels só se pequeno
            node_color="lightblue",
            node_size=200 if n >= 50 else 800,
            font_size=8 if n > 30 else 10,
            edge_color="gray", width=1)

    # Desenha rótulos das arestas só se for pequeno
    if n <= 30:
        nx.draw_networkx_edge_labels(G, pos,
                                     edge_labels=nx.get_edge_attributes(G, "weight"),
                                     font_size=8)

    # Destaca MST em vermelho
    nx.draw_networkx_edges(T, pos, edge_color="red", width=2.5)

    plt.title(titulo)

    if salvar or n > 100:
        pasta = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(pasta, f"grafo_{n}_vertices.png")
        plt.savefig(caminho, dpi=150)
        print(f"✅ Grafo salvo em: {caminho}")
        plt.close()
    else:
        plt.show()
