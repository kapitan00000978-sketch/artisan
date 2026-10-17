#!/usr/bin/env python3
"""Compatibility alias for Hallwright Studio."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hallwright_studio import (
    capture_visual_metrics,
    run_studio_critique,
    elevate_html_to_world_class,
    main
)

if __name__ == "__main__":
    main()
