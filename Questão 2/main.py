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

def kruskal(graf):
    arestas = sorted(graf.edges(), key=lambda e: e.element())
    mst = []
    
    adj = {v: [] for v in graf.vertices()} 
    def cria_ciclo(u, v):
        visitado = set()

        def dfs(atual, destino):
            if atual == destino:
                return True
            visitado.add(atual)
            for vizinho in adj[atual]:
                if vizinho not in visitado:
                    if dfs(vizinho, destino):
                        return True
            return False

        return dfs(u, v)

    for e in arestas:
        u, v = e.endpoints()
        if not cria_ciclo(u, v):
            mst.append(e)
            adj[u].append(v)
            adj[v].append(u)

        if len(mst) == graf.vertex_count() - 1:
            break

    return mst


if __name__ == "__main__":
    lista_vertices = ["1", "2", "3", "4", "5", "6"]
    
    lista_arestas = [
        ("1", "2", 33),
        ("1", "3", 17),
        ("2", "3", 18),
        ("2", "4", 20),
        ("3", "4", 16),
        ("3", "5", 4),
        ("4", "5", 9),
        ("4", "6", 8),
        ("5", "6", 14)
    ]

    G = criar_grafo(lista_vertices, lista_arestas)

    print(f"Número de vértices: {G.vertex_count()}")
    print(f"Número de arestas: {G.edge_count()}")
    
    print("\nArestas e seus pesos:")
    for aresta in G.edges():
        origem, destino = aresta.endpoints()
        print(f"  - Aresta ({origem.element()}, {destino.element()}) com peso {aresta.element()}")
    
    mst = kruskal(G)

    print("\nÁrvore Geradora Mínima (Kruskal):")
    for aresta in mst:
        u, v = aresta.endpoints()
        print(f"  - ({u.element()}, {v.element()}) com peso {aresta.element()}")
