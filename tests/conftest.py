"""Pytest configuration for local source imports and integration gating."""

from pathlib import Path
import os
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

INTEGRATION_FILES = {
    "test_decide.py",
    "test_direct_order_placement.py",
    "test_end_to_end.py",
    "test_live_order_execution.py",
    "test_real_order_placement.py",
}
INTEGRATION_NODEIDS = {
    "tests/test_execute.py::test_sell_limit_order_functionality",
    "tests/test_execute.py::test_profit_taking_orders",
}


def _has_live_credentials() -> bool:
    key_file = ROOT / "kalshi_private_key.pem"
    return key_file.exists() and bool(os.getenv("KALSHI_API_KEY"))


def pytest_collection_modifyitems(config, items):
    if _has_live_credentials():
        return

    skip_live = pytest.mark.skip(
        reason="Skipping live Kalshi integration tests: missing KALSHI_API_KEY or kalshi_private_key.pem"
    )
    for item in items:
        if item.fspath.basename in INTEGRATION_FILES or item.nodeid in INTEGRATION_NODEIDS:
            item.add_marker(skip_live)
