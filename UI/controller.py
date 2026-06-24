import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._k = None
        self._m = None
        self.min = None
        self.max = None

    def handleBuildGraph(self, e):
        if self._view._ddYear1.value > self._view._ddYear2.value or self._view._ddYear1.value is None or self._view._ddYear2.value is None:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text("seleziona giisto"))
            self._view.update_page()
            return
        self.min = self._view._ddYear1.value
        self.max = self._view._ddYear2.value
        self._model.creaGrafo(self.min, self.max)
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text("grafo giusto"))
        self._view.update_page()

    def handlePrintDetails(self, e):
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text("dettagli"))
        self._view._txtGraphDetails.controls.append(ft.Text(f"archi: {self._model.getArchi()} e nodi {self._model.getN()}"))
        mas, listao = self._model.stampaDettagli()
        #self._view._txtGraphDetails.controls.append(ft.Text(f"comp Max: {mas}"))
        for l in listao:
            self._view._txtGraphDetails.controls.append(ft.Text(f"NODOOOOOOOOOO {l[0].name} - {l[1]}"))
        self._view.update_page()


    def handleCercaDreamChampionship(self, e):
        self._k = self._view._txtInSoglia.value
        self._m = self._view._txtInNumDiEdizioni.value
        if self._k == None or self._m == None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("seleziona"))
            self._view.update_page()
            return
        try:
            self._k = int(self._k)
            self._m = int(self._m)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("seleziona numeri valid"))
            self._view.update_page()
            return
        self._view._txt_result.controls.clear()
        path, bestI = self._model.cerca(self._k, self._m)
        self._view._txt_result.controls.clear()
        for n in path:
            self._view._txt_result.controls.append(ft.Text(f"id: {n.circuitId} - nome: {n.name}"))
        self._view._txt_result.controls.append(ft.Text(f"imprevisti: {bestI}"))
        self._view.update_page()

    def fillDD(self):
        years = self._model.getAllYears()
        for y in years:
            self._view._ddYear1.options.append(ft.dropdown.Option(y))
            self._view._ddYear2.options.append(ft.dropdown.Option(y))
        self._view.update_page()