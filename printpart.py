"""CLI tool to print the parameters of a part."""
from argparse import ArgumentParser
import pprint

from parts import Parts


def main():
    """Print the parameters of a part as a json object."""
    parser = ArgumentParser("Print the parameters of a part as a json object")
    parser.add_argument("part", help="Digikey part number of the part to print")
    args = parser.parse_args()

    parts = Parts()
    part = parts.get_part(args.part)
    pprint.pprint(part.data)


if __name__ == "__main__":
    main()
