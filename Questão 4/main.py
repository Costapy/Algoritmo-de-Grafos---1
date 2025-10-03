import heapq
import itertools
import random
from grafo import Graph
from desenho import desenhar_grafo_mst

# -------------------------
# Algoritmos
# -------------------------

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


def prim(graf):
    start = next(iter(graf.vertices())) 
    mst = [] 
    visitados = {start}

    pq = []
    contador = itertools.count()  # gera índices únicos para desempatar

    for e in graf.incident_edges(start):
        u, v = e.endpoints()
        outro = v if u == start else u
        heapq.heappush(pq, (e.element(), next(contador), start, outro, e))

    while pq and len(visitados) < graf.vertex_count():
        peso, _, u, v, e = heapq.heappop(pq)
        if v in visitados:
            continue

        mst.append((u, v, peso))
        visitados.add(v)

        for f in graf.incident_edges(v):
            x, y = f.endpoints()
            outro = y if x == v else x
            if outro not in visitados:
                heapq.heappush(pq, (f.element(), next(contador), v, outro, f))

    return mst


# -------------------------
# Função para criar grafos
# -------------------------

def criar_grafo(n, m, denso=True):
    g = Graph(directed=False)
    vertices = [g.insert_vertex(str(i)) for i in range(n)]

    arestas = set()
    while len(arestas) < m:
        u, v = random.sample(vertices, 2)
        if (u, v) not in arestas and (v, u) not in arestas:
            peso = random.randint(1, 100)
            g.insert_edge(u, v, peso)
            arestas.add((u, v))

    return g


# -------------------------
# Programa Principal
# -------------------------

if __name__ == "__main__":
    # Tamanhos diferentes de grafos para testar
    tamanhos = [6, 20, 50, 100]

    for n in tamanhos:
        m = min(n * (n - 1) // 2, n * 4)  # número de arestas controlado
        g = criar_grafo(n, m)

        print(f"\n==== Grafo com {n} vértices e {m} arestas ====")

        # --- Kruskal ---
        mst_kruskal = kruskal(g)
        print("\nMST (Kruskal):")
        for e in mst_kruskal:
            u, v = e.endpoints()
            print(f"{u.element()} -- {v.element()} (peso {e.element()})")
        desenhar_grafo_mst(g, mst_kruskal, usar_prim=False,
                           titulo=f"Grafo {n} vértices (Kruskal)")

        # --- Prim ---
        mst_prim = prim(g)
        print("\nMST (Prim):")
        for u, v, peso in mst_prim:
            print(f"{u.element()} -- {v.element()} (peso {peso})")
        desenhar_grafo_mst(g, mst_prim, usar_prim=True,
                           titulo=f"Grafo {n} vértices (Prim)")
