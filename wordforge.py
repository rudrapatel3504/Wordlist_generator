#!/usr/bin/env python3
"""
Wordlist_generator — Main Entry Point
Run: python wordforge.py
     ./wordforge.py (on Linux after chmod +x)
"""

import os
import sys

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

MENU = """
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
"""


def launch_webapp():
    print()
    print("  [*] Starting web server...")
    print("  [*] Open your browser at: http://localhost:5000")
    print("  [*] Press CTRL+C to stop the server.")
    print()
    try:
        from app import app
        app.run(debug=False)
    except ImportError:
        print("  [!] Flask not installed. Run: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n  [*] Server stopped. Goodbye.")


def launch_cli():
    print()
    # Pass all remaining sys.argv to CLI so flags still work
    # e.g. python wordforge.py -n john -y 1990 2005
    from wordforge_cli import main
    main()


def interactive_menu():
    """Show menu and let user pick mode interactively."""
    print(BANNER)
    print(MENU)

    while True:
        try:
            choice = input("  Enter choice (0/1/2): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye.")
            sys.exit(0)

        if choice == '1':
            launch_webapp()
            break
        elif choice == '2':
            launch_cli()
            break
        elif choice == '0':
            print("\n  Goodbye.\n")
            sys.exit(0)
        else:
            print("  [!] Invalid choice. Enter 1, 2, or 0.")


def main():
    # If CLI flags are passed directly, skip the menu and go straight to CLI
    # e.g. python wordforge.py -n john -y 1990 2005
    cli_flags = [a for a in sys.argv[1:] if a.startswith('-')]
    if cli_flags or any(a in sys.argv[1:] for a in ['--web', '--cli']):

        # --web flag forces webapp
        if '--web' in sys.argv:
            sys.argv.remove('--web')
            print(BANNER)
            launch_webapp()

        # --cli flag or any other flag → go straight to CLI
        else:
            if '--cli' in sys.argv:
                sys.argv.remove('--cli')
            print(BANNER)
            launch_cli()

    else:
        # No flags — show interactive menu
        interactive_menu()


if __name__ == '__main__':
    main()
