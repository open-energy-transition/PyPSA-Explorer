"""Helper utility functions for PyPSA Explorer."""

import re
from contextlib import suppress
from pathlib import Path
from typing import Any

import plotly.graph_objects as go
import pypsa
from dash import html
from pypsa.plot.statistics.base import sanitize_mathtext
from pypsa.plot.statistics.charts import ChartGenerator


def title_except_multi_caps(text: str) -> str:
    """
    Convert words to title case, except words with multiple uppercase letters.

    Parameters
    ----------
    text : str
        The input string to process

    Returns
    -------
    str
        Processed string with words in title case, except those with multiple uppercase letters
    """
    words = text.split()
    result = []

    for word in words:
        uppercase_count = sum(1 for char in word if char.isupper())
        if uppercase_count > 1:
            result.append(word)
        else:
            result.append(word.capitalize())

    return " ".join(result)


def get_carrier_nice_name(n: pypsa.Network, carrier: str) -> str:
    """
    Retrieve the nice name of a carrier from the network.

    Falls back to the carrier index if not available.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object
    carrier : str
        The carrier name to retrieve the nice name for

    Returns
    -------
    str
        The nice name of the carrier or the carrier index if no nice name is available
    """
    return title_except_multi_caps(
        n.carriers.nice_name.where(n.carriers.nice_name.ne(""), n.carriers.index.to_series()).at[carrier]
    )


def apply_carrier_colors(fig: go.Figure, n: pypsa.Network) -> None:
    """Color each bar by its carrier, in place.

    PyPSA drops the color mapping for bar charts when ``color`` equals the
    categorical axis (it treats it as redundant), so the explorer's
    ``y="carrier", color="carrier"`` bars render in a single default color.
    This reapplies the network's carrier colors per bar, matching the nice-name
    labels PyPSA puts on the axis.
    """
    raw_colors = ChartGenerator(n).get_carrier_colors(nice_names=True)
    color_map = {sanitize_mathtext(label): color for label, color in raw_colors.items()}

    for trace in fig.data:
        if trace.type != "bar":
            continue
        categories = trace.y if trace.orientation == "h" else trace.x
        if categories is None:
            continue
        trace.marker.color = [color_map.get(category, "#AAAAAA") for category in categories]


def convert_latex_to_html(text: str) -> html.Span:
    """
    Convert LaTeX-style subscripts to HTML.

    Parameters
    ----------
    text : str
        Text that may contain LaTeX subscript notation like H$_2$

    Returns
    -------
    html.Span
        A Dash HTML component with proper subscript formatting
    """
    # Pattern to match LaTeX subscripts like $_2$ or $_{2}$
    pattern = r"\$_\{?([^$}]+)\}?\$"

    # Split the text by the pattern
    parts = re.split(pattern, text)

    # Build the HTML elements
    elements = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Regular text
            if part:
                elements.append(part)
        else:
            # Subscript text
            elements.append(html.Sub(part))

    return html.Span(elements)


def get_bus_carrier_options(n: pypsa.Network) -> list[dict[str, Any]]:
    """
    Get the bus carrier options for dropdown/checklist components.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object

    Returns
    -------
    list[dict[str, Any]]
        List of options with label and value for each carrier
    """
    return [
        {
            "label": html.Span([" ", convert_latex_to_html(get_carrier_nice_name(n, carrier))]),  # type: ignore[list-item]
            "value": carrier,
        }
        for carrier in sorted(n.buses.carrier.unique())
        if carrier != "none"
    ]


def get_country_options(n: pypsa.Network) -> list[dict[str, str]]:
    """
    Get the country options for dropdown components.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object

    Returns
    -------
    list[dict[str, str]]
        Sorted list of country options with label and value
    """
    options = [{"label": country, "value": country} for country in n.buses.country.unique()]
    return sorted(options, key=lambda x: x["label"])


def get_country_filter(country_mode: str, selected_countries: list[str]) -> tuple[str | None, str | None, html.Div | None]:
    """
    Determine the query string and facet column based on country selection.

    Parameters
    ----------
    country_mode : str
        Either "All" or "Specific" to indicate filtering mode
    selected_countries : list[str]
        List of selected country codes

    Returns
    -------
    tuple
        (query, facet_col, error_message_component | None)
    """
    from pypsa_explorer.layouts.components import PLEASE_SELECT_COUNTRY_MSG

    if country_mode == "Specific":
        if not selected_countries:
            return None, None, PLEASE_SELECT_COUNTRY_MSG
        else:
            formatted_countries = [f"'{c}'" for c in selected_countries]
            query = f"country in [{', '.join(formatted_countries)}]"
            return query, "country", None
    # Default is "All" countries
    return None, None, None


def summarize_network(n: pypsa.Network) -> dict[str, int | str]:
    """Summarize basic counts for a PyPSA network."""

    return {
        "buses": len(getattr(n, "buses", [])),
        "links": len(getattr(n, "links", [])),
        "lines": len(getattr(n, "lines", [])),
    }


def resolve_default_network_path(default_path: str | None = "demo-network.nc") -> Path | None:
    """Locate the bundled demo network if available."""

    if not default_path:
        return None

    candidate = Path(default_path)
    search_paths = [candidate]

    if not candidate.is_absolute():
        file_parents = Path(__file__).resolve().parents
        base_paths = []
        if len(file_parents) > 3:
            base_paths.append(file_parents[3])  # repository root when running from source
        if len(file_parents) > 1:
            base_paths.append(file_parents[1])  # package directory when installed
        base_paths.append(Path.cwd())
        search_paths.extend(base / default_path for base in base_paths)

    for path in search_paths:
        if path.is_file():
            return path

    with suppress(Exception):
        from importlib import resources

        resource = resources.files("pypsa_explorer") / default_path
        if resource.is_file():
            with resources.as_file(resource) as tmp_path:
                return Path(tmp_path)

    return None
