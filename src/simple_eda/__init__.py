"""simple_eda: a tiny pandas + matplotlib exploratory data analysis toolkit."""

from .core import (
    categorical_summary,
    correlation_matrix,
    dtype_summary,
    load_csv,
    missing_summary,
    numeric_summary,
    quick_report,
    shape_summary,
)
from .plots import (
    area_plot,
    bar_plot,
    donut_plot,
    gauge_plot,
    hbar_plot,
    line_plot,
    theme,
)

__all__ = [
    "load_csv",
    "shape_summary",
    "dtype_summary",
    "missing_summary",
    "numeric_summary",
    "categorical_summary",
    "correlation_matrix",
    "quick_report",
    "theme",
    "line_plot",
    "area_plot",
    "bar_plot",
    "hbar_plot",
    "donut_plot",
    "gauge_plot",
]

__version__ = "0.2.0"
