"""
PyPSA Explorer - Interactive dashboard for visualizing and analyzing PyPSA energy system networks.

This package provides a comprehensive web-based dashboard for exploring PyPSA networks
with interactive visualizations, filtering capabilities, and multi-network support.
"""

__version__ = "0.1.2"
__author__ = "Open Energy Transition"
__email__ = "info@openenergytransition.org"

from pypsa_explorer.app import create_app, run_dashboard
from pypsa_explorer.utils.network_loader import load_networks

__all__ = [
    "create_app",
    "run_dashboard",
    "load_networks",
    "__version__",
]
