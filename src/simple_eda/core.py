"""Core EDA functions for simple_eda, built on top of pandas."""

import os

import pandas as pd


def load_csv(path):
    """Load a CSV file into a DataFrame, raising a clear error if it's missing."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path)


def shape_summary(df):
    """Return a dict with row count, column count, and column names."""
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
    }


def dtype_summary(df):
    """Return a dict mapping each column name to its dtype as a string."""
    return {col: str(dtype) for col, dtype in df.dtypes.items()}


def missing_summary(df):
    """Return a DataFrame of missing count and missing % per column, sorted descending."""
    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df) * 100) if len(df) else missing_count * 0.0
    summary = pd.DataFrame(
        {"missing_count": missing_count, "missing_pct": missing_pct}
    )
    return summary.sort_values("missing_count", ascending=False)


def numeric_summary(df):
    """Return describe() for numeric columns only; empty DataFrame if none."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.describe()


def categorical_summary(df, top_n=5):
    """For each non-numeric column, return unique value count and top_n most frequent values."""
    categorical_df = df.select_dtypes(exclude="number")
    result = {}
    for col in categorical_df.columns:
        value_counts = categorical_df[col].value_counts().head(top_n)
        result[col] = {
            "unique_values": categorical_df[col].nunique(),
            "top_values": value_counts.to_dict(),
        }
    return result


def correlation_matrix(df):
    """Return Pearson correlations for numeric columns; empty if fewer than 2 numeric cols."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr()


def quick_report(df):
    """Return a human-readable multi-line string summarizing the DataFrame."""
    lines = []

    shape = shape_summary(df)
    lines.append("=== Shape ===")
    lines.append(f"Rows: {shape['rows']}, Columns: {shape['columns']}")
    lines.append(f"Column names: {shape['column_names']}")

    lines.append("\n=== Dtypes ===")
    for col, dtype in dtype_summary(df).items():
        lines.append(f"{col}: {dtype}")

    lines.append("\n=== Missing Values ===")
    lines.append(missing_summary(df).to_string())

    lines.append("\n=== Numeric Summary ===")
    num_summary = numeric_summary(df)
    lines.append(num_summary.to_string() if not num_summary.empty else "No numeric columns.")

    lines.append("\n=== Categorical Summary ===")
    cat_summary = categorical_summary(df)
    if cat_summary:
        for col, info in cat_summary.items():
            lines.append(f"{col}: {info['unique_values']} unique values")
            lines.append(f"  Top values: {info['top_values']}")
    else:
        lines.append("No categorical columns.")

    lines.append("\n=== Correlation Matrix ===")
    corr = correlation_matrix(df)
    lines.append(corr.to_string() if not corr.empty else "Fewer than 2 numeric columns.")

    return "\n".join(lines)
