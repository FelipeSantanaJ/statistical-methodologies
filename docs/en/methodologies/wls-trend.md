# Weighted least squares (WLS) trend with confidence-interval classification

## 1. What problem does this solve?

An analyst wants to know, for every store in a chain, whether average ticket size is rising, falling, or holding steady over the last several quarters. The problem is that not every quarter has the same number of recorded sales — a quarter with 500 transactions is a far more reliable estimate than one with 20. An ordinary linear regression treats every point as equally trustworthy, letting a single sparse quarter distort the estimated trend just as much as a well-populated one.

## 2. Intuition

Imagine asking two people for a restaurant's average rating: one answered based on 400 reviews, the other based on 3. Intuitively, you trust the first answer more. Weighted least squares (WLS) does exactly that when fitting a trend line: it gives more weight to points backed by more observations, and less weight to points backed by few.

## 3. Plain explanation

The method fits a line (or another simple trend) to the data over time, exactly like an ordinary linear regression — but instead of minimizing the plain sum of squared errors, it minimizes the **weighted** sum of squared errors, using each period's number of observations as the weight. After estimating the line's slope, a confidence interval is computed for that slope, and the trend is classified in a simple, objective way:

- If the slope's confidence interval sits entirely **above zero** → an **upward** trend.
- If it sits entirely **below zero** → a **downward** trend.
- If the interval **includes zero** → a **stable** trend (there isn't enough statistical evidence that the slope differs from zero).

## 4. Simple conceptual example

Two stores record their average ticket size over six quarters. Store A rises consistently, quarter after quarter, with plenty of sales in every period — the estimated slope is clearly positive and the confidence interval doesn't come close to zero: classified as "rising." Store B bounces up and down with no clear pattern, with few sales in some quarters — the estimated slope might even be slightly positive, but the confidence interval is wide enough to include zero: classified as "stable," even though the fitted line isn't perfectly flat.

## 5. How it works, broadly

1. For each unit (store, region, category), arrange the metric of interest over time (quarter, month) alongside the number of observations backing each point.
2. Fit a line using weighted least squares, where each point's weight is proportional to its number of observations — points with more data pull the line more toward them.
3. Compute the standard error of the estimated slope, which already accounts for the weighting.
4. Build a confidence interval (typically 95%) for the slope.
5. Classify the trend as rising, falling, or stable, depending on where the confidence interval sits relative to zero.

## 6. What the result means

The estimated slope tells you how much, on average, the metric changes per period. The confidence interval tells you how precise that estimate is — wide intervals (common with few observations, high variability, or few time periods) make it harder to confidently claim a real trend exists, even if the point estimate of the slope looks different from zero.

## 7. How to interpret it

"Stable" in this classification doesn't necessarily mean "no change whatsoever" — it means "there isn't enough statistical evidence, given the observed volume and variability, to tell the slope apart from zero." A store might genuinely be flat, or it might simply lack enough data to detect a real trend that exists but is small. It's important not to conflate the two when communicating the result.

## 8. When it's useful

Whenever you need to classify the trend of many units (stores, players, regions, products) systematically and comparably, especially when the number of observations per period varies substantially across units or over time. This is the logic used in sports analytics to classify whether a club's performance is trending up, down, or holding steady over a season, weighting each period by the number of matches or events observed in that stretch.

## 9. Important caveats

- CI-based classification depends on the chosen confidence level (95% is common but not universal) — a 90% CI classifies more series as "rising" or "falling" than a 99% CI would, for the same data.
- Few time points (say, only three or four periods) make the confidence interval very wide, making any classification other than "stable" hard to reach even when a real trend exists.
- WLS assumes a linear relationship with time; non-linear trends (growth that accelerates or decelerates) can be poorly captured by a single line.
- Weighting by number of observations corrects for unequal sampling precision, but it doesn't fix data-quality issues within a given period (for example, a period with many transactions but a systematic recording error).

## 10. A small worked example

Two stores, twelve quarters each, with observation counts ranging from 40 to 400 per quarter. For Store A, the WLS-estimated slope is +2.4 (metric units per quarter), with a 95% confidence interval between +1.1 and +3.7 — entirely above zero, classified as **rising**. For Store B, the estimated slope is +0.05, with a confidence interval between −1.2 and +1.3 — it crosses zero, classified as **stable**, even though the point estimate is technically positive.

![Weighted trend classification for two stores](../../../assets/figures/wls-trend-classification-en.png)

## 11. Simple code example

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

df = pd.DataFrame({
    "quarter": range(12),
    "avg_ticket": [100, 102, 105, 104, 108, 110, 111, 115, 116, 119, 121, 124],
    "n_observations": [40, 55, 380, 390, 60, 400, 45, 370, 50, 360, 400, 390],
})

X = sm.add_constant(df["quarter"])
model = sm.WLS(df["avg_ticket"], X, weights=df["n_observations"]).fit()

slope = model.params["quarter"]
ci_low, ci_high = model.conf_int(alpha=0.05).loc["quarter"]

if ci_low > 0:
    classification = "rising"
elif ci_high < 0:
    classification = "falling"
else:
    classification = "stable"

print(f"Slope: {slope:.2f} | 95% CI: [{ci_low:.2f}, {ci_high:.2f}] | Classification: {classification}")
```
