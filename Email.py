

class Email():
    def __init__(self, datetime, mesage, target):
        self.Timestamp = datetime
        self.Mesage = mesage
        self.Target = target
        self.Hash = None
        self.Nounce = None