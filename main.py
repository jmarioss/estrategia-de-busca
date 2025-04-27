from collections import deque
import heapq
import math
import tkinter as tk
from tkinter import ttk

grafo_aereo = {
    "Aracaju": {"Maceió": 201, "Salvador": 277, "Recife": 398, "Fortaleza": 815, "Belém": 1641},
    "Belém": {"São Luís": 481, "Teresina": 750, "Fortaleza": 1133, "Macapá": 329, "Manaus": 1292},
    "Boa Vista": {"Manaus": 785, "Belém": 1292},
    "Brasília": {"Belém": 1592, "Fortaleza": 1687, "Salvador": 1060, "São Paulo": 873, "Goiânia": 209, "Campo Grande": 878},
    "Campo Grande": {"Brasília": 878, "Cuiabá": 694, "São Paulo": 894, "Manaus": 2013},
    "Cuiabá": {"Campo Grande": 694, "Goiânia": 934, "Manaus": 2337},
    "Curitiba": {"São Paulo": 338, "Florianópolis": 300, "Porto Alegre": 711, "Brasília": 1356, "Campo Grande": 991},
    "Florianópolis": {"Curitiba": 300, "Porto Alegre": 476},
    "Fortaleza": {"Teresina": 495, "Natal": 435, "Recife": 682, "Belém": 1133},
    "Goiânia": {"Brasília": 209, "Cuiabá": 934},
    "João Pessoa": {"Recife": 109, "Natal": 151},
    "Macapá": {"Belém": 329, "Manaus": 1054},
    "Maceió": {"Aracaju": 201, "Recife": 202, "Salvador": 475},
    "Manaus": {"Belém": 1292, "Boa Vista": 785, "Porto Velho": 901, "Macapá": 1054, "Brasília": 1932, "Campo Grande": 2013},
    "Natal": {"Fortaleza": 435, "Recife": 253, "João Pessoa": 151},
    "Palmas": {"Brasília": 923, "Belém": 1283},
    "Porto Alegre": {"Curitiba": 711, "Florianópolis": 476},
    "Porto Velho": {"Manaus": 901, "Rio Branco": 544},
    "Recife": {"Maceió": 202, "João Pessoa": 109, "Natal": 253, "Fortaleza": 682},
    "Rio Branco": {"Porto Velho": 544},
    "Rio de Janeiro": {"São Paulo": 357, "Belo Horizonte": 434, "Vitória": 521},
    "Salvador": {"Aracaju": 277, "Recife": 675, "Belo Horizonte": 964, "Fortaleza": 1023},
    "São Luís": {"Belém": 481, "Teresina": 329},
    "São Paulo": {"Rio de Janeiro": 357, "Belo Horizonte": 489, "Brasília": 873, "Curitiba": 338, "Campo Grande": 894},
    "Teresina": {"São Luís": 329, "Fortaleza": 495},
    "Vitória": {"Belo Horizonte": 324, "Rio de Janeiro": 521}
}

grafo_terrestre = {
    "Manaus": {"Porto Velho": 901, "Boa Vista": 785},
    "Porto Velho": {"Manaus": 901, "Rio Branco": 544, "Cuiabá": 1458},
    "Rio Branco": {"Porto Velho": 544},
    "Boa Vista": {"Manaus": 785},
    "Belém": {"São Luís": 800, "Macapá": 300, "Teresina": 917},
    "Macapá": {"Belém": 300},
    "Palmas": {"Brasília": 923, "Belém": 1283},
    
    "São Luís": {"Belém": 800, "Teresina": 440},
    "Teresina": {"São Luís": 440, "Fortaleza": 630, "Belém": 917},
    "Fortaleza": {"Teresina": 630, "Natal": 530, "Recife": 800},
    "Natal": {"Fortaleza": 530, "João Pessoa": 180},
    "João Pessoa": {"Natal": 180, "Recife": 120},
    "Recife": {"João Pessoa": 120, "Maceió": 260, "Fortaleza": 800},
    "Maceió": {"Recife": 260, "Aracaju": 270, "Salvador": 632},
    "Aracaju": {"Maceió": 270, "Salvador": 350},
    "Salvador": {"Aracaju": 350, "Brasília": 1446},
    
    "Brasília": {"Goiânia": 209, "Palmas": 923, "Campo Grande": 1134, "Salvador": 1446},
    "Goiânia": {"Brasília": 209, "Cuiabá": 934},
    "Cuiabá": {"Goiânia": 934, "Campo Grande": 694, "Porto Velho": 1458},
    "Campo Grande": {"Cuiabá": 694, "Brasília": 1134, "São Paulo": 1014},
    
    "São Paulo": {"Campo Grande": 1014, "Rio de Janeiro": 357, "Belo Horizonte": 489, "Curitiba": 408},
    "Rio de Janeiro": {"São Paulo": 357, "Belo Horizonte": 434, "Vitória": 521},
    "Belo Horizonte": {"Rio de Janeiro": 434, "São Paulo": 489, "Vitória": 324, "Brasília": 746},
    "Vitória": {"Belo Horizonte": 324, "Rio de Janeiro": 521},
    
    "Curitiba": {"São Paulo": 408, "Florianópolis": 300, "Porto Alegre": 711},
    "Florianópolis": {"Curitiba": 300, "Porto Alegre": 476},
    "Porto Alegre": {"Florianópolis": 476, "Curitiba": 711}
}

