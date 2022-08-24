"""Digikey API."""

import digikey
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

digikey_logger = logging.getLogger('digikey')
digikey_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
digikey_logger.addHandler(handler)


class DigikeyPartError(Exception):
    """Part did not match any digikey part names."""

    pass


def digikey_part_details(digikey_part_number):
    """Retrieve the part details for the part with the given digikey part number.

    Requires the following environment variables to work:
    DIGIKEY_CLIENT_ID=<client_id>
    DIGIKEY_CLIENT_SECRET=<client_secret>
    DIGIKEY_CLIENT_SANDBOX=False
    DIGIKEY_STORAGE_PATH<storage_path>
    """
    details = digikey.product_details(digikey_part_number)
    if details is None:
        raise DigikeyPartError(f"{digikey_part_number} part not found")
    return details.to_dict()
