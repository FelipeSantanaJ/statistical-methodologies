# Randomization inference (permutation test)

## Concept

Randomization inference (also called a permutation test, or the "Fisher
randomization test," after Ronald Fisher) builds a hypothesis test's
reference distribution directly from the actual randomness of the
experimental design, instead of relying on a theoretical approximation
(such as the normal or t distribution) that is only valid asymptotically,
in large samples.

The central idea is the "sharp" null hypothesis: under $H_0$, each unit's
outcome would be exactly the same regardless of whether it was assigned to
treatment or control. If that is true, the only source of variation in the
observed statistic is the randomness of who was drawn into each group
itself — and that source of variation can be enumerated exactly, because
the researcher knows the assignment mechanism that was used.

## Mathematical formulation

Let there be $N$ experimental units, of which $N_1$ are assigned to
treatment and $N_0 = N - N_1$ to control, according to a known assignment
mechanism. Let $Y_i$ be unit $i$'s observed outcome and $W_i \in \{0,1\}$
the treatment indicator that was actually drawn.

The observed test statistic is typically the mean difference:

$$
\hat\tau_{\text{obs}} = \frac{1}{N_1}\sum_{i: W_i=1} Y_i \; - \; \frac{1}{N_0}\sum_{i: W_i=0} Y_i
$$

Under the sharp null hypothesis $H_0: Y_i(1) = Y_i(0)$ for every unit $i$
(each unit's outcome would be identical under either group), the observed
values $Y_i$ do not depend on $W_i$. That makes it possible to compute the
same statistic under **any** other possible assignment $W'$, holding the
$Y_i$ values fixed:

$$
\hat\tau(W') = \frac{1}{N_1}\sum_{i: W_i'=1} Y_i \; - \; \frac{1}{N_0}\sum_{i: W_i'=0} Y_i
$$

The set of all possible assignments, given the assignment mechanism (for
example, every way of choosing $N_1$ out of $N$ units without replacement),
has $\binom{N}{N_1}$ elements when the design is a simple complete
randomization. The two-sided p-value is:

$$
p = \frac{1}{\binom{N}{N_1}} \sum_{W'} \mathbb{1}\left[ \, |\hat\tau(W')| \geq |\hat\tau_{\text{obs}}| \, \right]
$$

where $\mathbb{1}[\cdot]$ is the indicator function (1 if the condition
holds, 0 otherwise). When $\binom{N}{N_1}$ is too large to enumerate
exhaustively, the sum is approximated by Monte Carlo: a large number $M$
(typically 10,000 or more) of random reassignments $W'$ is drawn, and the
same proportion is computed over that sample, converging to the exact
p-value as $M$ grows.

## Assumptions

- **Genuine randomness of the treatment assignment.** This is the method's
  only fundamental assumption — without it, the reference distribution
  built does not correspond to any real process that generated the data.
- **Sharp null hypothesis.** The classical (Fisher) form of the test checks
  the hypothesis that treatment had absolutely no effect on any unit at
  all — stronger than the usual "average effect equal to zero" hypothesis
  (Neyman's). Rejecting $H_0$ under this design is evidence that treatment
  affected at least some unit, not necessarily all of them equally.
- **No interference between units (SUTVA).** One unit's outcome cannot
  depend on which treatment other units received (no spillovers or
  general-equilibrium effects) — otherwise, the hypothetical reassignment
  $W'$ no longer corresponds to a coherent counterfactual scenario.

## Hypotheses

- $H_0$: sharp null effect — each unit's outcome would be identical
  regardless of which group it was assigned to.
- $H_1$: treatment affects the outcome of at least some units.
- Test statistic: usually the mean difference between groups, but the
  method accepts any statistic of interest (median difference, a model
  coefficient, a ratio of proportions) — the reassignment logic is the same
  regardless of which statistic is chosen.
- P-value: the proportion of possible (or sampled) reassignments that
  produce a statistic as extreme as, or more extreme than, the observed
  one.
- Significance level: conventionally 5%, but subject to the discrete
  granularity of the number of possible reassignments (see limitations).

## Interpretation

A low p-value obtained by randomization is evidence that the actual
assignment produced an unusual result among every possible way the draw
could have gone — a causal reading directly tied to the experiment's own
randomization, without relying on assumptions about the data's population
distribution. That is an important advantage over parametric tests:
validity does not depend on normality, a large sample, or a specific
functional form for the errors.

What the method does not do is automatically generalize the estimated
effect beyond the observed units — the inference is about the observed
assignment versus the other possible assignments within the experiment, not
about a larger population the units were sampled from (that would be a
question of sampling inference, separate from inference about the
assignment).

## Limitations

- **P-value granularity in small samples.** With few units, the number of
  possible reassignments is small, limiting how low a p-value can go — with
  $\binom{4}{2} = 6$ reassignments, the smallest possible p-value is 1/6 ≈
  0.167, even in the face of a large effect. This is a structural
  limitation, not a computational flaw.
- **Depends on genuine randomization.** If treatment assignment was not
  actually random (for example, "volunteer" units self-selected into
  treatment), the built reference distribution does not represent any real
  mechanism — the method loses validity.
- **Computational cost in large designs.** With many units, exhaustive
  enumeration becomes infeasible (the number of combinations grows
  quickly), requiring Monte Carlo approximation — which, in turn,
  introduces a small sampling margin of error into the p-value calculation
  itself, controllable by increasing the number of drawn reassignments.

### Comparison with other methods for inference with few clusters

Randomization inference, cluster-robust standard errors, and wild-cluster
bootstrap all answer the same general problem: reliable inference when
observations are not independent, often because of few clusters or few
randomization units.

- **Cluster-robust standard errors** are the standard starting point, but
  become unreliable precisely in the few-cluster setting, because they
  depend on an asymptotic approximation.
- **Randomization inference** is the most direct alternative when the
  experiment's own assignment mechanism is known and the number of possible
  reassignments is enumerable (or sample-able) — it depends on no
  distributional assumption at all, only on the genuine randomness of the
  assignment. It is especially attractive when the experimental design is
  simple (for example, a complete random draw among a small number of
  units).
- **Wild-cluster bootstrap** is preferable when the effect of interest
  comes from a more complex regression model (with controls, for example),
  or when there is no simple, known assignment mechanism to reproduce
  exactly through reassignment — wild-cluster bootstrap resamples the
  fitted model's residuals instead of directly reassigning treatment.

In practice, when both are applicable, it is common to run both as a
cross-check: conclusions that agree between randomization inference and
wild-cluster bootstrap give more confidence in the result's robustness than
either one alone.

## Example

A restaurant chain tests a new seasonal menu across 6 locations (simple
draw: 3 treatment, 3 control), measuring average spend per table during the
test week, in dollars: treated locations record 12, 15, and 9; control
locations record 22, 18, and 11.

The observed mean difference is 12.0 − 17.0 = −5.0. There are
$\binom{6}{3} = 20$ possible ways to choose which 3 locations were treated.
Computing the mean difference for each of those 20 combinations gives the
full reference distribution — with no assumption at all about the shape of
the distribution of spend per table.

![Reference distribution formed by all 20 possible reassignments, with the observed difference of −5.0 highlighted](../../../assets/figures/randomization-inference-permutation-distribution-en.png)

Of the 20 combinations, 6 produce a difference as extreme as (or more
extreme than) −5.0 in absolute value, giving a two-sided p-value of
6/20 = 0.30. With only 6 units in the experiment, this result is not
unusual enough to be evidence that the new menu actually changed average
spend per table — even though the observed difference, taken alone, looks
large in percentage terms. The example illustrates the granularity
limitation well: with few units, you need a very large effect for the
observed assignment to genuinely stand out among the few possible
reassignments.
