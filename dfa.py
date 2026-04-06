"""
CPT411 Assignment
Our group topic: L6 English Stop Words Finder (our stop words - and, the, then, so, into, if, with)

The DFA processes input ONE CHARACTER AT A TIME, simulating a finite state machine.
No string matching functions or regex/APIs are used — pure automata implementation.

"""


class StopWordDFA:
    """
    A Deterministic Finite Automaton (DFA) for recognizing English stop words.

    Stop Words Detected:
    ====================
    1. "and"  - conjunction
    2. "the"  - article    
    3. "then" - adverb              ← shares prefix "th" and "the" with "the"
    4. "so"   - conjunction / adverb
    5. "into" - preposition
    6. "if"   - conjunction
    7. "with" - preposition

    DFA State Map:
    ==============
    State  0 : START — no characters matched yet
    State  1 : Matched 'a'           (prefix of "and")
    State  2 : Matched 'an'          (prefix of "and")
    State  3 : ACCEPT                → "and"

    State  4 : Matched 't'           (shared prefix of "the" / "then")
    State  5 : Matched 'th'          (shared prefix of "the" / "then")
    State  6 : Matched 'the'         (ACCEPT for "the"; can extend to "then")
    State  7 : Matched 'then'        (ACCEPT for "then")

    State  8 : Matched 's'           (prefix of "so")
    State  9 : Matched 'so'          (ACCEPT → "so",  final char: 'o')

    State 10 : Matched 'i'           (shared prefix of "into" / "if")
    State 11 : Matched 'in'          (prefix of "into")
    State 12 : Matched 'int'         (prefix of "into")
    State 13 : Matched 'into'        (ACCEPT → "into", final char: 'o')
    State 14 : Matched 'if'          (ACCEPT → "if",   final char: 'f')

    State 15 : Matched 'w'           (prefix of "with")
    State 16 : Matched 'wi'          (prefix of "with")
    State 17 : Matched 'wit'         (prefix of "with")
    State 18 : Matched 'with'        (ACCEPT → "with", final char: 'h')

    State -1 : TRAP — invalid prefix; no stop word is possible from here

    """

    def __init__(self):
        """Initialize the DFA: define states, build the transition table."""

        # ── Stop words this DFA recognises ──────────────────────────────────
        self.stop_words = ["and", "the", "so", "into", "then", "if", "with"]

        # ── Special states ───────────────────────────────────────────────────
        self.START = 0
        self.TRAP  = -1

        # ── Accept states  →  which stop word each one represents ────────────
        self.accept_states = {
            3:  "and",
            6:  "the",
            7:  "then",
            9:  "so",
            13: "into",
            14: "if",
            18: "with",
        }

        # ── Build transition table ───────────────────────────────────────────
        self.transitions = {}
        self._build_transitions()

    # ────────────────────────────────────────────────────────────────────────
    # Internal helpers
    # ────────────────────────────────────────────────────────────────────────

    def _build_transitions(self):
        """
        Build the complete transition table  δ(state, char) → next_state.

        Every (state, char) pair not listed here implicitly goes to TRAP.

        """

        # State 0 — START: first character determines which stop word branch
        self.transitions[0] = {
            'a': 1,   # → branch for "and"
            't': 4,   # → branch for "the" / "then"
            's': 8,   # → branch for "so"
            'i': 10,  # → branch for "into" / "if"
            'w': 15,  # → branch for "with"
        }

        # ── "and" branch ─────────────────────────────────────────────────────
        # State 1: matched 'a'
        self.transitions[1] = {'n': 2}

        # State 2: matched 'an'
        self.transitions[2] = {'d': 3}

        # State 3: ACCEPT — "and" complete; no further transitions needed
        self.transitions[3] = {}

        # ── "the" / "then" branch ────────────────────────────────────────────
        # State 4: matched 't'
        self.transitions[4] = {'h': 5}        

        # State 5: matched 'th'
        self.transitions[5] = {'e': 6}

        # State 6: ACCEPT — "the" complete.
        self.transitions[6] = {'n': 7}      

        # State 7: ACCEPT — "then" complete; no further transitions needed
        self.transitions[7] = {}

        # ── "so" branch ──────────────────────────────────────────────────────
        # State 8: matched 's'
        self.transitions[8] = {'o': 9}

        # State 9: ACCEPT — "so" complete
        self.transitions[9] = {}

        # ── "into" / "if" branch ─────────────────────────────────────────────
        # State 10: matched 'i'
        self.transitions[10] = {
            'n': 11,  # → "into"
            'f': 14,  # → "if" (accept immediately on next char check)
        }

        # State 11: matched 'in'
        self.transitions[11] = {'t': 12}

        # State 12: matched 'int'
        self.transitions[12] = {'o': 13}

        # State 13: ACCEPT — "into" complete
        self.transitions[13] = {}

        # State 14: ACCEPT — "if" complete
        self.transitions[14] = {}

        # ── "with" branch ────────────────────────────────────────────────────
        # State 15: matched 'w'
        self.transitions[15] = {'i': 16}

        # State 16: matched 'wi'
        self.transitions[16] = {'t': 17}

        # State 17: matched 'wit'
        self.transitions[17] = {'h': 18}

        # State 18: ACCEPT — "with" complete
        self.transitions[18] = {}

    def get_next_state(self, current_state, char):
        """
        Transition function  δ(current_state, char) → next_state.

        Converts the character to lowercase first so the DFA is case-insensitive ("The", "THE", "tHe" all map to "the").

        Args:
            current_state (int): The active DFA state.
            char          (str): The single input character being processed.

        Returns:
            int: The next state, or TRAP if no valid transition exists.
        """
        char = char.lower()

        if current_state == self.TRAP:
            return self.TRAP

        if current_state in self.transitions and char in self.transitions[current_state]:
            return self.transitions[current_state][char]

        return self.TRAP  # no valid transition → trap

    # ────────────────────────────────────────────────────────────────────────
    # Core DFA processing
    # ────────────────────────────────────────────────────────────────────────

    def process_word(self, word):
        """
        Run the DFA on a single alphabetic word (one character at a time).

        Args:
            word (str): A purely alphabetic string (no punctuation).

        Returns:
            tuple: (is_stop_word: bool, matched_word: str | None)
        """
        if not word:
            return False, None

        current_state = self.START
        chars_processed = 0

        # ── Core simulation: one character at a time ─────────────────────────
        for char in word:
            current_state = self.get_next_state(current_state, char)
            chars_processed += 1

            # Early exit: trap state means this word cannot be a stop word
            if current_state == self.TRAP:
                return False, None

        # ── After the last character: check accept state AND full word match ──
        # We must have consumed exactly len(word) characters AND be in an
        # accept state.  The length check ensures "android" doesn't match "and".
        if current_state in self.accept_states and chars_processed == len(word):
            return True, self.accept_states[current_state]

        return False, None

    def process_text(self, text):
        """
        Scan an entire text and return every stop word occurrence.

        Returns:
            list of (position: int, original_slice: str, matched_word: str)
                position      — character index of the word's start in `text`
                original_slice — the original casing from the text (e.g. "The")
                matched_word  — the canonical lowercase stop word (e.g. "the")
        """
        results = []
        current_word = ""
        word_start   = 0

        for i, char in enumerate(text):
            if char.isalpha():
                if not current_word:
                    word_start = i        # mark start of new word
                current_word += char
            else:
                if current_word:
                    is_stop, matched = self.process_word(current_word)
                    if is_stop:
                        # Store position, the original text slice, and the matched word
                        original_slice = text[word_start: word_start + len(current_word)]
                        results.append((word_start, original_slice, matched))
                    current_word = ""

        # Handle final word if text ends without a delimiter
        if current_word:
            is_stop, matched = self.process_word(current_word)
            if is_stop:
                original_slice = text[word_start: word_start + len(current_word)]
                results.append((word_start, original_slice, matched))

        return results

    # ────────────────────────────────────────────────────────────────────────
    # Visualisation
    # ────────────────────────────────────────────────────────────────────────

    def visualize_text_with_stopwords(self, text, stopword_results):
        """
        Wrap every detected stop word in the text with an HTML <span> tag
        so it can be highlighted in the browser.

        Args:
            text             (str):  The full original text.
            stopword_results (list): Output of process_text() —
                                     list of (position, original_slice, matched_word).

        Returns:
            str: HTML string with stop words wrapped in <span class="stopword">.
        """
        parts    = []
        last_pos = 0

        for pos, original_slice, _ in stopword_results:
            parts.append(text[last_pos:pos])                          # text before match
            parts.append(f'<span class="stopword">{original_slice}</span>')  # highlighted match (original casing)
            last_pos = pos + len(original_slice)

        parts.append(text[last_pos:])   # remaining text after last match
        return "".join(parts)

    # ────────────────────────────────────────────────────────────────────────
    # Utility / debug
    # ────────────────────────────────────────────────────────────────────────

    def get_dfa_info(self):
        """Return a summary dict about this DFA (used by the web UI)."""
        return {
            "stop_words":    self.stop_words,
            "total_states":  len(self.transitions) + 1,   # +1 for trap state
            "accept_states": list(self.accept_states.keys()),
            "start_state":   self.START,
            "trap_state":    self.TRAP,
        }

    def print_dfa_info(self):
        """Print the full DFA structure to stdout (useful for the demo / report)."""
        sep = "=" * 70
        print(sep)
        print("DFA STOP WORD RECOGNIZER — AUTOMATA INFORMATION")
        print(sep)
        print(f"\nStop Words  : {', '.join(self.stop_words)}")
        print(f"Total States: {len(self.transitions) + 1}  (states 0–18 + trap state -1)")
        print(f"Start State : {self.START}")
        print(f"Trap State  : {self.TRAP}")
        print(f"Accept States:")
        for state, word in self.accept_states.items():
            print(f"   State {state:>2} → '{word}'")
        print("\nTransition Function  δ(state, char) = next_state:")
        for state, trans in self.transitions.items():
            for char, nxt in trans.items():
                print(f"   δ({state:>2}, '{char}') = {nxt}")
        print(sep)