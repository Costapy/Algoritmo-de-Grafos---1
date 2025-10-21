import time
import csv
import os
import random
import heapq
from grafo import Graph


# -------------------------
# Algoritmos
# -------------------------

# Kruskal - Versão otimizada com Union-Find

def criar_grafo_aleatorio(num_vertices, tipo):
    G = Graph(directed=False)
    vertices = [G.insert_vertex(str(i)) for i in range(num_vertices)]
    arestas_existentes = set()

    # Número máximo possível de arestas (grafo completo)
    max_arestas = num_vertices * (num_vertices - 1) // 2

    if tipo == "denso":
        num_arestas = int(max_arestas * 0.98)
    else:  # esparso
        num_arestas = num_vertices * 2  # bem menor

    while len(arestas_existentes) < num_arestas:
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v and (u, v) not in arestas_existentes and (v, u) not in arestas_existentes:
            peso = random.randint(1, 100)
            G.insert_edge(u, v, peso)
            arestas_existentes.add((u, v))

    print(f"Grafo {tipo.upper()} criado: {G.vertex_count()} vértices e {G.edge_count()} arestas.")
    return G


# ======================================================
# === ALGORITMO DE KRUSKAL (COM UNION-FIND OTIMIZADO)
# ======================================================
def kruskal(graf):
    arestas = sorted(graf.edges(), key=lambda e: e.element())
    mst = []

    # Estrutura Union-Find
    parent = {}
    rank = {}

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(u, v):
        raiz_u = find(u)
        raiz_v = find(v)
        if raiz_u == raiz_v:
            return False
        if rank[raiz_u] < rank[raiz_v]:
            parent[raiz_u] = raiz_v
        elif rank[raiz_u] > rank[raiz_v]:
            parent[raiz_v] = raiz_u
        else:
            parent[raiz_v] = raiz_u
            rank[raiz_u] += 1
        return True

    # Inicializa o Union-Find
    for v in graf.vertices():
        parent[v] = v
        rank[v] = 0

    for e in arestas:
        u, v = e.endpoints()
        if union(u, v):
            mst.append(e)
        if len(mst) == graf.vertex_count() - 1:
            break

    return mst


# Prim - Versão com heapq e contador para evitar problemas de comparação
def prim(graf):
    start = next(iter(graf.vertices()))
    mst = []
    visitados = {start}
    pq = []

    for e in graf.incident_edges(start):
        u, v = e.endpoints()
        outro = v if u == start else u
        heapq.heappush(pq, (e.element(), id(start), id(outro), e))

    while pq and len(visitados) < graf.vertex_count():
        peso, _, _, e = heapq.heappop(pq)
        while pq and (pq[0][3].endpoints()[0] in visitados and pq[0][3].endpoints()[1] in visitados):
            heapq.heappop(pq)

        u, v = e.endpoints()
        if u in visitados and v in visitados:
            continue
        novo = v if u in visitados else u
        mst.append(e)
        visitados.add(novo)

        for f in graf.incident_edges(novo):
            x, y = f.endpoints()
            outro = y if x == novo else x
            if outro not in visitados:
                heapq.heappush(pq, (f.element(), random.random(), id(outro), f))


    return mst


# -------------------------
# Experimento
# -------------------------
def medir_desempenho(num_vertices):
    resultados = []
    tipos = ["esparso", "denso"]

    for tipo in tipos:
        G = criar_grafo_aleatorio(num_vertices, tipo)

        # Kruskal
        inicio = time.time()
        kruskal(G)
        tempo_kruskal = time.time() - inicio

        # Prim
        inicio = time.time()
        prim(G)
        tempo_prim = time.time() - inicio

        resultados.append((num_vertices, tipo, tempo_kruskal, tempo_prim))

    return resultados



if __name__ == "__main__":
    tamanhos = [10, 30, 50, 80, 100, 500]
    resultados_finais = []

    for n in tamanhos:
        resultados_finais.extend(medir_desempenho(n))

    # Caminho do arquivo (mesmo diretório dos scripts)
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "resultados.csv")

    # Salva resultados
    with open(caminho_arquivo, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Vertices", "Tipo", "Tempo_Kruskal", "Tempo_Prim"])
        writer.writerows(resultados_finais)

    print(f"\nResultados salvos em: {caminho_arquivo}")
    print("Execução concluída ✅")
