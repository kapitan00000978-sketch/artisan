#!/usr/bin/env python3
"""
Artisan CLI (Backward Compatibility Layer for Hallwright CLI).
All commands and routines are maintained in hallwright_cli.py.
"""
import sys
from hallwright_cli import *
from hallwright_cli import main

if __name__ == "__main__":
    sys.exit(main())
