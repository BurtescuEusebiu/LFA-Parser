from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        next_states = {state}
        stack = [state]

        while stack:
            curr = stack.pop()
            for next in self.d.get((curr, EPSILON), set()):
                if next not in next_states:
                    next_states.add(next)
                    stack.append(next)

        return next_states

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        init = self.epsilon_closure(self.q0)
        new_k = {frozenset(init)}
        new_d = {}
        stack = [frozenset(init)]
        new_f = set()
        while stack:
            curr_state = stack.pop()
            for symbol in self.S:
                next_states = set()
                for nfa_state in curr_state:
                    for next in self.d.get((nfa_state, symbol), set()):
                        next_states.update(self.epsilon_closure(next))
                if next_states:
                    next_frozenset = frozenset(next_states)
                    new_d[(curr_state, symbol)] = next_frozenset
                    if next_frozenset not in new_k:
                        new_k.add(next_frozenset)
                        stack.append(next_frozenset)
        for s in new_k:
            if s & self.F:
                new_f.add(s)

        sink = frozenset()
        new_k.add(sink)
        for s in new_k:
            for symbol in self.S:
                if (s, symbol) not in new_d:
                    new_d[(s, symbol)] = sink
        for symbol in self.S:
            new_d[(sink, symbol)] = sink
                    
        return DFA(
            S=self.S,
            K=new_k,
            q0=frozenset(init),
            d=new_d,
            F=new_f
        )

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        return self
