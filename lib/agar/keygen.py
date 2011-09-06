from uuid import uuid4
from codec import encode

def _gen_key(size=2):
    return ''.join(''.join(it) for it in zip(uuid4().bytes for _ in range(size)))


def gen_short_key():
    """
    Generates a short key (22 chars +/- 1) with a high probability of uniqueness
    """
    return encode(_gen_key(size=1))

def gen_medium_key():
    """
    Generates a medium key (44 chars +/- 1) with a higher probability of uniqueness
    """
    return encode(_gen_key(size=2))

def gen_long_key():
    """
    Generates a long key (66 chars +/- 1) with the highest probability of uniqueness
    """
    return encode(_gen_key(size=3))

generate_key = gen_medium_key
