"""Application logic, independent of how it is invoked.

Nothing here reads arguments, prints or exits: that belongs to the delivery
layer in `cli`, so this module can be tested and reused without it.
"""


def greet(name: str) -> str:
    """Return the greeting for `name`."""
    return f"Hello, {name}!"
