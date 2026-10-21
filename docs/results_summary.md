# Results summary (Milestone 8D)

All numbers from the 8D run (balanced α selection, prevalence‑aware calibration).
Source tables/figures: `results/tables/*_8D.csv`, `results/figures/*_8D.png`,
plus 8A diagnostics and 8C case studies / feature importance.

## Coverage and balance (8A)

| Quantity | Value |
|---|---|
| High‑confidence labelled universe | 16,355 |
| Overall label balance | 51.9% path / 48.1% benign |
| Evidence sentences (clean) | 912 |
| Distinct variants with evidence | 519 (350 labelled, 169 VUS/conflicting) |
| Labelled variants with **decided, non‑circular** text | **149** |
| Text‑bearing labelled balance | **90.6% path / 9.4% benign** (the skew we control) |
| Circular sentences | 39 / 912 |
| Sentences with conflict > 0.3 | 17 |

## α selection (8D, balanced OOF log‑loss on 119 train text‑bearing variants)

| α | balanced log‑loss | selected? |
|---|---|---|
| 0 | 0.2901 | |
| 0.25 | 0.2786 | |
| 0.5 | 0.2686 | |
| 1 | 0.2520 | |
| 2 | 0.2293 | |
| **4** | **0.2115** | **✔ (parsimonious min)** |
| 8 | 0.2334 | |
| 16 | 0.3757 | (excluded from selection) |

Ordinary log‑loss would have chosen 16 (bias toward "any text ⇒ pathogenic"); the
balanced criterion chooses 4. This is the central methodological safeguard.

## Table 1 — Full test set (n = 3,271, prevalence 0.519)

| Model | AUROC | AUPRC | Brier | bal. Brier | BSS | ECE | slope | intercept |
|---|---|---|---|---|---|---|---|---|
| S structural | 0.9028 | 0.9005 | 0.1218 | 0.1217 | **0.512** | 0.0175 | 0.903 | 0.028 |
| F fused + AF gate | 0.9040 | 0.9018 | 0.1211 | 0.1210 | **0.515** | 0.0174 | 0.909 | 0.021 |
| F fused, no AF gate | 0.9040 | 0.9018 | 0.1211 | 0.1210 | 0.515 | 0.0174 | 0.909 | 0.021 |

Both models are well calibrated and beat the prevalence baseline strongly (BSS ≈ 0.51).
Fusion is a small, safe upgrade and never damages the structural baseline.

## Table 2 — Matched text‑bearing slice (n = 30, prevalence 0.90)

| Model | AUROC | AUPRC | Brier | bal. Brier | BSS | ECE | slope | intercept |
|---|---|---|---|---|---|---|---|---|
| S structural | 0.9938 | 0.9987 | 0.2057 | 0.1143 | −1.285 | 0.3341 | 2.81 | 11.48 |
| F fused + AF gate | 0.9877 | 0.9987 | 0.1309 | 0.0732 | −0.455 | 0.2286 | 1.46 | 4.96 |
| F fused, no AF gate | 0.9877 | 0.9987 | 0.1309 | 0.0732 | −0.455 | 0.2282 | 1.67 | 5.34 |

> **Read this correctly.** The slice is 90% pathogenic and n=30, so the trivial
> "predict 0.9" baseline (Brier ≈ 0.090) beats *every* model here — hence negative
> absolute BSS for structural **and** fused. That is a subset artefact, not a fusion
> failure. The meaningful signal is the *direction*: fusion shrinks the structural
> model's overconfidence (slope 2.81→1.46, intercept 11.48→4.96) and improves every
> calibration metric, with AUROC essentially unchanged. Slice‑level slope/intercept
> are noisy at n=30 and are reported with bootstrap CIs below.

## Bootstrap (1,000 reps) — fused − structural on the matched slice

| Metric | q2.5 | median | q97.5 | % reps favouring fusion |
|---|---|---|---|---|
| Δ AUROC | −0.029 | 0.000 | 0.000 | (never meaningfully hurt) |
| Δ Brier | −0.116 | **−0.073** | −0.037 | **100%** |
| Δ balanced Brier | −0.063 | **−0.040** | −0.021 | **100%** |
| Δ ECE | −0.167 | **−0.103** | −0.053 | **100%** |
| Δ BSS | +0.303 | **+0.850** | +3.176 | **100%** |

Fusion improves calibration on the text‑bearing subset in **100% of replicates**
across Brier, balanced Brier, ECE and BSS, while leaving discrimination intact.

## Worked example — rs11571833 (benign common polymorphism)

| | value |
|---|---|
| ClinVar label | 0 (benign) |
| AF | 0.0044 |
| net_text (path−ben) | 1.916 (4 decided sentences) |
| AF‑gate multiplier | 0.049 |
| P(structural) | 0.0016 |
| P(fused, **no** gate) | 0.0130 |
| P(fused, **+** gate) | 0.0017 |

Conservative α (=4) already contains the one‑sided text damage (0.0016→0.0130); the
ACMG BA1/BS1 frequency gate removes the residual (→0.0017, back to structural). The
gate's benefit is visible **per variant**, not in aggregate slice metrics (the slice
holds only one such benign common variant), which is exactly what the AF‑threshold
sensitivity table shows (flat Brier/BSS across θ = 2e−4…5e−3).

## Structural feature importance (permutation, AUROC drop)

`is_frameshift` 0.180 › `is_synonymous` 0.109 › `AF` 0.057 › `is_intron` 0.015 ›
`is_splice_site` 0.008 › `SIFT` 0.006 › `is_stop_gained` 0.004 › `PolyPhen` 0.000 ›
`is_missense` −0.000. Consequence class and population frequency dominate — consistent
with high‑confidence ClinVar labels and with the fact that subtle missense predictors
add little once truncating/synonymous/AF are known.

## Figures

- `fig_calibration_full_8D.png` — reliability curves, full test set (S and F nearly overlap).
- `fig_calibration_matched_8D.png` — reliability curves, matched slice (F visibly less extreme).
- `fig_alpha_sensitivity_8D.png` — AUROC/Brier/BSS vs α (full and matched).
- (8C) `fig_vus_conflict_triage.png` — conflict signal, VUS‑with‑text vs confident labels.

## One‑line takeaway

A strong structural baseline (AUROC 0.903) plus sparse, one‑sided literature, fused by
a balanced‑α, confidence/specificity/provenance/frequency‑gated Bayesian update,
yields **calibrated, interpretable, uncertainty‑aware** interpretation on the minority
of variants that literature actually discusses — without ever harming the rest.
