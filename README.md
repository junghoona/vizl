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

## Plotting

As of 0.2.0, `simple-eda` also depends on `matplotlib` and ships an
on-brand plotting layer — reinstall with `pip install -e .` to pull in
the new dependency.

```python
import os
import simple_eda as se

os.makedirs("src/output", exist_ok=True)

df = se.load_csv("data.csv")
fig, ax = se.bar_plot(df, "category", "value")
fig.savefig("src/output/out.png", dpi=150)
```

Available plot functions: `theme`, `line_plot`, `area_plot`, `bar_plot`, `hbar_plot`, `donut_plot`, `gauge_plot`.

### Smoke-testing the plots

After installing, run this to generate one of each chart from a tiny sample
DataFrame and confirm the theme is applied (dark indigo background, coral/
periwinkle gradients):

```python
import os
import pandas as pd
import simple_eda as se

out = "src/output"
os.makedirs(out, exist_ok=True)

ts = pd.DataFrame({"month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                    "revenue": [12, 18, 15, 22, 30, 27],
                    "cost": [8, 10, 11, 14, 16, 15]})
cat = pd.DataFrame({"category": ["A", "B", "C", "D"], "value": [42, 27, 63, 35]})

se.line_plot(ts, "month", ["revenue", "cost"])[0].savefig(f"{out}/line.png", dpi=150)
se.area_plot(ts, "month", "revenue")[0].savefig(f"{out}/area.png", dpi=150)
se.bar_plot(cat, "category", "value")[0].savefig(f"{out}/bar.png", dpi=150)
se.hbar_plot(cat, "category", "value")[0].savefig(f"{out}/hbar.png", dpi=150)
se.donut_plot(75, label="Completion")[0].savefig(f"{out}/donut.png", dpi=150)
se.gauge_plot(80, label="Score")[0].savefig(f"{out}/gauge.png", dpi=150)
```

Open the saved PNGs in `src/output/` and check each has a `#2E1F4E`
background with coral (warm) and periwinkle (cool) gradients — no pure
black or default Matplotlib colors should appear anywhere.

## Note on the package name

The distribution name `simple-eda` may already be taken on PyPI. If you plan
to publish this package, check availability first and rename it (in
`pyproject.toml`) if necessary.
