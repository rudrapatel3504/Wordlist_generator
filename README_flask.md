# WordForge 🔑 — Flask Webapp

A targeted password wordlist generator with a web interface, built with Python + Flask.

---

## Project Structure

```
wordforge/
├── app.py            ← Flask routes
├── generator.py      ← Core generation engine (shared logic)
├── requirements.txt
├── templates/
│   └── index.html    ← Frontend UI
└── README.md
```

---

## Installation

```bash
git clone https://github.com/you/wordforge.git
cd wordforge
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## Usage

1. Enter one or two **lowercase** names
2. Set a **year range** for YYYY patterns
3. Toggle **brute 4-digit** patterns on/off
4. Click **Generate & Download** — the `.txt` file downloads automatically

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Web UI |
| `POST` | `/generate` | Generate & stream wordlist as `.txt` download |
| `POST` | `/stats` | Returns estimated entry count (JSON) |

### `/generate` — Request body (JSON)

```json
{
  "name1": "john",
  "name2": "smith",
  "year_from": 1980,
  "year_to": 2010,
  "include_brute": true
}
```

### `/stats` — Response

```json
{ "count": 207736 }
```

---

## Output Priority Order

Passwords are ordered top → bottom by likelihood:

| Priority | Format | Example |
|---|---|---|
| 🟢 1 | YYYY | `john@1995`, `John1995` |
| 🔵 2 | DDMM | `john@0112`, `John#3101` |
| 🔵 2 | MMDD | `john@1231`, `John$0101` |
| 🔵 2 | DDDD | `john@1520`, `John#0131` |
| 🔵 2 | MMMM | `john@0912`, `John$1112` |
| ⚫ 3 | Brute | `john#0000`, `john9999$` |

---

## Disclaimer

This tool is for **authorized security testing**, **CTF challenges**, and **penetration testing with explicit permission only**. Do not use against systems you do not own.

---

## License

MIT
