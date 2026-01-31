from .Regex import Regex, parse_regex, Counter
from .NFA import NFA, EPSILON
from functools import reduce

class Lexer:
    def __init__(self, spec: list[tuple[str, str]]) -> None:
        nfaDict = {}
        tokenOrder = {}
        finalToken = {}
        nrCrt = 0
        for token,regex in spec:
            nfaDict[token] = parse_regex(regex).thompson()
            tokenOrder[token] = nrCrt
            nrCrt += 1

        start = Counter.new_state()
        S=set()
        K={start}
        d={}
        F=set()
        for token,nfa in nfaDict.items():
            d.setdefault((start, EPSILON), set()).add(nfa.q0)
            S = S | nfa.S
            K = K | nfa.K
            F = F | nfa.F

            for key, value in nfa.d.items():
                d.setdefault(key, set()).update(value)

            for f in nfa.F:
                finalToken[f]=token

        bigNFA = NFA(
            S=S,
            K=K,
            q0=start,
            d=d,
            F=F,
        )
        self.DFA = bigNFA.subset_construction()
        self.tokenOrder = tokenOrder
        self.finalToken = finalToken
    pass

    def lex(self, word: str) -> list[tuple[str, str]]:
        i = 0
        output = []
        while i < len(word):
            j = i
            last_accept = None
            last_accept_pos = 0
            curr_state = self.DFA.q0

            while j < len(word):
                next_state = self.DFA.d.get((curr_state, word[j]))
                if next_state is None or next_state == frozenset():
                    if last_accept is None:
                        nr_line = word.count('\n', 0, j)
                        output = []
                        curr_index = j
                        if nr_line > 0:
                            last_line_index = curr_index
                            while word[last_line_index] != '\n':
                                last_line_index = last_line_index - 1
                            curr_index = curr_index - last_line_index - 1
                        output.append(("", f"No viable alternative at character {curr_index}, line {nr_line}"))
                        return output
                    else:
                        break
                curr_state = next_state
                j=j+1
                accept_tokens = [self.finalToken[nfa_state] for nfa_state in curr_state if nfa_state in self.finalToken]
                if accept_tokens:
                    last_accept = curr_state
                    last_accept_pos = j

            if last_accept is None:
                nr_line = word.count('\n', 0, j)
                output = []
                output.append(("",f"No viable alternative at character EOF, line {nr_line}"))
                return output

            accept_tokens = [self.finalToken[nfa_state] for nfa_state in last_accept if nfa_state in self.finalToken]
            best_token = accept_tokens[0]
            for t in accept_tokens:
                if self.tokenOrder[t] < self.tokenOrder[best_token]:
                    best_token = t

            lexeme = word[i:last_accept_pos]
            output.append((best_token, lexeme))

            i = last_accept_pos
        return output
