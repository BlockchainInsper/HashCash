import datetime


class Email():
    def __init__(self, timestamp: datetime, mesage: str, target: int):
        self.Timestamp = datetime
        self.Mesage = mesage
        self.Target = target
        self.Hash = None
        self.Nounce = None