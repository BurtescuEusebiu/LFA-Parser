# LFA-Parser
%
% Descriere
% ----------
% Proiectul are două etape și este implementat în Python.
% Scop: lucrul cu automate și parser pentru expresii lambda.
%
% Etapa 1: Conversia expresiilor regulate (REGEX) → NFA → DFA → minDFA
%           - Minim DFA implementat folosind algoritmul Hopcroft
%
% Etapa 2: Implementarea Lexer și Parser folosind DFA și gramatica în FNC
%           - Parser implementat folosind algoritmul CYKa Parse (CYK)
%
%
% Etapa 1 – Automate
% ------------------
% Clase:
%   - Regex: generează NFA din regex
%   - NFA: epsilon-closure, subset-construction
%   - DFA: acceptare cuvânt și minimizare (Hopcroft)
%
% Funcționalități:
%   - Regex suportă: *, +, ?, |, (), [a-z], [A-Z], [0-9], caractere escaped
%   - Spațiile sunt ignorate dacă nu sunt escape-uite
%   - STATE flexibil: int, string, frozenset
%
%
% Etapa 2 – Lexer și Parser
% -------------------------
% Lexer:
%   - Specificație: spec = [(TOKEN, regex), ...]
%   - Output: listă de tupluri (token, lexem)
%   - Identifică cel mai lung subsir valid
%   - Erori: "No viable alternative at character N, line X"
%
% Parser:
%   - Folosește output-ul lexer-ului
%   - Verifică apartenența la limbaj FNC
%   - Algoritm: CYKa Parse (CYK)
%   - Returnează ParseTree
%   - Fișiere config:
%       - grammar_lambda.txt (gramatica în FNC)
%       - lexer_spec.json (tokeni)
%
% Exemplu arbore parsare:
% assign
%   (TYPE: int)
%   (ID: x)
%   (EQUAL: =)
%   sum
%     (NUMBER: 1)
%     (PLUS: +)
%     (NUMBER: 2)
%
%
% Testare
% -------
% Python 3.12
% Comandă pentru rularea testelor:
% python3.12 -m unittest
%
%
% Structura arhivei
% -----------------
% .
% ├── grammar_lambda.txt
% ├── lexer_spec.json
% ├── src
% │   ├── __init__.py
% │   ├── DFA.py
% │   ├── NFA.py
% │   ├── Regex.py
% │   ├── Lexer.py
% │   ├── Parser.py
% │   ├── Grammar.py
% │   ├── ParseTree.py
% │   └── ... (alte surse)
% ├── ID.txt
%
%
% Licență
% -------
% CC Attribution-Share Alike 3.0 Unported (CC BY-SA)
