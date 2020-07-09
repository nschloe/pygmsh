import pathlib

import exdown
import pytest

this_dir = pathlib.Path(__file__).resolve().parent


@pytest.mark.parametrize(
    "string", exdown.extract(this_dir.parent / "README.md", syntax_filter="python"),
)
def test_readme(string):
    exec(string)
