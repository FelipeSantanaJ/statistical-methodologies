# Inequality decomposition (Theil, Gini, weighted quantiles)

## 1. What problem does this solve?

When people talk about "income inequality," it's easy to think of it as a
single number — but where does it come from? How much of it is because
different groups (by region, by gender, by any other split) have different
average incomes, and how much is because, within each group, there's already
a lot of variation between low and high earners? This family of tools — the
Theil index, the Gini index, and weighted quantiles — helps answer those
questions.

## 2. Intuition

Think of two sources of inequality that can coexist. First: different groups
can have different average incomes from one another — that's "between-group"
inequality. Second: even within a single group, some people earn much more
than others — that's "within-group" inequality. The Theil index has a
valuable mathematical property: it can split these two components exactly,
with no leftover and no double-counting. The Gini index, on the other hand,
measures income concentration within a single distribution (a group, or the
whole population), on a scale from 0 (perfect equality) to 1 (one individual
has everything, everyone else has nothing). Weighted quantiles are simply
cutoff points — "what defines the richest 10% of this group?" — that use
each observation's sampling weight to correctly estimate those cutoffs in a
survey with a complex sampling design.

## 3. Plain-language explanation

The Theil index computes, essentially, an entropy-based dispersion measure —
the more unequal the distribution, the higher the index. Its property of
exact decomposability lets you write:

$$
\text{Total inequality} = \text{Between-group inequality} + \text{Within-group inequality}
$$

That sum isn't an approximation — the two parts add up to exactly the total.
The Gini index, by contrast, doesn't share this simple form of exact
decomposability — it's computed separately for each group (or for the whole
population), and it's used to compare how concentrated the distribution is
within each slice.

![Stacked bar showing the split of total Theil inequality between the "between-groups" share and the "within-groups" share](../../../assets/figures/inequality-decomposition-theil-en.png)

## 4. Easy conceptual example

Picture a company with two departments. If everyone in Department A earned
exactly the same salary, and everyone in Department B also earned a fixed
salary (just different from A's), all of the company's inequality would come
from the difference between the two salaries — 100% "between groups," 0%
"within groups." In practice, within any real department there's also
salary variation between people — and the Theil index separates exactly how
much of the total inequality comes from each of these two sources.

## 5. How it works, broadly

1. Compute the Theil index for the whole population, a measure of income
   dispersion relative to the mean.
2. Compute the Theil index within each group separately (using only that
   group's observations).
3. The "between-groups" share is computed as if every person within a group
   received their group's average income — it captures only the variation
   between group means.
4. The "within-groups" share is the weighted average (weighted by each
   group's share of total income) of the Theil indices computed within each
   group.
5. The two shares add up to exactly the total Theil index.
6. In parallel, the Gini index is computed within each group to compare
   concentration, and weighted quantiles are estimated within each group
   using each observation's sampling weight.

## 6. What the result means

If the "between-groups" share is small relative to the total, that means
most of the income inequality is spread within each group, not between them
— even if the average difference between groups is large and statistically
significant. The two things don't contradict each other: a between-group gap
can be real and important, and still represent a small fraction of total
inequality, because the inequality within each group is also large.

## 7. How to interpret it

A common mistake is to conclude that "only 7% of the inequality comes from
race, so racial inequality doesn't matter much." That conflates two
different questions: (1) is the average gap between groups large and
significant? and (2) what fraction of total income variance does that gap
explain? The answer to the first question can be "yes, large and
significant" even when the answer to the second is "a small fraction of the
total" — because the inequality within each group, on its own, is already
enormous. Contextualizing the size of the "between-groups" share matters,
but it doesn't cancel out the importance of the gap itself.

Similarly, a lower Gini in one group doesn't necessarily mean a "better
situation" — it can simply reflect a distribution more compressed near the
bottom, meaning everyone in that group earns relatively similarly low
amounts, which is different from "high income, well distributed."

## 8. When it's useful

When you want to contextualize the size of a between-group gap within the
overall picture of inequality — for instance, showing that even though most
income inequality sits within each racial group (not between them), the
between-group gap is still large and statistically robust, and deserves
attention on its own.

## 9. Important caveats

- The "between-groups" share tends to be small when the groups being
  compared are broad and internally heterogeneous (like large demographic
  categories) — that's expected and shouldn't be used to minimize the gap.
- The Theil index requires strictly positive values of the variable of
  interest (it doesn't work directly with zero or negative income without
  adjustments).
- When comparing Gini indices across groups, always check whether the
  underlying distributions are comparable (same unit, same period), and
  remember a lower Gini isn't synonymous with "better."
- Weighted quantiles require the correct use of the survey's sampling
  weights — ignoring the weights produces biased estimates when sampling
  isn't simple random.

## 10. A small worked example

Suppose a hypothetical population split into two groups:

- Group A: average income = 4,000, internal Theil = 0.25.
- Group B: average income = 2,800, internal Theil = 0.30.
- Group A accounts for 40% of the population's total income; Group B, 60%.

The "between-groups" Theil index (computed from the difference in means,
weighted by income share) comes out to about 0.04. The "within-groups" Theil
index is the weighted average of the two internal Theils: 0.4 × 0.25 +
0.6 × 0.30 = 0.28. Adding the two parts, total Theil is about 0.32.

This means the "between-groups" share accounts for roughly 0.04 / 0.32 ≈
12.5% of total inequality — most of it (87.5%) comes from inequality that
already exists within each group, even with a substantial difference in
average income between the groups (4,000 vs. 2,800, a difference of over
40%).

## 11. Simple code example

```python
import numpy as np

def theil_index(income):
    income = np.asarray(income, dtype=float)
    mean = income.mean()
    return np.mean((income / mean) * np.log(income / mean))

def gini_index(income):
    income = np.sort(np.asarray(income, dtype=float))
    n = len(income)
    indices = np.arange(1, n + 1)
    return (2 * np.sum(indices * income) - (n + 1) * np.sum(income)) / (n * np.sum(income))

# illustrative data
group_a = np.array([...])  # individual incomes, Group A
group_b = np.array([...])  # individual incomes, Group B

theil_total = theil_index(np.concatenate([group_a, group_b]))
theil_a = theil_index(group_a)
theil_b = theil_index(group_b)

share_a = group_a.sum() / (group_a.sum() + group_b.sum())
share_b = 1 - share_a

theil_within = share_a * theil_a + share_b * theil_b
theil_between = theil_total - theil_within

p90_a = np.average(np.quantile(group_a, 0.9))  # with sampling weights, use a weighted average
```

For surveys with a complex sampling design (weights, strata, clusters),
libraries like `samplics` in Python, or the `survey` package in R, compute
weighted quantiles and inequality indices correctly, including their
standard errors.
