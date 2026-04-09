import sys
import os
import warnings

import pytest

# Add src/ to Python path so tests can import project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Suppress known harmless warnings from colour-science library
warnings.filterwarnings("ignore", message=".*related API features are not available.*")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*invalid value encountered in log.*")


@pytest.fixture(autouse=True)
def force_english_locale():
    """Ensure tests always run in English regardless of system locale."""
    import i18n
    i18n._current_lang = "en"
