# StopWord_DFA 🔍

A **Deterministic Finite Automaton (DFA)** implementation that recognises common English stop words from an uploaded text file. 

---

## What It Does

The program reads a `.txt` file and processes it **one character at a time**, simulating a finite state machine. It detects the following stop words:

| Word | Type |
|------|------|
| `and` | conjunction |
| `the` | article |
| `then` | adverb |
| `so` | conjunction / adverb |
| `into` | preposition |
| `if` | conjunction |
| `with` | preposition |

For each stop word found, it reports the **position**, **original casing**, and **surrounding context**. Stop words are also **highlighted visually** in the output.

---

## Project Structure

```
CPT411Ass/
├── app.py                  # Flask web application (routes)
├── dfa.py                  # DFA logic — state machine implementation
├── templates/
│   ├── index.html          # Upload page
│   └── results.html        # Results page
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## DFA Design

The DFA has **19 states** plus a **trap state (−1)**:

```
State  0  →  START
State  1  →  matched 'a'          (prefix: "and")
State  2  →  matched 'an'         (prefix: "and")
State  3  →  ACCEPT               → "and"
State  4  →  matched 't'          (prefix: "the"/"then")
State  5  →  matched 'th'         (prefix: "the"/"then")
State  6  →  matched 'the'        (ACCEPT → "the"; extends to "then")
State  7  →  matched 'then'       (ACCEPT → "then")
State  8  →  matched 's'          (prefix: "so")
State  9  →  matched 'so'         (ACCEPT → "so")
State 10  →  matched 'i'          (prefix: "into"/"if")
State 11  →  matched 'in'         (prefix: "into")
State 12  →  matched 'int'        (prefix: "into")
State 13  →  matched 'into'       (ACCEPT → "into")
State 14  →  matched 'if'         (ACCEPT → "if")
State 15  →  matched 'w'          (prefix: "with")
State 16  →  matched 'wi'         (prefix: "with")
State 17  →  matched 'wit'        (prefix: "with")
State 18  →  matched 'with'       (ACCEPT → "with")
State -1  →  TRAP (early exit)
```
---

## Getting Started

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jashh18/CPT411Ass.git
   cd CPT411Ass
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage

1. On the home page, upload any `.txt` file (max 16 MB)
2. Click **Run DFA →**
3. The results page shows:
   - ✅ **ACCEPTED** / ❌ **REJECTED** verdict
   - Occurrence count per stop word
   - Full visualised text with stop words highlighted in amber
   - Detailed table with position and context for each match

---

## Author

Course: CPT411 — Automata Theory & Formal Languages
Assignment: L6 — English Stop Words Finder

**Sabrina binti Sofian**  
**Dershyani Thessaruva**  
**Tejashree Laxmi**  