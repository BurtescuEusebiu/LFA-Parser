from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
import pandas as pd
from typing import TypeVar
from functools import reduce

STATE = TypeVar('STATE')

@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]
    

    def accept(self, w: str) -> bool:
        curr = self.q0
        while w:
            c, w = w[0], w[1:]
            curr = self.d.get((curr, c))
            if curr is None:
                return False
        if curr in self.F:
            return True
        return False

    def minimize(self) -> 'DFA[STATE]':
        reach = set()
        stack = [self.q0]
        while stack:
            s = stack.pop()
            if s not in reach:
                reach.add(s)
                for c in self.S:
                    next_state = self.d.get((s, c))
                    if next_state is not None:
                        stack.append(next_state)

        K = self.K & reach
        F = self.F & reach


        P = set()
        W = set()
        F_fr = frozenset(F)
        NF_fr = frozenset(K - F)

        if F_fr:
            P.add(F_fr)
            W.add(F_fr)
        if NF_fr:
            P.add(NF_fr)
            W.add(NF_fr)

        while W:
            Q = W.pop()
            for c in self.S:
                X = {s for s in K if self.d.get((s, c)) in Q}
                for R in P.copy():
                    if X & R and R - X:
                        R1 = frozenset(X & R)
                        R2 = frozenset(R - X)
                        P.remove(R)
                        P.add(R1)
                        P.add(R2)
                        if R in W:
                            W.remove(R)
                            W.add(R1)
                            W.add(R2)
                        else:
                            if len(R1) <= len(R2):
                                W.add(R1)
                            else:
                                W.add(R2)
        states_map = {s: frozenset(part) for part in P for s in part}
        new_k = set(states_map.values())
        new_q = states_map[self.q0]
        new_d = {}
        for (s, symbol), next_state in self.d.items():
            if s in states_map and next_state in states_map:
                new_d[(states_map[s], symbol)] = states_map[next_state]

        new_f = {states_map[s] for s in self.F}
        return DFA(
            S=self.S,
            K=new_k,
            q0=new_q,
            d=new_d,
            F=new_f
        )
        
    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        return self
    
    