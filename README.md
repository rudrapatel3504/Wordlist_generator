# Wordlist_generator 🔑 — Password Wordlist Generator

A targeted password wordlist generator with **two interfaces**:
- 🌐 **Flask Web App** — browser-based UI with file download
- 💻 **Linux CLI** — terminal tool for scripting and pipelines

> ⚠️ For **authorized security testing**, **CTF challenges**, and **penetration testing with explicit permission** only.

---

## 🔗 Repository

**[github.com/rudrapatel3504/Wordlist_generator](https://github.com/rudrapatel3504/Wordlist_generator)**

---

## 📁 Project Structure

```
Wordlist_generator/
├── app.py               ← Flask webapp (routes & API)
├── wordforge_cli.py     ← Linux CLI tool
├── generator.py         ← Core engine (shared by both)
├── requirements.txt     ← Dependencies (just Flask)
├── templates/
│   └── index.html       ← Frontend UI
└── README.md
```

> `generator.py` is the shared core — both the webapp and CLI use it. No duplicated logic.

---

## ⚙️ Installation

```bash
git clone https://github.com/rudrapatel3504/Wordlist_generator.git
cd Wordlist_generator
pip install -r requirements.txt
```

---

## 🚀 Quick Start

Just run the main entry point — it will ask you which mode you want:

```bash
python wordforge.py
```

```
  ┌─────────────────────────────────────────┐
  │         SELECT MODE                     │
  ├─────────────────────────────────────────┤
  │  [1]  Web App  —  browser UI            │
  │       opens http://localhost:5000       │
  │                                         │
  │  [2]  CLI      —  terminal mode         │
  │       generate wordlist directly        │
  │                                         │
  │  [0]  Exit                              │
  └─────────────────────────────────────────┘
```

You can also skip the menu by passing flags directly:

```bash
# Force webapp
python wordforge.py --web

# Force CLI (any CLI flag also works)
python wordforge.py --cli
python wordforge.py -n john -y 1990 2005
```

---

## 🌐 Web App

Select `[1]` from the menu, or run `python wordforge.py --web`.

Then open **http://localhost:5000** in your browser.

1. Enter one or two **lowercase** names (second is optional)
2. Set a **year range** for YYYY patterns
3. Toggle **brute 4-digit** patterns on/off
4. Click **Generate & Download** — `.txt` file downloads automatically

---

## 💻 CLI (Linux)

Select `[2]` from the menu, or pass flags directly:

```bash
python wordforge.py -n NAME [NAME] [-y FROM TO] [-o FILE] [--no-brute] [-q]
```

### Arguments

| Argument | Description | Default |
|---|---|---|
| `-n`, `--names` | One or two names (lowercase only) | required |
| `-y`, `--years` | Year range for YYYY patterns | `1980 2010` |
| `-o`, `--output` | Output file path | `wordlist.txt` |
| `--no-brute` | Skip 4-digit brute patterns (faster) | off |
| `-q`, `--quiet` | Suppress all output except errors | off |

### Examples

```bash
# Single name
python wordforge_cli.py -n john

# Two names
python wordforge_cli.py -n john smith

# Custom year range
python wordforge_cli.py -n john -y 1990 2005

# Two names, custom range, custom output file
python wordforge_cli.py -n john smith -y 1985 2000 -o john_smith.txt

# Skip brute patterns (faster, smaller file)
python wordforge_cli.py -n john --no-brute

# Quiet mode — no output, just generates the file
python wordforge_cli.py -n john smith -q
```

---

## 🌐 API Endpoints (Flask)

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Web UI |
| `POST` | `/generate` | Generate & stream wordlist as `.txt` download |
| `POST` | `/stats` | Returns estimated entry count (JSON) |

### `/generate` — Request Body (JSON)

```json
{
  "name1": "john",
  "name2": "smith",
  "year_from": 1980,
  "year_to": 2010,
  "include_brute": true
}
```

---

## 📋 Output Format

One password per line, plain `.txt`:

```
john1995
John1995
john@1995
John@1995
john1995@
John1995@
...
john@0112
John#3101
...
john#0000
john9999$
```

---

## 📊 Priority Order (top → bottom in output file)

| Priority | Format | Description | Example |
|---|---|---|---|
| 🟢 1 | YYYY | Year only | `john@1995`, `John2001` |
| 🔵 2 | DDMM | Day(01–31) + Month(01–12) | `john@0112`, `John#3101` |
| 🔵 2 | MMDD | Month(01–12) + Day(01–31) | `john@1231`, `John$0101` |
| 🔵 2 | DDDD | Day × Day (01–31 × 01–31) | `john@1520`, `John#0131` |
| 🔵 2 | MMMM | Month × Month (01–12 × 01–12) | `john@0912`, `John$1112` |
| ⚫ 3 | Brute | 0000–9999 all combos | `john#0000`, `john9999$` |

---

## 🔢 Pattern Reference

For every name (`john` / `John`) and each date token:

```
john<token>       John<token>
john@<token>      John@<token>
john#<token>      John#<token>
john$<token>      John$<token>
john<token>@      John<token>@
john<token>#      John<token>#
john<token>$      John<token>$
```

---

## 📦 Requirements

- Python 3.7+
- Flask 3.0+ *(only needed for the web app)*

```bash
pip install -r requirements.txt
```

---

## ⚖️ Disclaimer

This tool is intended for **legal and authorized use only**, including:
- Authorized penetration testing
- CTF (Capture The Flag) challenges
- Security research on systems you own

**Do not use against systems without explicit permission.** The author is not responsible for any misuse.

---

## 👤 Author

**Rudra Patel** — [github.com/rudrapatel3504](https://github.com/rudrapatel3504)

---

## 📄 License

MIT
