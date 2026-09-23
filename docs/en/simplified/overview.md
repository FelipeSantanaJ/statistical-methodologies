# Overview — every methodology, in plain language

This document explains, without formulas and without unnecessary jargon, every
statistical methodology used across the portfolio. The goal is simple: you
don't need a statistics background to understand **what question each method
answers** and **what it lets you conclude** — and, just as important, **what it
doesn't**.

Each section follows the same shape: a concrete question, the idea behind the
method, what the result means, and one important limit.

For a more detailed explanation of any of these methods, see
[`methodologies/`](../methodologies/) (intermediate level) or
[`complete/`](../complete/) (full technical level).

---

## 1. Welch's t-test

**The question:** two groups have different average values in a sample. Is that
difference probably real, or could it just as easily have come from the random
variation of who happened to end up in each sample?

**The idea:** if you repeatedly drew small samples from two populations that
actually had the same mean, the sample means would still almost never come out
identical. The test measures how unusual the observed difference is, given the
sample sizes and the spread within each group — without requiring the two
groups to have the same internal variability, which makes it safer than the
classic (Student's) version when the groups differ in size or spread.

**What the result means:** a low p-value says a difference this large would be
rare if the population means were actually equal. That's evidence in favor of
a real difference — not proof that it's large or practically important.

**What it doesn't tell you:** why the difference exists, or whether it's caused
by anything in particular.

---

## 2. Oaxaca-Blinder decomposition

**The question:** two groups earn different average wages. How much of that
comes from the groups having, on average, different characteristics (years of
education, say), and how much is left over even after accounting for those?

**The idea:** the method fits a statistical model relating wages to observable
characteristics separately for each group, then asks: "if Group B had Group
A's characteristics but kept being paid according to its own wage structure,
what gap would we expect?" That splits the gap into an **explained** part
(difference in characteristics) and an **unexplained** part (what's left
over).

**What the result means:** the unexplained part is whatever can't be
attributed to the measured characteristics. It's often read as a possible
signal of discrimination — but that conclusion needs much stronger assumptions
than the method alone provides: there may be relevant characteristics that
simply weren't measured.

**What it doesn't tell you:** the method doesn't prove causation or isolate
discrimination — it decomposes an observed difference, it doesn't explain its
causal origin.

---

## 3. RIF (Recentered Influence Function) decomposition

**The question:** Oaxaca-Blinder decomposes the difference in **means**. What
if the gap between groups isn't the same everywhere in the distribution — what
if it's larger among low earners, or among high earners?

**The idea:** instead of looking only at the mean, the method lets you
decompose the gap at any point of the distribution — the median, say, or the
90th percentile. It does this by transforming each observation into a measure
of "how much it contributes" to that specific point of the distribution, then
applies the same Oaxaca-Blinder logic on top of that transformed measure.

**What the result means:** it reveals patterns the mean hides — a small gap in
the middle of the distribution but a large one at the tails, for example.

**What it doesn't tell you:** each point of the distribution is estimated with
its own margin of error, usually wider at the tails (where there's less data)
— results there deserve more caution.

---

## 4. Inequality decomposition (Theil, Gini, weighted quantiles)

**The question:** how much of the total inequality in a variable (income, say)
comes from differences **between** groups, and how much from differences
**within** each group?

**The idea:** the Theil index has a useful mathematical property called exact
decomposability: total inequality can be split, with no leftover, into a
"between-groups" share and a "within-groups" share. The Gini index measures
concentration within a group (how far that group is from a perfectly equal
distribution). Weighted quantiles estimate, within each group, cutoffs like
"what defines the richest 10% of that group."

**What the result means:** it's common, in broad demographic splits like race
or gender, for most of the total inequality to sit within each group — that
doesn't diminish the importance of a between-group gap that's large and
statistically significant; it just shows inequality has several sources at
once.

**What it doesn't tell you:** a lower Gini in one group doesn't necessarily
mean a "better situation" — it can simply reflect a distribution more
compressed near the bottom.

---

## 5. Duncan dissimilarity index

**The question:** are two groups distributed similarly across different
categories (occupations, say), or is one group concentrated in certain
categories while the other sits in different ones?

**The idea:** the index essentially measures what fraction of one group would
need to "switch categories" for the two distributions to become identical. A
value of zero means identical distributions; a value of one (or 100%) means
complete segregation.

**What the result means:** a high index indicates the groups rarely occupy the
same categories — a signal of occupational segregation, for instance.

**What it doesn't tell you:** the index doesn't say why the segregation
exists, nor does it distinguish voluntary concentration from access barriers
or differences in qualifications.

---

## 6. Structural break test

**The question:** did a series over time change pattern at a specific, known
moment — an event, a law, a crisis?

**The idea:** the method compares the series' behavior before and after a
pre-defined date, testing whether the two pieces look like they come from the
same process or from different ones.

**What the result means:** a significant break is evidence that something
changed at that moment — but if several events happened close together (a
pandemic near a labor reform, say), the test alone can't say which one caused
the change.

**What it doesn't tell you:** this is evidence of temporal correlation, not
causation — and a test that looks at one pre-defined date is not a search for
unknown breaks anywhere in the series.

---

## 7. Difference-in-differences

**The question:** did a policy or event have a causal effect on an affected
group, compared to an unaffected one?

**The idea:** compares the change over time in the affected group with the
change over time in the unaffected group. If the two groups were already
following similar trajectories before the event (so-called "parallel trends"),
the difference in changes can be attributed to the event. Placebo tests apply
the same logic to fake dates — if an "effect" shows up even on a date with no
real policy change, that's a warning sign.

**What the result means:** when parallel trends hold and the design is well
executed, the method supports a causal reading — stronger than a simple
before/after comparison.

**What it doesn't tell you:** "we didn't find an effect" isn't the same as
"there is no effect" — a design with few data points, or a small sample, may
simply lack the statistical power to detect a real effect.

---

## 8. Panel transition analysis

**The question:** do people in one group leave unemployment, or enter formal
work, faster or slower than people in another group?

**The idea:** some household surveys interview the same person more than once
over time. That makes it possible to track real individual transitions
(unemployed → employed, say), instead of only comparing isolated snapshots of
different moments.

**What the result means:** different transition rates between groups show real
differences in mobility, not just differences in composition at a single
moment.

**What it doesn't tell you:** matching the same person across interviews can
fail (a household member changing, for instance) — the match success rate
matters for how much you can trust the result.

---

## 9. A/B testing

**The question:** does a specific change (to a product, a process) actually
improve the outcome that matters, or does the apparent improvement come from
noise?

**The idea:** a group of people is randomly split in two — half see the new
version, half stay on the old one — and the average outcome is compared
between the two groups, with a significance test and a confidence interval
around the estimated effect.

**What the result means:** because the split is random, a significant
difference between the groups can be attributed to the change being tested,
not to other differences between the people.

**What it doesn't tell you:** this only holds if the randomization actually
worked — hence the importance of always checking that before trusting the
result (see the next item).

---

## 10. Sample Ratio Mismatch (SRM) test

**The question:** did the split between the experiment's groups actually come
out as planned?

**The idea:** if you planned a 50/50 split but a bug put 55% of people in one
group and 45% in the other, that's a sign something broke in the
randomization — and any effect measured after that point can't be trusted.

**What the result means:** a significant SRM is an alarm: stop and investigate
before interpreting any result from the experiment.

**What it doesn't tell you:** the test detects that the ratio is wrong, it
doesn't automatically say why — that requires separate investigation.

---

## 11. Balance checks and covariate adjustment

**The question:** were the two experiment groups actually similar before the
change was applied?

**The idea:** characteristics that already existed before the experiment (age,
usage history, say) are compared between the two groups. If they look similar,
the randomization worked. Those same characteristics can also be used to
"clean up" some of the noise in the effect estimate, making it more precise.

**What the result means:** balanced groups give more confidence that any
difference in outcome came from the change being tested, not from a
pre-existing difference between the groups.

**What it doesn't tell you:** balance on the measured characteristics doesn't
guarantee balance on unmeasured ones.

---

## 12. Non-inferiority test

**The question:** did a safety or risk metric (fraud rate, say) not get worse
beyond an acceptable limit?

**The idea:** unlike an ordinary test, which asks "is there any difference?",
this one asks only "did this metric not get worse than X?" — in a single
direction.

**What the result means:** when the test passes, there's evidence the metric
stayed within the acceptable range. When it doesn't pass, that doesn't
necessarily mean the metric got much worse — it means there isn't enough
evidence that it stayed within the agreed margin.

**What it doesn't tell you:** choosing the acceptable margin is a business
decision, not a statistical one — the test doesn't say which margin is
"right."

---

## 13. Heterogeneity (interaction) testing and novelty-effect decay

**The question:** is the effect of a change the same for everyone, or larger
for some subgroups? And does the effect hold over time, or is it just a
"novelty effect" that fades?

**The idea:** a formal interaction test checks whether the difference in
effect between subgroups is large enough not to be just sampling noise.
Looking at the effect across the weeks after launch shows whether it decays.

**What the result means:** finding an effect concentrated in one specific
subgroup changes the practical decision — you might roll out only to that
subgroup, instead of to everyone.

**What it doesn't tell you:** testing many subgroups raises the chance of
finding a "significant" difference by chance alone — an isolated
heterogeneity result deserves more caution than one confirmed by several
pieces of evidence.

---

## 14. Cluster-robust standard errors

**The question:** what if observations within the same group (a store, a
region, a survey sampling unit) aren't actually independent of each other?

**The idea:** the ordinary standard-error calculation assumes each observation
is independent. When several observations come from the same cluster and look
similar to one another, treating them all as independent makes the standard
error look smaller than it really is. The cluster adjustment corrects for
that.

**What the result means:** with the adjustment, the confidence interval comes
out wider (and more honest) than it would without it.

**What it doesn't tell you:** with very few clusters, even the adjusted
standard error can be unreliable — that's where alternative methods (items 15
and 16) come in.

---

## 15. Randomization inference

**The question:** with very few groups in the experiment (few stores, few
regions), how do you trust a p-value computed the traditional way?

**The idea:** instead of assuming a theoretical formula, the method reshuffles
the treatment/control assignment across groups in all possible ways (or many
of them), computing the effect under each reshuffling. The p-value comes from
comparing the observed effect to this distribution of "what if the assignment
had been different" effects.

**What the result means:** it's a form of inference that doesn't depend on
assumptions about the data's distribution — only on the randomness of the
assignment itself.

**What it doesn't tell you:** it requires that the treatment assignment
actually was random.

---

## 16. Wild-cluster bootstrap

**The question:** another way to get reliable inference with few clusters.

**The idea:** instead of resampling whole clusters (which works poorly when
there are few of them), the method resamples the model's residuals,
multiplying them by random signs (+1 or -1) per cluster, and rebuilds the test
statistic many times to form a reference distribution.

**What the result means:** it tends to agree with randomization inference when
both are applicable — using more than one method and seeing whether they
agree is a way of checking how robust a conclusion is.

**What it doesn't tell you:** it still relies on some assumptions about the
fitted model, even though it's more robust than the classic formula.

---

## 17. Statistical power and Minimum Detectable Effect (MDE)

**The question:** before running an experiment, what's the smallest effect it
actually has a real chance of detecting?

**The idea:** it depends on the sample size, the metric's variability, and the
desired confidence level. Calculating this beforehand avoids running an
expensive experiment that was never going to be able to see an effect of the
size that matters.

**What the result means:** a high MDE (relative to the effect you'd
realistically expect) is a sign that the experiment, as designed, likely won't
give a useful answer.

**What it doesn't tell you:** not detecting an effect in an experiment with a
high MDE doesn't mean there's no effect — only that the design didn't have the
power to see one.

---

## 18. Spatial spillover (cannibalization)

**The question:** is the positive effect measured in a treated area real
gain, or is it activity "stolen" from neighboring control areas?

**The idea:** control areas near treated areas are compared with control areas
farther away — if the nearby ones perform worse, that suggests part of the
apparent "effect" is just displacement, not net creation.

**What the result means:** it helps estimate the real net effect of an
intervention, not just its apparent local effect.

**What it doesn't tell you:** fully isolating spillover is hard — the method
gives an approximate estimate, not an exact measurement.

---

## 19. Cohort / retention decomposition

**The question:** why did an aggregate metric suddenly change — what
specifically is driving it?

**The idea:** instead of looking only at the aggregate number, the base is
split into subgroups (entry cohorts, segments, channels) and compared to see
how each one contributed to the change — often revealing that several
overlapping causes, not just one, explain the total.

**What the result means:** it lets you act on the specific cause, instead of
reacting to the aggregate symptom.

**What it doesn't tell you:** the decomposition is descriptive — showing that
a subgroup "contributed more" doesn't by itself prove it was the root cause
without further investigation.

---

## 20. Growth decomposition

**The question:** did a business's growth come from expanding into new
places/products, or from real improvement in what already existed?

**The idea:** total growth is split into an expansion part (new markets, new
stores) and a "comparable" part (growth in what already existed long enough
for a fair comparison) — and then, within the comparable part, split further
into how much came from price, how much from volume, and how much from a
change in the mix of products sold.

**What the result means:** an impressive total-growth number can hide a
mature base that's stagnant or even shrinking.

**What it doesn't tell you:** the decomposition doesn't say whether the
expansion strategy was a good call — it only separates where the total number
came from.

---

## 21. Poisson regression (counts, with fixed effects)

**The question:** what explains how many goals a team scores — its own attack
strength, the opponent's defense strength, and whether it's playing at home or
away?

**The idea:** for count variables (number of events, like goals), Poisson
regression models that count as a function of explanatory factors. Fixed
effects per team capture each team's specific strength, isolating the effect
of interest (playing at home, say).

**What the result means:** the coefficient for the factor of interest, once
properly transformed, becomes a multiplicative factor — "playing at home
multiplies the expected number of goals by X," already net of the strength of
both teams involved.

**What it doesn't tell you:** the model assumes a specific relationship
between the factors and the expected count — it's worth checking whether that
assumption is reasonable for the data at hand.

---

## 22. Weighted least squares trend

**The question:** is a metric rising, falling, or stable over time, for each
unit being compared (a team, a club, a region)?

**The idea:** a straight line is fit to the data over time, giving more weight
to periods with more observations (more reliable ones). Instead of deciding
"rising or falling" just by looking at whether the slope is positive or
negative, the slope's confidence interval is examined: if the whole interval
is positive, the trend is rising; if entirely negative, it's falling; if it
crosses zero, it's classified as stable (not enough evidence of a trend).

**What the result means:** this classification avoids declaring a "trend" on
top of noise — it requires the evidence to be strong enough to rule out the
stable hypothesis.

**What it doesn't tell you:** with few time periods, the confidence interval
tends to be wide, and most units end up classified as "stable" simply for
lack of enough data to decide — that's not the same as saying they truly don't
change.

---

## 23. Logistic regression

**The question:** given the value of one or more variables, what's the
probability that a binary outcome happens — a customer cancels, a team gets
relegated, a patient responds to a treatment?

**The idea:** instead of predicting a number between 0 and 1 directly (which
an ordinary linear regression doesn't guarantee), logistic regression models
the log odds of the outcome as a linear combination of the explanatory
variables. That transformation guarantees the predicted probability, once
converted back, always stays between 0 and 1 — the result is an S-shaped
curve, flat at the extremes and steeper in the middle.

**What the result means:** each variable's coefficient, properly transformed,
becomes an odds ratio — "each extra point on this variable multiplies the
odds of the outcome by X." The model's quality as a classifier is assessed
separately, typically via AUC (how well the model separates who had the
outcome from who didn't) and out-of-sample validation.

**What it doesn't tell you:** when a variable almost perfectly separates the
two classes, the estimate becomes unstable (quasi-separation) — the direction
of the effect still holds, but its confidence interval calls for caution. And
a statistically significant coefficient doesn't by itself guarantee the model
classifies well — those are different questions.
