from enum import Enum

class State(Enum):
    CONNECTING = "connecting"
    SETUP = "setup"
    TRAINING = "training"
    SECURE_AVERAGE_COMPUTATION = "secure_average_computation"
    SAVING_MODEL = "saving_model"
    SHUTDOWN = "shutdown"

