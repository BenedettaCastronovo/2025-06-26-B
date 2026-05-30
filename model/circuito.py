from dataclasses import dataclass, field


@dataclass
class Circuito:
    circuitId: int
    circuitRef: str
    name: str
    location: str
    country: str
    lat: float
    lng: float
    alt: int
    url: str
    #LA CREO COME LISTA VUOTA COSI MI PASSA AL **ROW
    piaz: dict = field(default_factory=dict)
#PIU DIFFICILE PERCHE DEVO PASSARE ANCHE ANNI


    #def __post_init__(self):
     #   self.piazzamenti = get_piazzamenti(
      #      self.circuitId,
       #     self.anno_min,
        #    self.anno_max
        #)
    #def __post_init__(self):
        #self.piazzamenti = {}
        #self.diz['circuitId'] = self.circuitId

    def __eq__(self, other):
        return self.circuitId == other.circuitId

    def __hash__(self):
        return hash(self.circuitId)

    def __str__(self):
        return f"Circuit {self.circuitId}"