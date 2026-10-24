from python_prj_seed.domain import greet


def test_greet_includes_the_name() -> None:
    assert greet("Ada") == "Hello, Ada!"
