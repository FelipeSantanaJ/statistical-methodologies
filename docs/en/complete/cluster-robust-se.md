# Cluster-robust standard errors

## Concept

Classical statistical inference (ordinary least squares standard errors, for
example) assumes model errors are independent and identically distributed
across observations. That assumption is violated whenever the data has a
**grouping** structure: observations within the same cluster (store, region,
household, classroom, sampling unit of a survey) share unobserved shocks in
common, which generates within-cluster correlation in the errors.

Ignoring that structure does not bias the point estimate of the coefficient
— the least-squares estimator remains unbiased under the usual assumptions —
but it biases the computed standard error **downward**, because the standard
formula counts every observation as a fully independent unit of information,
when in fact part of the within-cluster variation is repetition, not new
information.

The cluster-robust standard error (also called the "cluster-robust variance
estimator," CRVE) corrects for this by allowing arbitrary correlation within
each cluster and requiring independence only between clusters.

## Mathematical formulation

For a linear model $Y_i = X_i'\beta + \varepsilon_i$, the least-squares
estimator is $\hat\beta = (X'X)^{-1}X'Y$. The classical variance of
$\hat\beta$ assumes $\varepsilon_i$ i.i.d. with variance $\sigma^2$:

$$
\widehat{\text{Var}}(\hat\beta)_{\text{classical}} = \hat\sigma^2 (X'X)^{-1}
$$

The cluster-robust estimator, with $G$ clusters indexed by $g = 1, \dots,
G$, each with covariate matrix $X_g$ and residual vector $\hat u_g = Y_g -
X_g \hat\beta$, takes the "sandwich" form:

$$
\widehat{\text{Var}}(\hat\beta)_{\text{cluster}} = (X'X)^{-1} \left( \sum_{g=1}^{G} X_g' \hat u_g \hat u_g' X_g \right) (X'X)^{-1}
$$

where:

- $X_g' \hat u_g \hat u_g' X_g$ is cluster $g$'s contribution to the central
  term — it lets residuals from observations in the same cluster be
  correlated with each other in an arbitrary way, without imposing a
  specific correlation structure;
- the sum runs cluster by cluster, not observation by observation — that is
  what preserves the internal correlation instead of treating it as
  independent noise;
- $(X'X)^{-1}$ at each end (the "bread" of the sandwich) is the same matrix
  as in the classical estimator.

It is common to apply a finite-sample degrees-of-freedom correction,
multiplying the result by a factor such as:

$$
c = \frac{G}{G-1} \cdot \frac{n-1}{n-k}
$$

with $n$ the total number of observations, $k$ the number of estimated
parameters, and $G$ the number of clusters — this correction helps, but does
not fully resolve, the problematic behavior with few clusters (see
limitations).

## Assumptions

- **Independence across clusters.** The correction is only valid if
  different clusters are genuinely independent of each other — if there is
  also dependence between clusters (for example, a macroeconomic shock
  hitting every region at the same time), the cluster-robust standard error
  still understates the real uncertainty.
- **Sufficiently large number of clusters.** The estimator's asymptotic
  properties rely on $G \to \infty$. In practice, values of $G$ below
  30-40 make the normal approximation to the distribution of $\hat\beta$
  unreliable, even with a large $n$ within each cluster.
- **The clustering variable is correctly specified.** Grouping at too fine a
  level (understating the true correlation) invalidates the correction just
  as much as ignoring the grouping entirely. When in doubt, the cluster
  level should match the level at which the treatment (or the source of
  dependence) actually varies.

## Hypotheses

The CRVE does not introduce a new hypothesis test — it is a method for
computing standard errors, used within the usual tests on regression
coefficients:

- $H_0$: $\beta_j = 0$ (the coefficient of interest is zero in the
  population)
- $H_1$: $\beta_j \neq 0$
- Test statistic: $t = \hat\beta_j / \widehat{SE}_{\text{cluster}}(\hat\beta_j)$,
  compared to the t distribution with $G - 1$ degrees of freedom (a common
  and conservative choice, since the effective amount of information is
  closer to the number of clusters than to the number of observations).
- 95% confidence interval: $\hat\beta_j \pm t_{0.975, \, G-1} \cdot \widehat{SE}_{\text{cluster}}(\hat\beta_j)$.

## Interpretation

The point estimate of the effect does not change when swapping the
classical standard error for the cluster-robust one — only the uncertainty
around it changes. An effect that stops being significant under the
cluster-robust standard error is not "less real" — the estimate is still
the best one available; only the confidence claimed around it was inflated
before the correction.

Worth stressing: the cluster-robust standard error fixes inference, not
causal identification. If the study design has other problems (omitted
variables, selection, lack of randomization), the cluster-robust standard
error does nothing about those — it only guarantees that, given the point
estimate, the stated margin of error is more faithful to the data's
dependence structure.

## Limitations

- **Few clusters.** This is the most-cited limitation in the applied
  literature. With few clusters (a common rule of thumb: below 30-40), the
  CRVE tends to understate the true variance, even with the
  degrees-of-freedom correction, and the test statistic's distribution
  drifts from the assumed t approximation. In that setting, two alternative
  paths, each covered in its own document in this repository, tend to work
  better: **randomization inference**, when the number of possible
  treatment reassignments is small enough to enumerate (or sample)
  directly; and **wild-cluster bootstrap**, which resamples residuals
  multiplied by random signs per cluster and tends to have better
  finite-sample behavior with few clusters than the asymptotic CRVE. As a
  rule of thumb: CRVE is the standard, simplest choice when there are
  enough clusters (dozens or more); with few clusters, prefer wild-cluster
  bootstrap as a more computationally accessible alternative, or
  randomization inference when the design's structure lets you enumerate
  the possible reassignments naturally.
- **Very unequal cluster sizes.** A cluster much larger than the others can
  dominate the sum in the sandwich formula, making the variance estimate
  unstable.
- **Choice of clustering level.** Grouping at too fine a level (understating
  the true correlation) invalidates the correction just as much as ignoring
  the grouping entirely. When in doubt, the cluster level should match the
  level at which the treatment (or the source of dependence) actually
  varies.

## Example

A coffee shop chain tests a new counter layout across 24 locations (12
treatment, 12 control), measuring average customer queue time, with about
150 customer observations per location — 3,600 observations in total.

A simple mean-comparison model, ignoring the cluster structure, estimates an
effect of −1.8 minutes on queue time, with a standard error of 0.25
(treating the 3,600 observations as independent), giving t ≈ −7.2 —
strongly significant.

Recomputing the standard error as cluster-robust, grouping by location (24
clusters), the standard error rises to 0.68 — almost three times larger —
giving t ≈ −2.65. Still significant at the 5% level, but with a
substantially more realistic confidence margin: the 95% interval moves from
roughly [−2.3, −1.3] to [−3.2, −0.4].

The reason for the difference: customers at the same location share the
same barista, the same peak-hour flow, and the same physical queue layout —
factors that make queue times within the same location resemble each other
for reasons that have nothing to do with the new layout. The real
information available is much closer to coming from 24 locations than from
3,600 independent customers.

![Confidence interval computed with the naive standard error compared to the interval with the cluster-robust standard error, same point estimate](../../../assets/figures/cluster-robust-se-ci-comparison-en.png)

With only 24 clusters, still within a reasonable range for the CRVE to work
well, but close enough to the edge that it would be worth confirming the
result with a wild-cluster bootstrap as an additional robustness check.
