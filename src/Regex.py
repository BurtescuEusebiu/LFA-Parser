from typing import Any, List
from .NFA import NFA

EPSILON = ''

class Regex:
    def thompson(self) -> NFA[int]:
        raise NotImplementedError()
    
class Counter:
    cnt = 0

    @classmethod
    def new_state(new):
        s = new.cnt
        new.cnt += 1
        return s


def parse_regex(regex: str) -> Regex:
    parser = Parser(regex)
    return parser.parse()
    
class Parser:
    def __init__(self, regex: str):
        self.tokens = tokenize(regex)
        self.pos = 0

    def parse(self) -> Regex:
        return self.parse_union()

    def parse_union(self) -> Regex:
        left = self.parse_concat()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '|':
            self.pos += 1
            right = self.parse_concat()
            left = Union(left, right)
        return left

    def parse_concat(self) -> Regex:
        l = self.parse_unary()
        while self.pos < len(self.tokens) and self.tokens[self.pos] not in {')', '|'}:
            r = self.parse_unary()
            l = Concat(l, r)
        return l


    def parse_unary(self) -> Regex:
        e = self.parse_other()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in {'*', '+', '?'}:
            op = self.tokens[self.pos]
            self.pos += 1
            if op == '*':
                e = Star(e)
            elif op == '+':
                e = Plus(e)
            elif op == '?':
                e = Optional(e)
        return e

    def parse_other(self) -> Regex:
        token = self.tokens[self.pos]

        if token == '(':
            self.pos += 1
            expr = self.parse_union()
            self.pos += 1
            return expr

        if token == 'eps':
            self.pos += 1
            return Eps()

        if token.startswith('\\'):
            self.pos += 1
            return Char(token[1])

        if token.startswith('[') and '-' in token:
            self.pos += 1
            start, end = token[1], token[3]
            chars = [Char(chr(c)) for c in range(ord(start), ord(end)+1)]
            expr = chars[0]
            for c in chars[1:]:
                expr = Union(expr, c)
            return expr

        self.pos += 1
        return Char(token)

def tokenize(regex: str) -> list[str]:
    tokens = []
    i = 0

    while i < len(regex):
        if regex.startswith("eps", i):
            tokens.append("eps")
            i += 3
            continue

        if regex[i] == '\\':
            tokens.append(regex[i:i+2])
            i += 2
            continue


        if regex[i] == ' ':
            i += 1
            continue

        if regex[i] == '[':
            j = regex.find(']', i)
            ins = regex[i+1:j]
            tokens.append(f"[{ins[0]}-{ins[2]}]")
            i = j + 1
            continue

        if regex[i] in {'(', ')', '*', '+', '?', '|'}:
            tokens.append(regex[i])
            i += 1
            continue

        tokens.append(regex[i])
        i += 1

    return tokens

  

class Char(Regex):
    def __init__(self, c: str):
        self.c = c

    def thompson(self):
        start, end = Counter.new_state(), Counter.new_state()

        transitions = {(start, self.c): {end}}
        return NFA(
            S={self.c},
            K={start, end},
            q0=start,
            d=transitions,
            F={end}
        )


class Concat(Regex):
    def __init__(self, left: Regex, right: Regex):
        self.left = left
        self.right = right

    def thompson(self):
        nfa1 = self.left.thompson()
        nfa2 = self.right.thompson()

        d = dict(nfa1.d)
        for key, value in nfa2.d.items():
            d[key] = value

        for f in nfa1.F:
            d.setdefault((f, EPSILON), set()).add(nfa2.q0)

        return NFA(
            S=nfa1.S | nfa2.S,
            K=nfa1.K | nfa2.K,
            q0=nfa1.q0,
            d=d,
            F=nfa2.F
        )


class Union(Regex):
    def __init__(self, left: Regex, right: Regex):
        self.left = left
        self.right = right

    def thompson(self):
        nfa1 = self.left.thompson()
        nfa2 = self.right.thompson()

        start, end = Counter.new_state(), Counter.new_state()
        d = dict(nfa1.d)
        for key, value in nfa2.d.items():
            d[key] = value
        d[(start, EPSILON)] = {nfa1.q0, nfa2.q0}
        for f in nfa1.F:
            d.setdefault((f, EPSILON), set()).add(end)
        for f in nfa2.F:
            d.setdefault((f, EPSILON), set()).add(end)

        return NFA(
            S=nfa1.S | nfa2.S,
            K=nfa1.K | nfa2.K | {start, end},
            q0=start,
            d=d,
            F={end}
        )


class Star(Regex):
    def __init__(self, expr: Regex):
        self.expr = expr

    def thompson(self):
        nfa = self.expr.thompson()
        start, end = Counter.new_state(), Counter.new_state()
        d = dict(nfa.d)
        d[(start, EPSILON)] = {nfa.q0, end}
        for f in nfa.F:
            d.setdefault((f, EPSILON), set()).update({nfa.q0, end})
        return NFA(
            S=nfa.S,
            K=nfa.K | {start, end},
            q0=start,
            d=d,
            F={end}
        )


class Plus(Regex):
    def __init__(self, expr: Regex):
        self.expr = expr

    def thompson(self):
        nfa = self.expr.thompson()
        start, end = Counter.new_state(), Counter.new_state()
        d = dict(nfa.d)
        for f in nfa.F:
            d.setdefault((f, EPSILON), set()).update({nfa.q0, end})
        return NFA(
            S=nfa.S,
            K=nfa.K | {start, end},
            q0=nfa.q0,
            d=d,
            F={end}
        )


class Optional(Regex):
    def __init__(self, expr: Regex):
        self.expr = expr

    def thompson(self):
        nfa = self.expr.thompson()
        start, end = Counter.new_state(), Counter.new_state()
        d = dict(nfa.d)
        d[(start, EPSILON)] = {nfa.q0, end}
        for f in nfa.F:
            d.setdefault((f, EPSILON), set()).add(end)
        return NFA(
            S=nfa.S,
            K=nfa.K | {start, end},
            q0=start,
            d=d,
            F={end}
        )


class Eps(Regex):
    def __init__(self):
        pass

    def thompson(self):
        start, end = Counter.new_state(), Counter.new_state()

        d = {(start, EPSILON): {end}}
        return NFA(
            S=set(),
            K={start, end},
            q0=start,
            d=d,
            F={end}
        )