heuristica = {
    "Aracaju": 1600, "Belém": 0, "Boa Vista": 2200, "Brasília": 1200,
    "Campo Grande": 1800, "Cuiabá": 1700, "Curitiba": 2500, "Florianópolis": 2600,
    "Fortaleza": 1200, "Goiânia": 1300, "João Pessoa": 1450, "Macapá": 200,
    "Maceió": 1700, "Manaus": 1500, "Natal": 1350, "Palmas": 1000,
    "Porto Alegre": 2800, "Porto Velho": 1900, "Recife": 1500, "Rio Branco": 2100,
    "Rio de Janeiro": 2300, "Salvador": 1400, "São Luís": 500, "São Paulo": 2400,
    "Teresina": 800, "Vitória": 2200
}


def busca_largura(grafo, inicio, objetivo):
    fila = deque([[inicio]])
    visitados = set()
    
    while fila:
        caminho = fila.popleft()
        no = caminho[-1]
        
        if no == objetivo:
            return caminho
        
        if no not in visitados:
            visitados.add(no)
            for vizinho in grafo.get(no, {}):
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)
    return []

def busca_profundidade(grafo, inicio, objetivo):
    pilha = [[inicio]]
    visitados = set()
    
    while pilha:
        caminho = pilha.pop()
        no = caminho[-1]
        
        if no == objetivo:
            return caminho
        
        if no not in visitados:
            visitados.add(no)
            for vizinho in reversed(list(grafo.get(no, {}))):
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                pilha.append(novo_caminho)
    return []

def busca_custo_uniforme(grafo, inicio, objetivo):
    fila = [(0, [inicio])]
    visitados = set()
    
    while fila:
        custo, caminho = heapq.heappop(fila)
        no = caminho[-1]
        
        if no == objetivo:
            return caminho, custo
        
        if no not in visitados:
            visitados.add(no)
            for vizinho, distancia in grafo.get(no, {}).items():
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                heapq.heappush(fila, (custo + distancia, novo_caminho))
    return [], 0

def busca_gulosa(grafo, inicio, objetivo, heuristica):
    fila = [(heuristica[inicio], [inicio])]
    visitados = set()
    
    while fila:
        _, caminho = heapq.heappop(fila)
        no = caminho[-1]
        
        if no == objetivo:
            distancia = calcular_distancia(grafo, caminho)
            return caminho, distancia
        
        if no not in visitados:
            visitados.add(no)
            for vizinho in grafo.get(no, {}):
                if vizinho in heuristica:  
                    novo_caminho = list(caminho)
                    novo_caminho.append(vizinho)
                    heapq.heappush(fila, (heuristica[vizinho], novo_caminho))
    return [], 0

def busca_a_estrela(grafo, inicio, objetivo, heuristica):
    fila = [(0 + heuristica[inicio], 0, [inicio])]
    visitados = set()
    
    while fila:
        _, custo, caminho = heapq.heappop(fila)
        no = caminho[-1]
        
        if no == objetivo:
            return caminho, custo
        
        if no not in visitados:
            visitados.add(no)
            for vizinho, distancia in grafo.get(no, {}).items():
                if vizinho in heuristica:
                    novo_caminho = list(caminho)
                    novo_caminho.append(vizinho)
                    heapq.heappush(fila, (custo + distancia + heuristica[vizinho], custo + distancia, novo_caminho))
    return [], 0

def calcular_distancia(grafo, caminho):
    if not caminho or len(caminho) < 2:
        return 0
    try:
        distancia = 0
        for i in range(len(caminho)-1):
            distancia += grafo[caminho[i]][caminho[i+1]]
        return distancia
    except KeyError:
        return 0

