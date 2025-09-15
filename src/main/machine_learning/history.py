class History:
    def __init__(self, train_accuracy: list[float], train_loss: list[float], validation_accuracy: list[float], validation_loss: list[float]):
        self.train_accuracy = train_accuracy
        self.train_loss = train_loss
        self.validation_accuracy = validation_accuracy
        self.validation_loss = validation_loss
