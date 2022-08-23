
import sys
import os
from traceback import print_exc
from argparse import ArgumentParser

from library import Library
from error import PartError

PARTS_MAP_PATH = os.path.expanduser("~/.part-map.yaml")


def add_part(library, part, continue_on_error):
    """Add a part to the library."""
    try:
        library.add_part(part)
        return
    except PartError as e:
        print(f"{e}")
    except Exception as e:
        print_exc()
        print(f"Failed to add {part}: {e.__class__} {e}")
    if not continue_on_error:
        sys.exit(1)


def add_from_list_file(library, list_path, continue_on_error):
    """Add parts from a file."""
    with open(list_path) as f:
        for line in f:
            add_part(library, line.strip(), continue_on_error)


def main():
    """Add parts to a workbook."""
    parser = ArgumentParser("Add parts to an Excel workbook. All part numbers must be given as Digikey part numbers.")
    parser.add_argument("workbook_path", help="Path to the workbook to add parts to")
    parser.add_argument("-L", "--parts_list", help="Path to a text file with a list of parts to add, one part per line")
    parser.add_argument("-p", "--part", action="append", help="Part number to add")
    parser.add_argument("-C", "--cached", action="store_true", help="Add all parts from the cache")
    parser.add_argument("-c", "--continue_on_error", action="store_true", help="Continue on an error")
    parser.add_argument("--config", default=PARTS_MAP_PATH, help="Path to a custom parts map configuration")
    args = parser.parse_args()

    if args.parts_list is None and args.cached is None and len(args.part) == 0:
        print(("At least one part number is required, "
               "a path to a parts list must be given "
               "or parts must be loaded from the cache."))
        parser.print_usage()
        sys.exit(1)

    library = Library(args.workbook_path, args.config)

    if args.cached:
        library.add_cached_parts()
    if args.parts_list is not None:
        add_from_list_file(library, args.parts_list, args.continue_on_error)

    if args.part is not None:
        for part in args.part:
            add_part(library, part, args.continue_on_error)

    library.save()


if __name__ == "__main__":
    main()
