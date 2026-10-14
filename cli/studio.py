#!/usr/bin/env python3
"""
Artisan Studio CLI Front-End
Empowered by The Council of Masters
"""

import sys
import os

# Redirect to scripts/artisan_studio.py
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, scripts_dir)

from artisan_studio import main

if __name__ == "__main__":
    main()
