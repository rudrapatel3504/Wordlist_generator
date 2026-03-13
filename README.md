# Wordlist_generator 🔑 — Password Wordlist Generator

A targeted password wordlist generator with a web interface, built with Python + Flask.

> ⚠️ For **authorized security testing**, **CTF challenges**, and **penetration testing with explicit permission** only.

---

## 🔗 Repository

**[github.com/rudrapatel3504/Wordlist_generator](https://github.com/rudrapatel3504/Wordlist_generator)**

---

## 📁 Project Structure

```
Wordlist_generator/
├── app.py            ← Flask routes & API endpoints
├── generator.py      ← Core generation engine (pure logic, no Flask)
├── requirements.txt  ← Dependencies (just Flask)
├── templates/
│   └── index.html    ← Frontend UI
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/rudrapatel3504/Wordlist_generator.git
cd Wordlist_generator
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 🚀 Usage

1. Enter one or two **lowercase** names (second name is optional)
2. Set a **year range** for YYYY patterns (default: 1980–2010)
3. Toggle **brute 4-digit** patterns on/off
4. Click **Generate & Download** — the `.txt` file downloads automatically

---

## 🌐 API Endpoints

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

### `/stats` — Response

```json
{ "count": 207736 }
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

## 🔢 Pattern Reference

For every name (`john` / `John`) and each date token:

```
john<token>          John<token>
john@<token>         John@<token>
john#<token>         John#<token>
john$<token>         John$<token>
john<token>@         John<token>@
john<token>#         John<token>#
john<token>$         John<token>$
```

---

## 📊 Priority Order (top → bottom in output file)

Passwords are ordered by likelihood — most probable at the top:

| Priority | Format | Description | Example |
|---|---|---|---|
| 🟢 1 | YYYY | Year only | `john@1995`, `John2001` |
| 🔵 2 | DDMM | Day + Month (01–31, 01–12) | `john@0112`, `John#3101` |
| 🔵 2 | MMDD | Month + Day (01–12, 01–31) | `john@1231`, `John$0101` |
| 🔵 2 | DDDD | Day + Day (01–31 × 01–31) | `john@1520`, `John#0131` |
| 🔵 2 | MMMM | Month + Month (01–12 × 01–12) | `john@0912`, `John$1112` |
| ⚫ 3 | Brute | 0000–9999 all combos | `john#0000`, `john9999$` |

---

## 📦 Requirements

- Python 3.7+
- Flask 3.0+

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