from pathlib import Path
import argparse
import tempfile
import os
import shutil
import sys

#!/usr/bin/env python3
"""
txt_cleaner.py

Remove all lines that contain the token "<media removed>" (case-insensitive)
from a text file. By default the input file is updated in-place; an output
path may be provided to write the cleaned content elsewhere.

Usage:
    python txt_cleaner.py input.txt
    python txt_cleaner.py input.txt -o cleaned.txt
"""

TOKEN = "<Media omitted>"

def clean_file(input_path: Path, output_path: Path | None = None, token: str = TOKEN):
    input_path = input_path.expanduser().resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path:
        output_path = output_path.expanduser().resolve()
        tmp_path = None
    else:
        # write to a temp file in same directory then atomically replace
        tmp = tempfile.NamedTemporaryFile(delete=False, dir=str(input_path.parent), prefix=input_path.name + ".", suffix=".tmp")
        tmp_path = Path(tmp.name)
        tmp.close()
        output_path = tmp_path

    token_lower = token.lower()
    with input_path.open("r", encoding="utf-8", errors="replace", newline="") as src, \
         output_path.open("w", encoding="utf-8", newline="") as dst:
        for line in src:
            if token_lower in line.lower():
                continue
            dst.write(line)

    if tmp_path:
        # replace original file atomically
        shutil.copystat(input_path, tmp_path)  # preserve permission/time where possible
        os.replace(str(tmp_path), str(input_path))

def main(argv=None):
    parser = argparse.ArgumentParser(description="Remove lines containing '<media removed>' from a text file.")
    parser.add_argument("input", help="Path to input .txt file")
    parser.add_argument("-o", "--output", help="Optional output path. If omitted, input file is updated in-place")
    parser.add_argument("-t", "--token", default=TOKEN, help="Token to remove lines containing (default: '<media removed>')")
    args = parser.parse_args(argv)

    try:
        clean_file(Path(args.input), Path(args.output) if args.output else None, token=args.token)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()