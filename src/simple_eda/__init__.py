"""simple_eda: a tiny pandas-based exploratory data analysis toolkit."""

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

__all__ = [
    "load_csv",
    "shape_summary",
    "dtype_summary",
    "missing_summary",
    "numeric_summary",
    "categorical_summary",
    "correlation_matrix",
    "quick_report",
]

__version__ = "0.1.0"
