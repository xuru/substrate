import env_setup; env_setup.setup()

import basin


alphabet = '23456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def encode(bytes, alphabet=alphabet):
    """
    Encodes the provided bytes with given alphabet.

    :param bytes: The bytes to be encoded
    :param alphabet: The string of characters used to encode the provided bytes, defaults to ``agar.codec.alphabet``
    """
    return basin.encode(alphabet, basin.bytestring_to_integer(bytes))


def decode(bytes, alphabet=alphabet):
    """
    Decodes the provided string with given alphabet.

    :param bytes: The encoded string to be decoded
    :param alphabet: The string of characters used to decode the provided bytes, defaults to ``agar.codec.alphabet``
    """
    return basin.integer_to_bytestring(basin.decode(alphabet, bytes))