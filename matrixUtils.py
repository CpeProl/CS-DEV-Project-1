# Returns True if the column j of the matrix M contains only None values
def isEmptyCol(M, j):
    for i in range(len(M)):
        if M[i][j] != None:
            return False
    return True

# Returns True if the row i of the matrix M contains only None values
def isEmptyRow(M, i):
    for j in range(len(M[0])):
        if M[i][j] != None:
            return False
    return True

# Returns the matrix M without its column number j (starting from 0)
def delCol(M, j):
    rows,cols = len(M), len(M[0])
    N = [[M[i][k] for k in range(cols) if k != j] for i in range(rows)]
    return N

# Returns the matrix M without its row number i (starting from 0)
def delRow(M, i):
    rows,cols = len(M), len(M[0])
    N = [[M[j][k] for k in range(cols)] for j in range(rows) if j != i]
    return N