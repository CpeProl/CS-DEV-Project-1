class Pile():
    def __init__(self):
        self.pile = []
    
    # Returns True if the stack is empty
    def empty(self):
        return self.pile == []

    # Adds an element to the stack
    def empile(self, x):
        self.pile.append(x)
    
    # Deletes an element from the stack, and returns it
    def depile(self):
        x = self.pile.pop()
        return x
    
    # Adds a whole list of elements to the stack
    def empileStack(self, l):
        for e in l:
            x = l.pop()
            self.empile(x)
    
    # Checks if an element is inside the stack
    def isInside(self, x):
        copie = []
        while not self.empty():
            y = self.depile()
            copie.append(y)
            if x == y:
                self.empileStack(copie)
                return True
        self.empileStack(copie)
        return False

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