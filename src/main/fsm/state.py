from enum import Enum

class State(Enum):
    CONNECTING = 1
    SETUP = 2
    TRAINING = 3
    WAITING_FOR_PEERS = 4
    SECURE_AVERAGE_COMPUTATION = 5
    SAVING_MODEL = 6
    SHUTDOWN = 7

