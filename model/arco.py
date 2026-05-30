from dataclasses import dataclass

from model.circuito import Circuito


@dataclass
class Arco:
    c1: Circuito
    c2: Circuito
    peso: int