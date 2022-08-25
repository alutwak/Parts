
import re

from error import PartError


def parse_taxonomy(tax_dict, taxonomy=None):
    """Parse the taxonomy dictionary from a part."""
    if taxonomy is None:
        taxonomy = [tax_dict['value']]
    else:
        taxonomy.append(tax_dict['value'])
    if "children" in tax_dict and len(tax_dict['children']) > 0:
        return parse_taxonomy(tax_dict['children'][0], taxonomy)
    else:
        return "/".join(taxonomy)


class Part:
    """A single part."""

    def __init__(self, underlying_dict):
        """Construct the part."""
        self._dict = underlying_dict
        self._parameters = {}
        for param in self._dict['parameters']:
            self._parameters[param['parameter']] = param['value']

    @property
    def part_number(self):
        """Get the digikey part number."""
        return self["digi_key_part_number"]

    @property
    def family(self):
        """Get the family."""
        return self._get_value("family")

    @property
    def taxonomy(self):
        """Get the taxonomy."""
        if not hasattr(self, "_taxonomy"):
            tax_dict = self._dict['limited_taxonomy']
            self._taxonomy = parse_taxonomy(tax_dict)
        return self._taxonomy

    @property
    def pricing(self):
        """Get the part's pricing."""
        if not hasattr(self, '_pricing'):
            self._pricing = {}
            for pbreak in self._dict['standard_pricing']:
                quant = pbreak['break_quantity']
                price = pbreak['unit_price']
                self._pricing[quant] = float(price)
        return self._pricing

    @property
    def unit_price(self):
        """Get the price for a single unit.

        If there is no price for a single unit, then the price will be 0.0.
        """
        try:
            return self.pricing[1]
        except KeyError:
            return 0.0

    def get_price(self, units):
        """Get the price at a specified quantity.

        If the part is not available for the given quantity, then the price will be 0.0.
        """
        for quant, price in reversed(self.pricing.items()):
            if quant < units:
                return price
        return 0.0

    def _dict_index_by_regex(self, d, pattern):
        """Index a dictionary by regular expression."""
        regex = re.compile(pattern)
        for key, item in d.items():
            if regex.fullmatch(key) is not None:
                return item
        raise KeyError(f"{pattern} not found in {self.part_number}")

    def _get_parameter(self, param):
        """Get the parameter.

        The parameter may be expressed as a regular expression.
        """
        return self._parameters[param]

    @property
    def data(self):
        """Return the underlying data."""
        return self._dict

    def _get_value(self, param):
        """Get the value of a general parameter."""
        p = self._dict[param]
        if isinstance(p, dict):
            return p['value']
        return p

    def __getitem__(self, key):
        """Get the given part item."""
        if key == "price":
            return self.unit_price
        elif key == "taxonomy":
            return self.taxonomy
        try:
            return self._get_parameter(key)
        except KeyError:
            pass
        try:
            return self._get_value(key)
        except KeyError:
            raise PartError(f"'{key}' parameter not in part {self.part_number}")

    def index_regex(self, pattern):
        """Index the part by regular expression."""
        try:
            return self._dict_index_by_regex(self._parameters, pattern)
        except KeyError:
            pass
        return self._dict_index_by_regex(self._dict, pattern)
