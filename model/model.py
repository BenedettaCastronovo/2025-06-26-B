import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._circ = DAO.getAllCircuits()
        self._grafo = nx.Graph()
        self.mappaC = {}
        self._best = {}
        self.somma = 0
        self.listao = []
        self.mas = []

    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, min, max):
        self._grafo.clear()
        for c in self._circ:
            c.piaz = DAO.getPiaz(c, min, max)
            self.mappaC[c.circuitId] = c
        self._grafo.add_nodes_from(self._circ)
        self._archi = DAO.getArchi(self.mappaC, min, max)
        for a in self._archi:
            self._grafo.add_edge(a.c1, a.c2, weight=a.peso)

    def getArchi(self):
        return len(self._grafo.edges)

    def getN(self):
        return len(self._grafo.nodes)

    def stampaDettagli(self):
            #listapesoM = list(sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True))[:3]
            compC = list(nx.connected_components(self._grafo))  # RICORDA
            self.mas = max(compC, key=len)
            subgraph = self._grafo.subgraph(self.mas).copy()
            lista = []
            for n in subgraph.nodes():
                edges = list(subgraph.edges(n, data=True))
                if len(edges) == 0:
                    continue  # nodo isolato, salta
                minino = min(edges, key=lambda x: x[2]['weight'])
                lista.append((n, minino[2]["weight"]))
            self.listao = sorted(lista, key=lambda x: x[1], reverse=True)
            return self.mas, self.listao


    def cerca(self, k, m):
        self._best = {}
        self.somma = 0
        #comp = self.listao meglio con mas perche senno lista di tupla piu difficult
        comp = self.mas #cosi ho solo i nodi
        for n in list(comp)[:5]:  # stampa i primi 5 nodi
            print(f"{n.name} - edizioni: {len(n.piaz)}")
        nodi_validi = [n for n in comp if self.is_valid(n, comp, m)]
        print(f"nodi validi: {len(nodi_validi)}")
        self.ric([], nodi_validi, k, m)
        return self._best, self.somma

    def ric(self, parziale, comp, k, m):
        if len(parziale) == k:
            print(f"trovato parziale pieno!")
            if self.sommaimp(parziale) > self.somma:
                self.somma = self.sommaimp(parziale)
                self._best = copy.deepcopy(parziale)
            return

        #for n in self._grafo.neighbors(parziale[-1]):
        for n in comp:
            if n not in parziale and self.is_valid(n, comp, m):
                parziale.append(n)
                self.ric(parziale, comp, k, m)
                parziale.pop()

    def sommaimp(self, parziale):
        i = 0
        somma = 0
        for c in parziale:
            np = 0
            npTot = 0
            for t in c.piaz.values():
                for p in t:  # p è la singola Posizione
                    npTot += 1
                    if p.time is not None:
                        np += 1
            if npTot > 0:
                i = 1 - np/npTot
            else:
                i = 0
            somma += i
        return somma

    def is_valid(self, n, comp, m):
        if n in comp and len(n.piaz) >= m:
            return True

        return False











