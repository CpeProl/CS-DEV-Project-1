class Pile():
    def __init__(self):
        self.pile = []
    
    def empty(self):
        return self.file == []

    def empile(self, x):
        self.pile.append(x)
    
    def depile(self):
        x = self.pile.pop()
        return x

class File():
    def __init__(self):
        self.file = []
    
    def empty(self):
        return self.file == []

    def ajoute(self, x):
        self.file.append(x)
    
    def retire(self):
        x = self.file.pop(0)
        return x