import pytest

from python_prj_seed import main


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    main()

    assert capsys.readouterr().out == "Hello from python-prj-seed!\n"
