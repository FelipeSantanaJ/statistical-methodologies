# Covariate balance and covariate adjustment

*Assumes the A/B testing fundamentals — see [A/B testing fundamentals](./ab-testing.md).*

## 1. What problem does this solve?

An experiment was randomized, but did the two groups actually come out alike
on characteristics that existed before the experiment started — user age,
prior product tenure, historical behavior? And, separately: given that such
pre-experiment characteristics were measured, can they be used to make the
effect estimate more precise, even when the groups are already well
balanced? These are two related but different questions, and they're
commonly conflated.

## 2. Intuition

A balance check is an audit: with groups formed by random assignment,
characteristics that shouldn't have any relationship to the assignment —
because they were measured before the experiment even existed — should be
distributed similarly across groups. If they're very different, that's a red
flag about randomization, not a normal feature of the experimental design.

Covariate adjustment is a different thing: even with perfect randomization,
there's always some user-to-user variation that has nothing to do with the
treatment. If a characteristic measured before the experiment (like last
month's purchase value) helps predict the metric under test, "netting out"
that characteristic from the comparison reduces the estimate's noise —
without biasing the result, because the characteristic was measured before
any treatment effect could exist.

## 3. Plain explanation

For balance: compare, for each covariate of interest, the mean (or
proportion) between the control and treatment groups, typically through the
standardized mean difference — the difference divided by a pooled standard
deviation, which lets you compare covariates on very different scales (age
in years, spend in dollars) on a common ruler.

For adjustment: instead of comparing only the two groups' raw averages, fit
a model that already accounts for these pre-experiment covariates (a
regression, for instance), or use post-stratification — splitting the
sample into strata defined by the covariates and combining the estimates
within each stratum. The result is an estimate of the same effect, but with
a smaller standard error.

![Balance chart (love plot) showing each covariate's standardized difference between groups, with a reference band around zero](../../../assets/figures/covariate-balance-love-plot-en.png)

## 4. A simple conceptual example

A subscription app tests a new pricing policy. Before looking at any
experiment outcome, the team compares average age, prior subscription
tenure, and average spend from the month before the experiment between the
control and treatment groups. All three are close between groups — a sign
that randomization worked. Later, when estimating the pricing policy's
effect on revenue, the team uses last month's spend as an adjustment
covariate, because they know past spend is a good predictor of future
spend — this makes the effect estimate more precise, with a narrower
confidence interval, without changing its meaning.

## 5. How it works, broadly

**Balance (pre-experiment check):**
1. List the relevant covariates, measured before the experiment started
   (never afterward — post-treatment covariates may already have been
   affected by the experiment itself).
2. Compute the standardized mean difference between groups for each
   covariate.
3. Compare each difference to a common reference threshold (0.1 is a
   commonly used value in the literature) — below that, balance is
   considered acceptable.

**Covariate adjustment (variance reduction):**
1. Choose pre-experiment covariates that are good predictors of the metric
   of interest.
2. Fit a model (a simple linear regression, or a technique like CUPED) that
   uses those covariates to explain part of the metric's variation that has
   nothing to do with the treatment.
3. The treatment-effect estimate, after this adjustment, has the same
   interpretation as before, but with reduced standard error.

## 6. What the result means

Acceptable balance across all observed covariates gives more confidence that
the groups were comparable before the experiment started — reinforcing the
causal reading of the effect test. Covariate adjustment, on the other hand,
doesn't change the interpretation of the estimated effect (it's still the
difference caused by the treatment); it only reduces the uncertainty around
that estimate, allowing smaller effects to be detected with the same
sample, or the same precision to be reached with a smaller sample.

## 7. How to interpret it

An imbalance in one covariate doesn't automatically invalidate the
experiment, but it warrants investigation — it might just be a false
positive (with many covariates tested, some will look imbalanced by chance)
or it could signal a real randomization problem, in which case a
complementary Sample Ratio Mismatch test is the natural next step. Good
balance on observed covariates never guarantees balance on unobserved ones —
it's evidence in favor of randomization, not complete proof.

## 8. When it's useful

The balance check should be routine in every randomized experiment, as part
of validating that randomization worked. Covariate adjustment is
especially valuable when the primary metric has high variability across
users (common, for instance, in revenue or engagement metrics) and there's a
pre-experiment covariate strongly correlated with it — in those cases, the
precision gain can be substantial.

## 9. Important caveats

- Never use a covariate measured after the experiment started for
  adjustment or balance checking — it may already have been affected by the
  treatment itself, which introduces bias instead of reducing noise.
- Covariate adjustment doesn't "fix" a real assignment imbalance — it
  reduces variance once randomization has already worked, not a substitute
  for broken randomization.
- Testing balance on dozens of covariates at once raises the odds of
  finding some "imbalanced" one by chance — look at the overall pattern,
  don't react in isolation to a single covariate outside the threshold.
- Which covariates to use for adjustment should be decided before looking
  at the experiment's results, to avoid retroactive selection bias.

## 10. A small worked example

A subscription app runs an experiment with 8,000 users per arm. Comparing
average spend in the month before the experiment: control $42.10 (standard
deviation $18.40), treatment $42.80 (standard deviation $18.90). The
standardized mean difference is:

$$
SMD = \frac{42.80 - 42.10}{\sqrt{(18.40^2 + 18.90^2)/2}} \approx 0.037
$$

Well below the 0.1 reference threshold — acceptable balance. When estimating
the pricing policy's effect on next month's revenue, the simple estimator
(difference in means) produces a 95% CI with a half-width of ±1.05
percentage points around the estimated effect; using last month's spend as
an adjustment covariate, the CI narrows to roughly ±0.62 percentage points —
the same estimated effect, with substantially more precision.

## 11. Simple code example

```python
import numpy as np
import statsmodels.api as sm

# illustrative: y = revenue in the experiment month, treat = 1 if treatment
# prior_spend = pre-experiment covariate (spend in the prior month)
X_adjusted = sm.add_constant(np.column_stack([treat, prior_spend]))
model = sm.OLS(y, X_adjusted).fit(cov_type="HC1")

print(model.summary())
# The 'treat' coefficient is the adjusted effect; its standard error tends
# to be smaller than in a regression without the covariate, when it's
# predictive.
```

The coefficient on the treatment indicator is the adjusted effect estimate;
comparing its standard error to that of a regression without the covariate
directly shows the precision gain achieved.
