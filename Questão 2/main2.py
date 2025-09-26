from grafo import Graph
from random import choice
import heapq

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

#Curti essa implementação não, achei bem complexa, tô pensando em fazer outra (sem falar que não tá funcionando 100%)
def prim(graf):
    start = next(iter(graf.vertices())) 
    mst = [] 
    visitados = {start}

    pq = []
    for e in graf.incident_edges(start):
        u, v = e.endpoints()
        outro = v if u == start else u
        heapq.heappush(pq, (e.element(), start, outro, e))

    while pq and len(visitados) < graf.vertex_count():
        peso, u, v, e = heapq.heappop(pq)
        if v in visitados:
            continue

        mst.append((u, v, peso))
        visitados.add(v)

        print(f"Aresta escolhida: ({u.element()} - {v.element()}) peso {peso}")

        for f in graf.incident_edges(v):
            x, y = f.endpoints()
            outro = y if x == v else x
            if outro not in visitados:
                heapq.heappush(pq, (f.element(), v, outro, f))

    print("\nÁrvore Geradora Mínima encontrada:")
    peso_total = 0
    for u, v, peso in mst:
        print(f"  - ({u.element()}, {v.element()}) peso {peso}")
        peso_total += peso
    print(f"Peso total da MST: {peso_total}")

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

    prim(G)
