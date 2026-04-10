
import os
from typing import List, Optional


def read_file(file_path: str) -> List[str]:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except IOError as e:
        raise IOError(f"Cannot read file {file_path}: {e}")


def filter_lines(lines: List[str], keyword: str) -> List[str]:
    """Filter lines that contain a specific keyword."""
    if not keyword:
        return []

    return [line for line in lines if keyword in line]

def write_file(file_path: str, lines: List[str]) -> None:
    """Write lines to a text file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
    except IOError as e:
        raise IOError(f"Cannot write to file {file_path}: {e}")

def filter_text_file(input_file: str, output_file: str, keyword: str) -> int:
    """Main function to filter text file by keyword."""
    lines = read_file(input_file)
    filtered_lines = filter_lines(lines, keyword)
    write_file(output_file, filtered_lines)
    return len(filtered_lines)


def main():
    """Command line interface for the text filter."""
    import sys

    if len(sys.argv) != 4:
        print("Usage: python text_filter.py <input_file> <output_file> <keyword>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    keyword = sys.argv[3]

    try:
        count = filter_text_file(input_file, output_file, keyword)
        print(f"Successfully filtered {count} lines to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()