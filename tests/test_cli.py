import runpy
from importlib.metadata import version

import pytest

from python_prj_seed.cli import main


def test_greets_world_by_default(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert capsys.readouterr().out == "Hello, world!\n"


def test_greets_the_given_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada!\n"


def test_version_prints_the_installed_version(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])

    assert exit_info.value.code == 0
    assert capsys.readouterr().out == f"{version('python-prj-seed')}\n"


def test_unknown_option_exits_with_usage_error() -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--unknown"])

    assert exit_info.value.code == 2  # argparse's exit code for usage errors


def test_runs_as_a_module(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["python-prj-seed"])

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module("python_prj_seed", run_name="__main__")

    assert exit_info.value.code == 0
    assert capsys.readouterr().out == "Hello, world!\n"
