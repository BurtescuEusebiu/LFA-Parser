# LFA Parser

## Descriere
Proiectul are două etape și este implementat în Python.  
Scop: lucrul cu automate și parser pentru expresii lambda.

- **Etapa 1**: Conversia expresiilor regulate (REGEX) → NFA → DFA → minDFA  
  - Minim DFA implementat folosind algoritmul **Hopcroft**  
- **Etapa 2**: Implementarea Lexer și Parser folosind DFA și gramatica în FNC  
  - Parser implementat folosind algoritmul **CYK Parse**  

---

## Etapa 1 – Automate

**Clase:**
- `Regex`: generează NFA din regex  
- `NFA`: epsilon-closure, subset-construction  
- `DFA`: acceptare cuvânt și minimizare (Hopcroft)  

**Funcționalități:**
- Regex suportă: `*`, `+`, `?`, `|`, `()`, `[a-z]`, `[A-Z]`, `[0-9]`, caractere escaped  
- Spațiile sunt ignorate dacă nu sunt escape-uite  
- `STATE` flexibil: `int`, `string`, `frozenset`  

---

## Etapa 2 – Lexer și Parser

### Lexer
- Specificație: `spec = [(TOKEN, regex), ...]`  
- Returnează lista de tupluri `(token, lexem)`  
- Identifică cel mai lung subsir valid  
- Erori: `"No viable alternative at character N, line X"`  

### Parser
- Folosește output-ul lexer-ului  
- Verifică apartenența la limbaj FNC  
- Algoritm: **CYK Parse**  
- Returnează `ParseTree`  
- Fișiere config:  
  - `grammar_lambda.txt` – gramatica în FNC  
  - `lexer_spec.json` – specificația tokenilor  

**Exemplu arbore parsare:**
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

## Testare automată
- Python 3.12  
```bash
python3.12 -m unittest

