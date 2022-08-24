
import os
from argparse import ArgumentParser

from library import Library

PARTS_MAP_PATH = os.path.expanduser("~/.part-map.yaml")


def main():
    """Add parts to a workbook."""
    parser = ArgumentParser("Add parts to an Excel workbook. All part numbers must be given as Digikey part numbers.")
    parser.add_argument("workbook_path", help="Path to the workbook to add parts to")
    parser.add_argument("--config", default=PARTS_MAP_PATH, help="Path to a custom parts map configuration")
    args = parser.parse_args()

    library = Library(args.workbook_path, args.config)
    library.resheet_parts()
    library.save()


if __name__ == "__main__":
    main()
