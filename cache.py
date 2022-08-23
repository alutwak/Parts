"""Defines a cache for storing the digikey part info."""

import os
import shelve

CACHE_PATH = os.path.expanduser("~/.parts-cache.db")


class PartsCache:
    """Caches the digikey part information."""

    def __init__(self):
        """Construct PartsCache."""
        self._db = shelve.open(CACHE_PATH)

    def __del__(self):
        """Destroy PartsCache."""
        print("closing cache")
        self._db.close()

    def __iter__(self):
        """Iterate over the cache."""
        return self._db.__iter__()

    def __next__(self):
        """Get the next part in the cache."""
        return self._db.__next()

    def get_part(self, digikey_part_number):
        """Get the part, if it exists."""
        if digikey_part_number in self._db:
            return self._db[digikey_part_number]

    def set_part(self, digikey_part_number, data):
        """Set the data for the given part number."""
        self._db[digikey_part_number] = data
