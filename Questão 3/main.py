import os
import heapq
import itertools
import random
import time
import csv
from grafo import Graph


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
# Experimento
# -------------------------

def medir_tempo(func, *args):
    inicio = time.perf_counter()
    func(*args)
    fim = time.perf_counter()
    return fim - inicio


if __name__ == "__main__":
    tamanhos = [10, 50, 100, 500]
    resultados = []

    for n in tamanhos:
        # Grafo Denso (completo)
        m_denso = n * (n - 1) // 2
        G_denso = criar_grafo(n, m_denso, denso=True)

        # Grafo Esparso
        m_esparso = (n - 1) * 4
        G_esparso = criar_grafo(n, m_esparso, denso=False)

        # Testes de desempenho
        for tipo, G in [("Denso", G_denso), ("Esparso", G_esparso)]:
            print(f"\n==== Grafo {tipo} com {n} vértices ====")

            tempo_kruskal = medir_tempo(kruskal, G)
            tempo_prim = medir_tempo(prim, G)

            print(f"Kruskal: {tempo_kruskal:.6f} segundos")
            print(f"Prim:    {tempo_prim:.6f} segundos")

            resultados.append([n, tipo, tempo_kruskal, tempo_prim])

    # Salvar no diretório atual
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(pasta_atual, "resultados.csv")

    with open(caminho_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Vertices", "Tipo", "Tempo_Kruskal", "Tempo_Prim"])
        writer.writerows(resultados)

    print(f"\nResultados salvos em: {caminho_csv}")
