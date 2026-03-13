#!/usr/bin/env python3
"""
Wordlist_generator — CLI Tool
Asks questions one by one when launched from the main menu.
Can also be used directly with flags:
  python wordforge_cli.py -n john -y 1990 2005
"""

import argparse
import os
import sys
from generator import generate, validate_names

BANNER = r"""
 _    _               _ _ _     _     _____                           _
| |  | |             | | (_)   | |   / ____|                         | |
| |  | | ___  _ __ __| | |_ ___| |_ | |  __  ___ _ __   ___ _ __ ___| |_ ___  _ __
| |/\| |/ _ \| '__/ _` | | / __| __|| | |_ |/ _ \ '_ \ / _ \ '__/ _ \ __/ _ \| '__|
\  /\  / (_) | | | (_| | | \__ \ |_ | |__| |  __/ | | |  __/ | |  __/ || (_) | |
 \/  \/ \___/|_|  \__,_|_|_|___/\__| \_____|\___|_| |_|\___|_|  \___|\__\___/|_|

  github.com/rudrapatel3504/Wordlist_generator
  For authorized security testing only.
"""


# ─── Helpers ──────────────────────────────────────────────────────────────────

def ask(prompt, default=None):
    """Ask a question, return stripped input. CTRL+C exits cleanly."""
    try:
        hint = f' [{default}]' if default is not None else ''
        val  = input(f'  {prompt}{hint}: ').strip()
        return val if val else (str(default) if default is not None else '')
    except (KeyboardInterrupt, EOFError):
        print('\n\n  Aborted. Goodbye.')
        sys.exit(0)


def divider():
    print('  ' + '-' * 45)


# ─── Interactive wizard ───────────────────────────────────────────────────────

def interactive():
    """Ask questions one by one and return collected inputs as a dict."""

    print()
    divider()
    print('  STEP 1 -- Target Names')
    divider()

    # Name 1 - required
    while True:
        name1 = ask('Enter first name (lowercase only)').lower()
        if not name1:
            print('  [!] First name cannot be empty.')
            continue
        errors = validate_names([name1])
        if errors:
            print(f'  [!] {errors[0]}')
            continue
        break

    # Name 2 - optional
    print()
    print('  Second name is optional -- press Enter to skip.')
    while True:
        name2 = ask('Enter second name (or press Enter to skip)').lower()
        if not name2:
            name2 = None
            break
        errors = validate_names([name2])
        if errors:
            print(f'  [!] {errors[0]}')
            continue
        break

    print()
    divider()
    print('  STEP 2 -- Year Range  (used for YYYY patterns)')
    divider()

    # Year from
    while True:
        val = ask('Year FROM', default=1980)
        try:
            year_from = int(val)
            if 1900 <= year_from <= 2099:
                break
            print('  [!] Enter a year between 1900 and 2099.')
        except ValueError:
            print('  [!] Please enter a valid year.')

    # Year to
    while True:
        val = ask('Year TO  ', default=2010)
        try:
            year_to = int(val)
            if year_to < year_from:
                print(f'  [!] Year TO must be >= Year FROM ({year_from}).')
                continue
            if year_to > 2099:
                print('  [!] Enter a year between 1900 and 2099.')
                continue
            break
        except ValueError:
            print('  [!] Please enter a valid year.')

    print()
    divider()
    print('  STEP 3 -- Brute Force Patterns')
    divider()
    print('  Adds name+0000 to name+9999 combos (~200k entries per name).')
    print()

    while True:
        choice = ask('Include brute 4-digit patterns? (y/n)', default='y').lower()
        if choice in ('y', 'yes'):
            include_brute = True
            break
        elif choice in ('n', 'no'):
            include_brute = False
            break
        else:
            print('  [!] Please enter y or n.')

    print()
    divider()
    print('  STEP 4 -- Output File')
    divider()

    names_str   = name1 + (f'_{name2}' if name2 else '')
    default_out = f'{names_str}_wordlist.txt'
    output      = ask('Output filename', default=default_out)
    if not output:
        output = default_out

    return {
        'names':         [n for n in [name1, name2] if n],
        'year_from':     year_from,
        'year_to':       year_to,
        'include_brute': include_brute,
        'output':        output,
    }


# ─── CLI flags mode ───────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        prog='wordforge',
        description='Wordlist_generator -- Targeted password wordlist generator',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
examples:
  python wordforge_cli.py -n john
  python wordforge_cli.py -n john smith
  python wordforge_cli.py -n john -y 1990 2005
  python wordforge_cli.py -n john smith -y 1985 2000 -o mylist.txt
  python wordforge_cli.py -n john --no-brute
        """
    )
    parser.add_argument('-n', '--names',  nargs='+', metavar='NAME',
                        help='One or two names (lowercase only)')
    parser.add_argument('-y', '--years',  nargs=2, type=int, default=[1980, 2010],
                        metavar=('FROM', 'TO'), help='Year range (default: 1980 2010)')
    parser.add_argument('-o', '--output', default=None, metavar='FILE',
                        help='Output file (default: <name>_wordlist.txt)')
    parser.add_argument('--no-brute',    action='store_true',
                        help='Skip brute 4-digit patterns')
    parser.add_argument('-q', '--quiet',  action='store_true',
                        help='Suppress all output except errors')
    return parser.parse_args()


# ─── Run generation ───────────────────────────────────────────────────────────

def run(names, year_from, year_to, include_brute, output, quiet=False):

    if not quiet:
        print()
        divider()
        print(f'  [*] Names       : {", ".join(names)}')
        print(f'  [*] Year range  : {year_from} -> {year_to}')
        print(f'  [*] Brute 4-dig : {"yes" if include_brute else "no"}')
        print(f'  [*] Output file : {output}')
        divider()
        print('  [*] Generating wordlist...')
        print()

    words = generate(names, year_from, year_to, include_brute=include_brute)

    if not quiet:
        print(f'  [*] Writing {len(words):,} entries to "{output}"...')

    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(words) + '\n')

    size_kb = os.path.getsize(output) / 1024
    size_mb = size_kb / 1024

    if not quiet:
        print()
        print('  +---------------------------------------+')
        print('  |  Done!                                |')
        print(f'  |  Entries  : {len(words):>12,}            |')
        print(f'  |  File     : {output:<24} |')
        if size_mb >= 1:
            print(f'  |  Size     : {size_mb:>11.1f} MB          |')
        else:
            print(f'  |  Size     : {size_kb:>11.1f} KB          |')
        print('  +---------------------------------------+')
        print()


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # If -n flag is given -> skip wizard, run directly with flags
    if args.names:
        if not args.quiet:
            print(BANNER)

        names  = [n.strip().lower() for n in args.names if n.strip()]
        errors = validate_names(names)
        if errors:
            print('[!] Error:', '; '.join(errors))
            sys.exit(1)

        year_from, year_to = args.years
        if year_from > year_to:
            print(f'[!] Year FROM ({year_from}) must be <= Year TO ({year_to})')
            sys.exit(1)

        names_str = '_'.join(names)
        output    = args.output or f'{names_str}_wordlist.txt'

        run(names, year_from, year_to,
            include_brute=not args.no_brute,
            output=output,
            quiet=args.quiet)

    else:
        # No flags -> launch interactive wizard
        print(BANNER)
        cfg = interactive()
        run(**cfg)


if __name__ == '__main__':
    main()