import logging
import argparse
import re
import sys

def set_argparse():
    """
    Set up an argument parser for the wc command.

    Returns:
        The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(prog='wc', description="Parse the arguments on the CLI for wc command")
    # Define options as optional arguments
    parser.add_argument('-c', '--bytes', action='store_true', help='count number of bytes')
    parser.add_argument('-l', '--lines', action='store_true', help='count number of lines in a file')
    parser.add_argument('-w', '--words', action='store_true', help='count number of words in a file')
    parser.add_argument('-m', '--chars', action='store_true', help='count number of characters in a file')

    # Handle file names as positional arguments
    parser.add_argument('files', metavar='FILE', type=str, nargs='*', help='Files to process')

    args = parser.parse_args()
    return args

def count_bytes(file):
    """
    Counts the number of bytes in a given file.

    Args:
        file (str): The path to the file to be counted.

    Returns:
        int: The number of bytes in the file.
    """
    bytes = 0

    # read in file as byte file
    with open(file, "rb") as file1:
        # count each byte
        for line in file1:
            bytes += len(line) # count number of bytes in the line, no conversion here

    return bytes

def count_lines(file):
    """
    Counts the number of lines in a given file.

    Args:
        file (str): The path to the file to be counted.

    Returns:
        int: The number of lines in the file.
    """
    lines = 0

    # read in file as just a read, can count lines from here
    with open(file, "r") as file1:
        # count each line
        for _ in file1:
            lines += 1

    return lines

def count_words(file):
    """
    Counts the total number of words in a file.

    Args:
        file (str): The path to the file to be counted.

    Returns:
        int: The total number of words in the file.
    """
    words = 0

    # read in file as a read, split lines
    with open(file, "r") as file1:
        # count words
        for line in file1:
            words += len(line.split())

    return words

def count_chars(file):
    """
    Counts the number of characters in a file.

    Args:
        file (str): The path to the file to be counted.

    Returns:
        int: The total number of characters in the file.
    """
    chars = 0

    # read in file as a read, count chars
    with open(file, "r") as file1:
        # count characters
        for line in file1:
            line_length = len(line)
            new_lines = len(re.findall(r'\n+', line))
            chars += line_length
            chars += new_lines

    return chars

if __name__ == '__main__':
    args = set_argparse()
    file_contents = ''

    if not args.files:
        file_contents = sys.stdin.readlines()

    # Check if any of the flags are set
    no_flags_set = not (args.bytes or args.lines or args.words or args.chars)

    if file_contents:
        try:
            file_counts = []

            if args.lines or no_flags_set:
                lines = len(file_contents)
                file_counts.append(lines)
            
            if args.words or no_flags_set:
                words = sum(len(line.split()) for line in file_contents)
                file_counts.append(words)
            
            if args.bytes or no_flags_set:
                bytes = sum(len(line.encode('utf-8')) for line in file_contents)
                file_counts.append(bytes)
            
            if args.chars:
                chars = sum(len(line) for line in file_contents)
                file_counts.append(chars)

            print("  ", "  ".join(map(str, file_counts)))
    
        except IOError as e:
            logging.error(f"Error: {e}")
    else:
        for file_path in args.files:
            try:
                file_counts = []

                # Count lines if -l is set or if no flags are set (default behavior)
                if args.lines or no_flags_set:
                    file_counts.append(count_lines(file_path))

                # Count words if -w is set or if no flags are set (default behavior)
                if args.words or no_flags_set:
                    file_counts.append(count_words(file_path))

                # Count bytes if -c is set or if no flags are set (default behavior)
                if args.bytes or no_flags_set:
                    file_counts.append(count_bytes(file_path))

                # Count characters only if -m is explicitly set
                if args.chars:
                    file_counts.append(count_chars(file_path))

                print("  ", "  ".join(map(str, file_counts)), file_path)

            except IOError as e:
                logging.error(f"Error: {e}")
   