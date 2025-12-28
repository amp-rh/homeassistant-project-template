"""Example tests.

See @tests/AGENTS.md for test guidance.
"""

# TODO: Update import to your package name
from my_package import __version__


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_sample_fixture(sample_data: dict[str, str]):
    """Test using a fixture from conftest.py."""
    assert sample_data["key"] == "value"
