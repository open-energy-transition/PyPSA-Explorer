"""Tests for utility functions."""

import pytest

from pypsa_explorer.utils.helpers import (
    apply_carrier_colors,
    convert_latex_to_html,
    get_bus_carrier_options,
    get_carrier_nice_name,
    get_country_filter,
    get_country_options,
    title_except_multi_caps,
)
from pypsa_explorer.utils.network_loader import load_networks, parse_cli_network_args


class TestTextFormatting:
    """Test text formatting utilities."""

    def test_title_except_multi_caps_basic(self):
        """Test basic title case conversion."""
        assert title_except_multi_caps("hello world") == "Hello World"

    def test_title_except_multi_caps_preserves_acronyms(self):
        """Test that acronyms are preserved."""
        assert title_except_multi_caps("AC power") == "AC Power"
        assert title_except_multi_caps("HVDC link") == "HVDC Link"

    def test_title_except_multi_caps_mixed(self):
        """Test mixed case handling."""
        assert title_except_multi_caps("natural GAS storage") == "Natural GAS Storage"


class TestCarrierHelpers:
    """Test carrier-related helper functions."""

    def test_get_carrier_nice_name(self, demo_network):
        """Test getting carrier nice names."""
        nice_name = get_carrier_nice_name(demo_network, "wind")
        assert nice_name == "Wind"

    def test_apply_carrier_colors(self, demo_network):
        """Bars colored by carrier pick up the network's carrier colors."""
        fig = demo_network.statistics.installed_capacity.iplot.bar(
            x="value", y="carrier", color="carrier", nice_names=True, width=None
        )
        assert isinstance(fig.data[0].marker.color, str)

        apply_carrier_colors(fig, demo_network)

        colors_by_label = dict(zip(fig.data[0].y, fig.data[0].marker.color, strict=True))
        assert colors_by_label["Solar"] == "#ffea00"
        assert colors_by_label["Wind"] == "#74c6f2"

    def test_get_bus_carrier_options(self, demo_network):
        """Test getting bus carrier options for UI."""
        options = get_bus_carrier_options(demo_network)
        assert len(options) > 0
        assert all("label" in opt and "value" in opt for opt in options)

    def test_get_country_options(self, demo_network):
        """Test getting country options for UI."""
        options = get_country_options(demo_network)
        assert len(options) > 0
        assert all("label" in opt and "value" in opt for opt in options)
        # Check sorting
        labels = [opt["label"] for opt in options]
        assert labels == sorted(labels)


class TestCountryFilter:
    """Test country filtering functionality."""

    def test_country_filter_all(self):
        """Test country filter with 'All' mode."""
        query, facet, error = get_country_filter("All", [])
        assert query is None
        assert facet is None
        assert error is None

    def test_country_filter_specific_with_countries(self):
        """Test country filter with specific countries."""
        query, facet, error = get_country_filter("Specific", ["DE", "FR"])
        assert query == "country in ['DE', 'FR']"
        assert facet == "country"
        assert error is None

    def test_country_filter_specific_without_countries(self):
        """Test country filter with specific mode but no countries."""
        query, facet, error = get_country_filter("Specific", [])
        assert query is None
        assert facet is None
        assert error is not None


class TestNetworkLoader:
    """Test network loading utilities."""

    def test_load_networks_with_path(self, demo_network_path):
        """Test loading network from file path."""
        networks = load_networks(demo_network_path)
        assert len(networks) == 1
        assert "Network" in networks

    def test_load_networks_with_dict(self, demo_network_path):
        """Test loading networks from dictionary of paths."""
        networks = load_networks({"Test1": demo_network_path})
        assert len(networks) == 1
        assert "Test1" in networks

    def test_load_networks_with_network_objects(self, demo_network):
        """Test loading from Network objects."""
        networks = load_networks({"Test": demo_network})
        assert len(networks) == 1
        assert "Test" in networks

    def test_load_networks_invalid_path(self):
        """Test loading with invalid path raises error."""
        with pytest.raises(FileNotFoundError):
            load_networks("/nonexistent/path.nc")

    def test_parse_cli_network_args(self):
        """Test parsing CLI network arguments."""
        args = [
            "/path/to/network1.nc:Label1",
            "/path/to/network2.nc",
        ]
        result = parse_cli_network_args(args)
        assert result == {
            "Label1": "/path/to/network1.nc",
            "network2": "/path/to/network2.nc",
        }


class TestLatexConversion:
    """Test LaTeX to HTML conversion."""

    def test_convert_simple_subscript(self):
        """Test converting simple subscripts."""
        html = convert_latex_to_html("H$_2$")
        # Check that it contains subscript
        assert hasattr(html, "children")

    def test_convert_complex_subscript(self):
        """Test converting complex subscripts."""
        html = convert_latex_to_html("CO$_{2}$")
        assert hasattr(html, "children")

    def test_convert_no_subscript(self):
        """Test text without subscripts."""
        html = convert_latex_to_html("Normal text")
        assert hasattr(html, "children")
