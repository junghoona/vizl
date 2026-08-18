# simple-eda

A tiny, pandas-based toolkit for quick exploratory data analysis.

## Install

From the project root:

```bash
pip install -e .
```

## Usage

```python
import simple_eda

df = simple_eda.load_csv("data.csv")
print(simple_eda.quick_report(df))
```

## Available functions

`load_csv`, `shape_summary`, `dtype_summary`, `missing_summary`, `numeric_summary`, `categorical_summary`, `correlation_matrix`, `quick_report`

## Note on the package name

The distribution name `simple-eda` may already be taken on PyPI. If you plan
to publish this package, check availability first and rename it (in
`pyproject.toml`) if necessary.
