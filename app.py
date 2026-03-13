"""
WordForge Flask Webapp
Run: python app.py
Then open: http://localhost:5000
"""

import io
import time
import json
from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from generator import generate, validate_names

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_wordlist():
    """
    Accepts JSON: { name1, name2, year_from, year_to, include_brute }
    Streams the wordlist as a plain .txt file download.
    """
    data = request.get_json()

    name1        = (data.get('name1') or '').strip().lower()
    name2        = (data.get('name2') or '').strip().lower()
    year_from    = int(data.get('year_from', 1980))
    year_to      = int(data.get('year_to',   2010))
    include_brute = data.get('include_brute', True)

    # Collect non-empty names
    names = [n for n in [name1, name2] if n]

    # Validate
    if not names:
        return jsonify(error='Please enter at least one name.'), 400

    errors = validate_names(names)
    if errors:
        return jsonify(error='; '.join(errors)), 400

    if year_from > year_to:
        return jsonify(error=f'Year FROM ({year_from}) must be ≤ Year TO ({year_to})'), 400

    # Generate
    words = generate(names, year_from, year_to, include_brute=include_brute)

    # Stream as file download
    def stream():
        for word in words:
            yield word + '\n'

    filename = '_'.join(names) + '_wordlist.txt'

    return Response(
        stream_with_context(stream()),
        mimetype='text/plain',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )


@app.route('/stats', methods=['POST'])
def stats():
    """
    Returns estimated entry count without generating the full list.
    Used to show a live count preview on the frontend.
    """
    data = request.get_json()

    name1     = (data.get('name1') or '').strip()
    name2     = (data.get('name2') or '').strip()
    year_from = int(data.get('year_from', 1980))
    year_to   = int(data.get('year_to',   2010))
    include_brute = data.get('include_brute', True)

    names = [n for n in [name1, name2] if n]
    if not names or year_from > year_to:
        return jsonify(count=0)

    num_names  = len(names)
    num_years  = max(0, year_to - year_from + 1)
    ddmm_count = 31 * 12          # 372
    mmdd_count = 12 * 31          # 372
    dddd_count = 31 * 31          # 961
    mmmm_count = 12 * 12          # 144
    specials   = 3
    variants   = 2                 # name + Name

    per_token  = variants + (variants * specials * 2)   # plain + sp+token + token+sp
    date_total = (num_years + ddmm_count + mmdd_count + dddd_count + mmmm_count) * per_token
    brute_total = (specials * 10000 * variants + 10000 + specials * 10000) if include_brute else 0

    estimate = (date_total + brute_total) * num_names

    return jsonify(count=estimate)


if __name__ == '__main__':
    app.run(debug=True)
