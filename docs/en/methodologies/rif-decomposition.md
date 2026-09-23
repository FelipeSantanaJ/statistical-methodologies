# RIF (Recentered Influence Function) decomposition

## 1. What problem does this solve?

Oaxaca-Blinder decomposition splits the difference in means between two
groups into an explained and an unexplained part — but what if the gap
between the groups isn't the same everywhere in the distribution? What if
the gap is small among low earners but large among high earners (or the
other way around)? RIF decomposition answers that question by extending the
Oaxaca-Blinder logic beyond the mean.

## 2. Intuition

The mean is just one of several possible summaries of a distribution. Other
summaries — the median, the 10th percentile, the 90th percentile — can also
be compared between groups and decomposed into "how much comes from
differences in characteristics" and "how much is left over." The technical
challenge is that these other summaries (called distributional statistics)
aren't simple averages of observed variables, so the regression machinery
used in Oaxaca-Blinder doesn't apply to them directly. The recentered
influence function is what solves that problem: it transforms each
observation into a measure of "how much it influences" that specific summary
of the distribution, in a way such that the average of this transformed
measure recovers the summary itself — and once transformed, the
Oaxaca-Blinder logic works again.

## 3. Plain-language explanation

An influence function measures, for a statistic of interest (the median,
say), how much that statistic would change if one specific observation were
slightly perturbed. The "recentered" version is adjusted so that the average
of the influence function, computed over the whole sample, equals exactly
the original value of the statistic. That's what lets you treat this
transformed measure as if it were an ordinary variable and apply regression
and Oaxaca-Blinder decomposition on top of it — except now you're decomposing
the difference in the statistic of interest (median, 90th percentile, etc.)
instead of the difference in means of the original variable.

![Estimated unexplained gap at different percentiles of the distribution, showing the gap is larger at the tails](../../../assets/figures/rif-decomposition-gap-por-quantil-en.png)

## 4. Easy conceptual example

Imagine the wage gap between two groups, looking only at the mean, is 15%.
RIF decomposition might reveal that at the 10th percentile (among lower
earners), the gap is 28%, while at the 50th percentile (the median) it drops
to 15%, and climbs back up to 26% at the 90th percentile (among higher
earners). That pattern — a larger gap at the tails of the distribution than
in the middle — is common enough to have its own names in the literature:
"sticky floor" (when the gap is larger at the bottom) and "glass ceiling"
(when the gap is larger at the top).

## 5. How it works, broadly

1. Choose the distributional statistic of interest (median, a specific
   percentile, the Gini index, etc.).
2. Compute the recentered influence function of that statistic for every
   observation in the sample.
3. Use that transformed measure as the outcome variable in a regression,
   separately for each group — exactly as in the first step of
   Oaxaca-Blinder, but with the transformed variable in place of the
   original one.
4. Apply the same counterfactual decomposition logic from Oaxaca-Blinder on
   top of that regression, obtaining explained and unexplained components
   for that specific point of the distribution.
5. Repeat across several points of the distribution (several percentiles,
   say) to build a full profile of the gap across the distribution.

## 6. What the result means

For each chosen point of the distribution, the result shows how much of the
gap at that point comes from differences in characteristics and how much is
left over — just like Oaxaca-Blinder, but point by point instead of only at
the mean. Looking at several points together shows whether the gap is
uniform across the distribution or concentrated in certain regions.

## 7. How to interpret it

Just as in Oaxaca-Blinder, the unexplained component at each point shouldn't
automatically be read as discrimination — the same caveat about omitted
variables applies, point by point. Precision of the estimate also tends to
vary across the distribution: points at the tails (very low or very high
percentiles) typically have fewer nearby observations and wider margins of
error — results there deserve a more cautious reading.

## 8. When it's useful

When the question isn't just "is there an average gap?" but "is that gap the
same at every level of the distribution, or is it concentrated in certain
ranges?" A typical use: applying this technique to show that a residual gap
between demographic groups in an income distribution is larger both among
low earners and among high earners, and comparatively smaller in the middle
of the distribution.

## 9. Important caveats

- Larger standard errors at the tails of the distribution demand extra
  caution when interpreting differences there.
- The choice of which points of the distribution to report (just the
  median? a full grid of percentiles?) shapes the narrative — it's worth
  reporting a representative set, not just the most "convenient" point for a
  given story.
- Just as with Oaxaca-Blinder, the decomposition is an accounting exercise,
  not a causal one.

## 10. A small worked example

Suppose, in a hypothetical scenario, the unexplained (residual) wage gap
between two groups, estimated at five percentiles of the distribution:

| Percentile | Unexplained gap |
|------------|------------------|
| P10        | 28%              |
| P25        | 19%              |
| P50        | 15%              |
| P75        | 18%              |
| P90        | 26%              |

The U-shaped pattern — larger at the tails, smaller in the middle — suggests
that even comparing people with similar characteristics, the gap isn't
constant across the distribution: it's more pronounced both at the bottom
and at the top of the wage distribution than in the middle range.

## 11. Simple code example

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import gaussian_kde

def rif_quantile(y, q):
    """Recentered influence function for quantile q (0 to 1)."""
    quantile_value = np.quantile(y, q)
    density = gaussian_kde(y)(quantile_value)[0]
    indicator = (y <= quantile_value).astype(float)
    return quantile_value + (q - indicator) / density

df_a = pd.DataFrame({"wage": [...], "education": [...]})  # Group A
df_b = pd.DataFrame({"wage": [...], "education": [...]})  # Group B

df_a["rif_median"] = rif_quantile(df_a["wage"].values, 0.5)
df_b["rif_median"] = rif_quantile(df_b["wage"].values, 0.5)

model_a = smf.ols("rif_median ~ education", data=df_a).fit()
model_b = smf.ols("rif_median ~ education", data=df_b).fit()
# from here, the decomposition follows the same steps as Oaxaca-Blinder
```

In practice, dedicated packages (like `rifreg` in R/Stata) handle the
details of density estimation and standard-error calculation, which need
more care than the simplified version above.
