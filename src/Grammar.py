from .ParseTree import ParseTree
EPSILON = ""

class Grammar:

    @classmethod
    def fromFile(cls, file_name: str):
        with open(file_name, 'r') as f:
            V = set()
            R = set()
            S = None
            line = f.readline().strip()
            while line:
                v, rest = line.split(": ")
                V.add(v)
                if not S:
                    S = v

                alternatives = rest.split("|")
                for alt in alternatives:
                    if " " in alt:
                        n1, n2 = alt.split(" ")
                        V.add(n1)
                        V.add(n2)
                        R.add((v, n1, n2))
                    else: 
                        V.add(alt)
                        R.add((v, alt, None))
            
                line = f.readline().strip()

        return cls(V, R, S)
    
    def __init__(self, V: set[str], R: set[tuple[str, str, str|None]], S: str):
        self.V = V # multimea de neterminali si terminali
        self.R = R # regulile (in FNC)
        self.S = S # simbolul de start
        
    def cykParse(self, w: list[tuple[str, str]]):
        n = len(w)
        if(n == 0):
            return None
        table = [[dict() for _ in range(n)] for _ in range(n)]

        for i in range(n):
            token, lexeme = w[i]
            for (a, b, c) in self.R:
                if c is None and b == token:
                    tree = ParseTree(a,(token,lexeme))
                    table[i][i][a] = tree

        for l in range(2,n+1):
            for i in range(n-l+1):
                j = i + l - 1
                for k in range(i, j):
                    for (a, b, c) in self.R:
                        if c is not None:
                            if b in table[i][k] and c in table[k + 1][j]:
                                left = table[i][k][b]
                                right = table[k + 1][j][c]
                                tree = ParseTree(a)
                                tree.add_children(left)
                                tree.add_children(right)
                                table[i][j][a] = tree

        if self.S in table[0][n-1]:
            return table[0][n-1][self.S]
        return None
        

            