def comparar_rotas(origem, destino):
    if origem not in grafo_aereo or destino not in grafo_aereo:
        print(f"Erro: {origem} ou {destino} não são capitais válidas!")
        return

    print(f"\n--- Comparação de Rotas: {origem} → {destino} ---")
    
    print("\n[ROTA AÉREA]")
    bfs_aereo = busca_largura(grafo_aereo, origem, destino)
    dfs_aereo = busca_profundidade(grafo_aereo, origem, destino)
    ucs_aereo, dist_ucs_aereo = busca_custo_uniforme(grafo_aereo, origem, destino)
    gulosa_aereo, dist_gulosa_aereo = busca_gulosa(grafo_aereo, origem, destino, heuristica)
    a_estrela_aereo, dist_a_estrela_aereo = busca_a_estrela(grafo_aereo, origem, destino, heuristica)
    
    print(f"BFS: {' → '.join(bfs_aereo)} (Distância: {calcular_distancia(grafo_aereo, bfs_aereo)} km)")
    print(f"DFS: {' → '.join(dfs_aereo)} (Distância: {calcular_distancia(grafo_aereo, dfs_aereo)} km)")
    print(f"UCS: {' → '.join(ucs_aereo)} (Distância: {dist_ucs_aereo} km)")
    print(f"Gulosa: {' → '.join(gulosa_aereo)} (Distância: {dist_gulosa_aereo} km)")
    print(f"A*: {' → '.join(a_estrela_aereo)} (Distância: {dist_a_estrela_aereo} km)")
    
    print("\n[ROTA TERRESTRE]")
    bfs_terr = busca_largura(grafo_terrestre, origem, destino)
    dfs_terr = busca_profundidade(grafo_terrestre, origem, destino)
    ucs_terr, dist_ucs_terr = busca_custo_uniforme(grafo_terrestre, origem, destino)
    gulosa_terr, dist_gulosa_terr = busca_gulosa(grafo_terrestre, origem, destino, heuristica)
    a_estrela_terr, dist_a_estrela_terr = busca_a_estrela(grafo_terrestre, origem, destino, heuristica)
    
    print(f"BFS: {' → '.join(bfs_terr)} (Distância: {calcular_distancia(grafo_terrestre, bfs_terr)} km)")
    print(f"DFS: {' → '.join(dfs_terr)} (Distância: {calcular_distancia(grafo_terrestre, dfs_terr)} km)")
    print(f"UCS: {' → '.join(ucs_terr)} (Distância: {dist_ucs_terr} km)")
    print(f"Gulosa: {' → '.join(gulosa_terr)} (Distância: {dist_gulosa_terr} km)")
    print(f"A*: {' → '.join(a_estrela_terr)} (Distância: {dist_a_estrela_terr} km)")
    
    try:
        distancias_aereas = [d for d in [dist_ucs_aereo, dist_gulosa_aereo, dist_a_estrela_aereo,
                                        calcular_distancia(grafo_aereo, bfs_aereo),
                                        calcular_distancia(grafo_aereo, dfs_aereo)] if d > 0]
        menor_aereo = min(distancias_aereas) if distancias_aereas else math.inf
        
        distancias_terrestres = [d for d in [dist_ucs_terr, dist_gulosa_terr, dist_a_estrela_terr,
                                            calcular_distancia(grafo_terrestre, bfs_terr),
                                            calcular_distancia(grafo_terrestre, dfs_terr)] if d > 0]
        menor_terr = min(distancias_terrestres) if distancias_terrestres else math.inf
        
        print(f"\n[CONCLUSÃO]")
        print(f"Menor distância aérea: {menor_aereo if menor_aereo != math.inf else 'N/A'} km")
        print(f"Menor distância terrestre: {menor_terr if menor_terr != math.inf else 'N/A'} km")
        
        if menor_aereo < menor_terr:
            print("✅ O trajeto AÉREO é mais curto!")
        elif menor_terr < menor_aereo:
            print("✅ O trajeto TERRESTRE é mais curto!")
        else:
            print("⚠️ As rotas têm distâncias equivalentes ou não foram encontradas")
    except:
        print("Erro ao comparar rotas")

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Rotas entre Capitais")
        
        self.capitais = sorted(list(grafo_aereo.keys()))
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid()
        
        ttk.Label(self.frame, text="Origem:").grid(column=0, row=0, sticky=tk.W)
        self.origem_var = tk.StringVar()
        self.origem_cb = ttk.Combobox(self.frame, textvariable=self.origem_var, values=self.capitais)
        self.origem_cb.grid(column=1, row=0, padx=5, pady=5)
        self.origem_cb.current(0)
        
        ttk.Label(self.frame, text="Destino:").grid(column=0, row=1, sticky=tk.W)
        self.destino_var = tk.StringVar()
        self.destino_cb = ttk.Combobox(self.frame, textvariable=self.destino_var, values=self.capitais)
        self.destino_cb.grid(column=1, row=1, padx=5, pady=5)
        self.destino_cb.current(1)
        
        self.btn_comparar = ttk.Button(self.frame, text="Comparar Rotas", command=self.executar_comparacao)
        self.btn_comparar.grid(column=0, row=2, columnspan=2, pady=10)
        
        self.resultados = tk.Text(self.frame, height=20, width=80, state=tk.DISABLED)
        self.resultados.grid(column=0, row=3, columnspan=2)
        
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.resultados.yview)
        scrollbar.grid(column=2, row=3, sticky=tk.NS)
        self.resultados['yscrollcommand'] = scrollbar.set
    
    def executar_comparacao(self):
        origem = self.origem_var.get()
        destino = self.destino_var.get()
        
        self.resultados.config(state=tk.NORMAL)
        self.resultados.delete(1.0, tk.END)
        
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        comparar_rotas(origem, destino)
        
        sys.stdout = old_stdout
        self.resultados.insert(tk.END, mystdout.getvalue())
        self.resultados.config(state=tk.DISABLED)
        self.resultados.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()