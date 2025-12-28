"""Shared pytest fixtures.

See @tests/AGENTS.md for test guidance.
See @docs/tooling/pytest.md for pytest documentation.
"""

import pytest


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Provide sample data for tests."""
    return {"key": "value"}

