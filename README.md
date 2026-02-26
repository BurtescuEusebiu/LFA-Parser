# LFA Parser

## Description
The project consists of two stages and is implemented in Python.  
Goal: working with automata and building a parser for lambda expressions.

- **Stage 1**: Conversion of regular expressions (REGEX) → NFA → DFA → minDFA  
  - DFA minimization implemented using **Hopcroft’s algorithm**
- **Stage 2**: Implementation of a Lexer and Parser using DFA and a CNF grammar  
  - Parser implemented using the **CYK Parse algorithm**

---

## Stage 1 – Automata

**Classes:**
- `Regex`: generates NFA from a regular expression  
- `NFA`: epsilon-closure, subset construction  
- `DFA`: word acceptance and minimization (Hopcroft)  

**Features:**
- Regex supports: `*`, `+`, `?`, `|`, `()`, `[a-z]`, `[A-Z]`, `[0-9]`, escaped characters  
- Whitespaces are ignored unless escaped  
- Flexible `STATE` type: `int`, `string`, `frozenset`  

---

## Stage 2 – Lexer and Parser

### Lexer
- Specification format: `spec = [(TOKEN, regex), ...]`  
- Returns a list of tuples `(token, lexeme)`  
- Identifies the longest valid substring  
- Error format: `"No viable alternative at character N, line X"`  

### Parser
- Uses the lexer output  
- Verifies membership in a CNF language  
- Algorithm: **CYK Parse**  
- Returns a `ParseTree`  
- Configuration files:  
  - `grammar_lambda.txt` – grammar in CNF  
  - `lexer_spec.json` – token specification  

**Example parse tree:**
```
expr
  (LAMBDA: \)
  (VAR: x)
  (POINT: .)
  expr
    (LAMBDA: \)
    (VAR: y)
    (POINT: .)
    expr
      (LPAREN: ()
      expr
        (VAR: x)
        (OP: +)
        (VAR: y)
      (RPAREN: ))
```

## Automated Testing
- Python 3.12  
```bash
python3.12 -m unittest

