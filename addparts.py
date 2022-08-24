
import sys
import os
from traceback import print_exc
from argparse import ArgumentParser

from library import Library
from error import PartError

PARTS_MAP_PATH = os.path.expanduser("~/.part-map.yaml")


def add_part(library, part, stock, continue_on_error):
    """Add a part to the library."""
    try:
        if stock is None:
            library.add_part(part)
        else:
            library.add_part(part, stock=stock)
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
            try:
                part, stock = line.split(",")
            except ValueError:
                part = line
                stock = None

            if stock is not None:
                try:
                    stock = int(stock)
                except ValueError:
                    print(f"Warning: stock of {stock.strip()} is invalid for part {part}")
                    stock = None
            add_part(library, part.strip(), stock, continue_on_error)


def main():
    """Add parts to a workbook."""
    parser = ArgumentParser("Add parts to an Excel workbook. All part numbers must be given as Digikey part numbers.")
    parser.add_argument("workbook_path", help="Path to the workbook to add parts to")
    parser.add_argument("-L", "--parts_list", help=("Path to a text file with a list of parts to add, one part per line."
                                                    " Optional stock values can be included for each part by adding a "
                                                    " comma-separated integer after the part number."))
    parser.add_argument("-p", "--part", action="append", help="Part number to add")
    parser.add_argument("-s", "--stock", action="append", help=("Stock associated with each part. This is optional,"
                                                                " but if it is used, each part must have an associated"
                                                                " stock number."))
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
        if args.stock is not None:
            assert(len(args.stock) == len(args.part))
            for part, stock in zip(args.part, args.stock):
                add_part(library, part, stock, args.continue_on_error)
        else:
            for part in args.part:
                add_part(library, part, None, args.continue_on_error)

    library.save()


if __name__ == "__main__":
    main()
