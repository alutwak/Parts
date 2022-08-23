
from cache import PartsCache
from digikey_api import digikey_part_details
from part import Part


class Parts:
    """The parts library."""

    def __init__(self):
        """Construct the parts library."""
        self._cache = PartsCache()

    def __del__(self):
        """Force the cache to immediately delete."""
        del(self._cache)

    def get_part(self, digikey_part_number):
        """Get the part info with the given part number.

        This will first look in the cache. If the part number isn't in the cache then it will be retrieved from digikey
        and store the info in the cache before returning it.
        """
        part = self._cache.get_part(digikey_part_number)
        if part is not None:
            return Part(part)
        part = self.update_part(digikey_part_number)
        return Part(part)

    def update_part(self, digikey_part_number):
        """Update the part details from digikey."""
        part = digikey_part_details(digikey_part_number)
        self._cache.set_part(digikey_part_number, part)
        return Part(part)

    def __contains__(self, digikey_part_number):
        """Support the `in` operator."""
        return digikey_part_number in self._cache

    def __iter__(self):
        """Iterate over the parts."""
        return self._cache.__iter__()

    def __next__(self):
        """Get the next part."""
        return self._cache.__next__()
