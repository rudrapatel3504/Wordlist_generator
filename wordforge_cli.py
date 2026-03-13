#!/usr/bin/env python3
"""
Wordlist_generator — CLI Tool
Usage: python wordforge_cli.py -n john -y 1990 2005
       ./wordforge_cli.py -n john smith --no-brute -o output.txt
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


# ─── CLI Args ─────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        prog='wordforge',
        description='Wordlist_generator — Targeted password wordlist generator',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
examples:
  python wordforge_cli.py -n john
  python wordforge_cli.py -n john smith
  python wordforge_cli.py -n john -y 1990 2005
  python wordforge_cli.py -n john smith -y 1985 2000 -o mylist.txt
  python wordforge_cli.py -n john --no-brute
  python wordforge_cli.py -n john -q
        """
    )

    parser.add_argument(
        '-n', '--names',
        nargs='+',
        required=True,
        metavar='NAME',
        help='One or two names in lowercase  e.g. -n john  or  -n john smith'
    )
    parser.add_argument(
        '-y', '--years',
        nargs=2,
        type=int,
        default=[1980, 2010],
        metavar=('FROM', 'TO'),
        help='Year range for YYYY patterns  (default: 1980 2010)'
    )
    parser.add_argument(
        '-o', '--output',
        default='wordlist.txt',
        metavar='FILE',
        help='Output file path  (default: wordlist.txt)'
    )
    parser.add_argument(
        '--no-brute',
        action='store_true',
        help='Skip brute 4-digit patterns — faster, smaller output'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress all output except errors'
    )

    return parser.parse_args()


# ─── Helpers ──────────────────────────────────────────────────────────────────

def log(msg, quiet=False):
    if not quiet:
        print(msg)


def progress_bar(label, current, total, width=30, quiet=False):
    if quiet:
        return
    filled = int(width * current / total) if total else 0
    bar    = '█' * filled + '░' * (width - filled)
    pct    = int(100 * current / total) if total else 0
    print(f'\r  {label:<20} [{bar}] {pct:3d}%', end='', flush=True)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    args   = parse_args()
    quiet  = args.quiet

    if not quiet:
        print(BANNER)

    # Validate names
    names  = [n.strip().lower() for n in args.names if n.strip()]
    errors = validate_names(names)
    if errors:
        print('[!] Error:', '; '.join(errors))
        sys.exit(1)

    if not names:
        print('[!] Please provide at least one name.')
        sys.exit(1)

    year_from, year_to = args.years
    if year_from > year_to:
        print(f'[!] Year FROM ({year_from}) must be ≤ Year TO ({year_to})')
        sys.exit(1)

    # Summary
    log(f'  [*] Names       : {", ".join(names)}', quiet)
    log(f'  [*] Year range  : {year_from} → {year_to}', quiet)
    log(f'  [*] Brute 4-dig : {"no" if args.no_brute else "yes"}', quiet)
    log(f'  [*] Output file : {args.output}', quiet)
    log('', quiet)

    # Generate
    log('  [*] Generating...', quiet)
    words = generate(
        names=names,
        year_from=year_from,
        year_to=year_to,
        include_brute=not args.no_brute
    )

    # Write output
    log(f'\n  [*] Writing {len(words):,} entries to "{args.output}"...', quiet)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(words) + '\n')

    size_kb = os.path.getsize(args.output) / 1024
    size_mb = size_kb / 1024

    log('', quiet)
    log('  ┌─────────────────────────────────┐', quiet)
    log(f'  │  ✓ Done!                         │', quiet)
    log(f'  │  Entries  : {len(words):>10,}          │', quiet)
    log(f'  │  File     : {args.output:<22} │', quiet)
    if size_mb >= 1:
        log(f'  │  Size     : {size_mb:>9.1f} MB          │', quiet)
    else:
        log(f'  │  Size     : {size_kb:>9.1f} KB          │', quiet)
    log('  └─────────────────────────────────┘', quiet)


if __name__ == '__main__':
    main()
