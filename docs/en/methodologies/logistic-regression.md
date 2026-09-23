# Logistic regression

## 1. What problem does this solve?

An analyst wants to predict whether something happens or not — a customer cancels or not, a team gets relegated or not, a patient responds to treatment or not — from one or more continuous variables. The problem: the outcome is binary (0 or 1), and an ordinary linear regression fit directly to that 0/1 variable can predict values like −0.3 or 1.4, which don't correspond to any real probability.

## 2. Intuition

A probability needs to stay between 0 and 1, always. Logistic regression solves this by modeling, not the probability directly, but a transformation of it — the **log odds** — as a linear combination of the explanatory variables. That linear combination can take any value, from minus to plus infinity; the transformation back (the logistic function, S-shaped) compresses it into the (0, 1) interval, guaranteeing the model's output is always a valid probability.

## 3. Plain explanation

For each combination of explanatory variables, the model estimates the probability that the outcome equals 1. The curve relating the linear combination of variables to the probability is S-shaped (sigmoid): near the middle, small changes in the variable shift the predicted probability a lot; at the extremes (near 0 or near 1), the same change has almost no effect — the probability is already near the boundary and can't cross it.

## 4. Simple conceptual example

Think of predicting whether a student passes an exam from how many hours they studied. Someone who studied 0 hours almost certainly fails; someone who studied 20 hours almost certainly passes — at both extremes, one more or fewer hour barely changes the prediction. It's in the middle range (say, between 4 and 8 hours) that an extra hour of study makes the biggest difference to the probability of passing — exactly the region where the S-curve is steepest.

## 5. How it works, broadly

1. For each observation, the model computes a linear combination of the explanatory variables: $z = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots$
2. That combination passes through the logistic function, $p = 1/(1+e^{-z})$, which converts any real number into a probability between 0 and 1.
3. The $\beta$ coefficients are estimated by maximum likelihood — the set of values that makes the observed outcomes (who had 1, who had 0) most probable under the model.
4. To classify a new observation, the predicted probability is compared to a threshold (0.5 by default) — above it, 1 is predicted; below it, 0. The threshold can be adjusted depending on the cost of each type of error.

## 6. What the result means

Each coefficient, exponentiated ($e^{\beta}$), becomes an **odds ratio**: how much the odds of the outcome being 1 gets multiplied by when the variable increases by one unit, holding everything else constant. An odds ratio of 2.0 means the odds double; one of 0.5 means they get cut in half. "Odds" here is the ratio $p/(1-p)$, not the probability $p$ itself — the distinction matters because odds ratios and probabilities don't move in the same proportion.

## 7. How to interpret it

Always translate the raw coefficient (on the log-odds scale) into an odds ratio before communicating it — "the coefficient was 0.69" says nothing on its own, but "each extra point of satisfaction cuts the odds of cancelling in half" ($e^{-0.69}\approx 0.50$) is immediately interpretable. To assess the model's quality as a classifier — not just the significance of its coefficients — two common metrics are **AUC** (area under the ROC curve: the probability the model scores a random positive observation higher than a random negative one; 0.5 is random, 1.0 is perfect separation) and the **Brier score** (mean squared error between predicted probability and observed outcome; lower is better calibrated).

## 8. When is it useful

Whenever the outcome of interest is binary and you want both to **quantify the effect** of each explanatory variable (via the odds ratio) and to **predict a probability** for new cases — not just a 0/1 classification. It's the model of choice for turning a continuous indicator (points pace, satisfaction score, usage time) into an actual chance that a binary outcome occurs.

## 9. Important caveats

- **Quasi-separation**: when a variable almost perfectly separates the two classes (say, everyone above some value has outcome 1 and everyone below has 0), the maximum-likelihood algorithm doesn't converge stably — coefficients and their standard errors become artificially large. This tends to happen precisely when the model is working well, and it doesn't invalidate the direction of the effect, but it calls for caution when interpreting the confidence interval.
- **Correlation between observations**: if several observations come from the same unit (the same customer across different months, the same team across different rounds of a season), treating them as independent artificially inflates the model's confidence. In those cases, validating with a split that respects the group structure (e.g., holding out one whole unit at a time) is more reliable than trusting the in-sample fit alone.
- **Significance isn't accuracy**: a coefficient can be statistically significant (small p-value) while the model still has little power to separate the classes (AUC close to 0.5) — these are different questions.

## 10. A small worked example

Suppose a model with a single variable ($x$ = satisfaction score from 0 to 10) predicting cancellation, with coefficient $\hat\beta = -0.69$ (standard error 0.10) and intercept $\hat\beta_0 = 3.45$. The odds ratio is $e^{-0.69}\approx 0.50$: each extra point of satisfaction cuts the odds of cancelling in half. The point where predicted probability equals 50% sits at $x = -\hat\beta_0/\hat\beta = 5.0$ — below that, the model predicts a higher chance of cancelling than of staying; above it, the reverse.

![Logistic regression: from a continuous variable to a probability](../../../assets/figures/logistic-regression-sigmoid-en.png)

![ROC curve for an illustrative classifier](../../../assets/figures/logistic-regression-roc-auc-en.png)

## 11. Simple code example

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# one row per customer: satisfaction score and whether they cancelled (1) or not (0)
df = pd.DataFrame({
    "satisfaction": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "cancelled":    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
})

X = sm.add_constant(df["satisfaction"])
model = sm.Logit(df["cancelled"], X).fit()
print(model.summary())

# odds ratio for each extra point of satisfaction
print(f"Odds ratio: {np.exp(model.params['satisfaction']):.2f}")

# predicted probability for a customer with satisfaction = 6
print(model.predict([1, 6]))
```
