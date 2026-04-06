"""
app.py — Flask web application for our DFA Stop Word Recognizer.

CPT411 Assignment
Our group topic: L6 English Stop Words Finder

"""

import os
from flask import Flask, render_template, request, redirect, url_for
from dfa import StopWordDFA

# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024   # to reject files > 16MB

# ── Single DFA instance shared across requests ────────────────────────────────
dfa = StopWordDFA()

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Render the home / upload page."""
    return render_template("index.html", stop_words=dfa.stop_words)


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Handle the uploaded .txt file:
        1. Read and decode the file content.
        2. Run the DFA over the text (character by character).
        3. Build context snippets and visualised HTML.
        4. Pass everything to results.html for display.
    """
    # ── Basic validation ──────────────────────────────────────────────────────
    if "file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "" or not file.filename.endswith(".txt"):
        return redirect(url_for("index"))

    # ── Read file ─────────────────────────────────────────────────────────────
    text = file.read().decode("utf-8")

    # ── Run DFA ───────────────────────────────────────────────────────────────
    #   process_text() returns list of (position, original_slice, matched_word)
    found = dfa.process_text(text)

    # ── Visualisation (highlighted HTML) ─────────────────────────────────────
    visualized_text = dfa.visualize_text_with_stopwords(text, found)

    # ── Build per-occurrence result rows for the results table ────────────────
    results = []
    for pos, original_slice, matched_word in found:
        # Grab ~20 chars either side for context
        ctx_start = max(0, pos - 20)
        ctx_end   = min(len(text), pos + len(original_slice) + 20)
        context   = text[ctx_start:ctx_end].replace("\n", " ")

        results.append({
            "word":          matched_word,      # canonical lowercase stop word
            "original":      original_slice,    # exact text as it appears in file
            "position":      pos,
            "context":       context,
        })

    # ── Count per stop word for the summary table ─────────────────────────────
    word_counts = {w: 0 for w in dfa.stop_words}
    for r in results:
        word_counts[r["word"]] += 1

    return render_template(
        "results.html",
        text=text,
        visualized_text=visualized_text,
        results=results,
        total_count=len(found),
        stop_words=dfa.stop_words,       
        word_counts=word_counts,
        filename=file.filename if file.filename else "uploaded file",
    )


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)