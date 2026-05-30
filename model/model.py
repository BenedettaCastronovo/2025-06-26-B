import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._circ = DAO.getAllCircuits()
        self._grafo = nx.Graph()
        self.mappaC = {}

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
            mas = max(compC, key=len)
            subgraph = self._grafo.subgraph(mas).copy()
            lista = []
            for n in subgraph.nodes():
                edges = list(subgraph.edges(n, data=True))
                if len(edges) == 0:
                    continue  # nodo isolato, salta
                minino = min(edges, key=lambda x: x[2]['weight'])
                lista.append((n, minino[2]["weight"]))
            listao = sorted(lista, key=lambda x: x[1], reverse=True)
            return mas, listao





