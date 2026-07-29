#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:22:27 2026

@author: ethanbrown
"""
import os

SEARCH_TEXT = input("Search for: ").lower()

TEXT_EXTENSIONS = {
    ".txt", ".py", ".md", ".json", ".csv",
    ".html", ".css", ".js", ".xml",
    ".yaml", ".yml", ".ini", ".cfg",
    ".log", ".java", ".cpp", ".c",
    ".hpp", ".h", ".cs", ".swift",
    ".sql", ".sh", ".bat", ".rtf"
}

for root, dirs, files in os.walk("/", topdown=True):

    # Skip virtual/system folders that waste lots of time
    dirs[:] = [
        d for d in dirs
        if d not in {
            ".git",
            "__pycache__",
            ".Trash",
            ".Spotlight-V100",
            ".fseventsd",
            ".DocumentRevisions-V100",
            ".TemporaryItems",
        }
    ]

    for file in files:
        path = os.path.join(root, file)

        # Search filename
        if SEARCH_TEXT in file.lower():
            print(f"\n📁 Filename Match:\n{path}")

        # Search contents
        _, ext = os.path.splitext(file)

        if ext.lower() in TEXT_EXTENSIONS:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if SEARCH_TEXT in line.lower():
                            print(f"\n📄 Content Match:")
                            print(path)
                            print(f"Line {line_num}: {line.strip()}")
            except Exception:
                pass

print("\nFinished.")