#!/usr/bin/env python3
"""Entry point for the wiki sync tool. The logic lives in the wikisync package."""
import sys

from wikisync.cli import main

if __name__ == "__main__":
    sys.exit(main())
