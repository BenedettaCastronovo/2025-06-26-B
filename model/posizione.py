from dataclasses import dataclass
from datetime import datetime


@dataclass
class Posizione:

    driverId: int
    time: datetime

