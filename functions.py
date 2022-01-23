# Returns the list without the elements from the pile
def listMinus(self, list, pile):
    copie = []
    while not pile.empty():
        x = pile.depile()
        copie.append(x)
        list = [e for e in list if e != x]
    pile.empileStack(copie)
    return list