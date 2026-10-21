# Methods

## 1. Variant universe and labels

We start from the ClinVar `variant_summary.txt.gz` tab‑delimited release and keep
records whose `GeneSymbol` matches `BRCA1` or `BRCA2` (regex `\bBRCA[12]\b`). The
rsID is taken from the `RS# (dbSNP)` column and normalised to lowercase `rs…`; the
HGVS string from the `Name` column (e.g. `NM_007294.4(BRCA1):c.68_69delAG`), reduced
to the change portion after the last colon.

Labels are mapped to a binary target for supervised evaluation:

| ClinVar `ClinicalSignificance` | label |
|---|---|
| Pathogenic, Likely pathogenic, Pathogenic/Likely pathogenic | 1 |
| Benign, Likely benign, Benign/Likely benign | 0 |
| Uncertain significance, Conflicting classifications, `-`, not provided | excluded from supervised training; retained as an **uncertainty set** |

To reduce label noise we restrict the supervised pool to records whose
`ReviewStatus` is one of: *criteria provided, multiple submitters, no conflicts*;
*reviewed by expert panel*; *criteria provided, single submitter*. Records are then
deduplicated to one row per `VariationID`. This yields **16,355** high‑confidence
labelled variants (51.9% pathogenic / 48.1% benign) plus a separate VUS/conflicting
pool used only for uncertainty analysis.

## 2. Structured genomic features

Each variant is annotated via the Ensembl REST API (`/vep/human/id/`, batched POST,
JSON‑cached and resumable; `/variation/human/` for HGVS cross‑checks). From the
canonical transcript we extract:

- **consequence‑class binary flags**: `is_frameshift`, `is_stop_gained`,
  `is_splice_site` (splice acceptor/donor), `is_missense`, `is_intron`,
  `is_synonymous` (substring match on `;`‑joined `consequence_terms`);
- **SIFT** and **PolyPhen‑2** scores (present only for missense; `NaN` otherwise);
- **allele frequency** (`AF`), averaged across available population frequencies from
  colocated variants.

`NaN` SIFT/PolyPhen/AF are *informative missingness* (e.g. a frameshift has no
missense score), so the structural model is a `HistGradientBoostingClassifier`,
which handles missing values natively. The structural model is trained on the nine
features above with an 80/20 stratified split (seed 42).

## 3. Literature evidence mining

We fetch up to 5,000 PubMed records matching
`(BRCA1[Title/Abstract] OR BRCA2[Title/Abstract]) AND (pathogenic OR mutation OR variant)`
via E‑utilities (esearch → efetch, XML, batched, rate‑limited), retaining ~4,645
abstracts.

**Attribution by exact HGVS, not rsID.** Abstracts rarely print `rs…`; they print
`c.`/`p.` notations. We therefore build a token→variant dictionary from the ClinVar
`Name` column (read in 400k‑row chunks to bound RAM) using strict regexes that
capture the *full* allele change (`c.\d[\w+\-/>*_]*`, `p\.[A-Z][a-z]{2}\d+[A-Za-z0-9*/_]*`)
and **reject position‑only tokens** (e.g. bare `c.631`, trailing `c.81-`) to prevent
positional collisions where one generic sentence is credited to many variants.
Abstracts are split into sentences; a sentence is linked to a variant only if it
contains that variant's exact specific token. This precision‑first choice trades
recall for trustworthy attribution.

The mining yields **912 evidence sentences** covering **519** distinct variants
(350 labelled, 169 VUS/conflicting). After requiring *decided, non‑circular*
sentences (below), **149** labelled variants carry usable text.

## 4. Zero‑shot polarity, confidence, conflict, circularity

Each sentence is scored by a zero‑shot NLI model
(`MoritzLaurer/deberta-v3-base-zeroshot-v1`) against two hypotheses —
*"the variant is pathogenic/likely pathogenic"* and *"the variant is benign/likely
benign"* — with `multi_label=True`, giving independent `path_score` and `ben_score`.
Derived per‑sentence fields:

- `polarity` ∈ {supports_pathogenic, supports_benign, ambiguous, neutral} via a
  margin rule (|path−ben| > 0.10 and max > 0.35, else neutral/ambiguous);
- `confidence` = max(path, ben);
- `conflict_score` = 1 − |path−ben|/(path+ben) when both > 0.2, else 0;
- `circular` flag via regex for sentences that merely *restate* database calls
  (ClinVar/OncoKB/LOVD/"annotated as P/LP…"), so we do not double‑count ClinVar
  evidence into a ClinVar‑trained model.

Observed distribution: 316 supports_pathogenic, 0 supports_benign, 8 ambiguous,
588 neutral; 39/912 circular; 17 with conflict > 0.3. The **absence of benign
calls is a real, reported property** of abstract‑level zero‑shot mining on BRCA and
drives the gating design below.

## 5. Per‑variant text aggregation

For each variant we sum a per‑sentence weight
`w = confidence / variants_in_sentence` (down‑weighting sentences that list many
alleles), zeroed if `circular`. Aggregated features:
`text_path = Σ w·path_score`, `text_ben = Σ w·ben_score`,
`text_n` (# decided non‑circular sentences), `text_conflict` (max),
`text_mean_conf`, `text_n_circ`. Net signal `net_text = text_path − text_ben`.

## 6. Bayesian log‑odds fusion with gates

The fused posterior is a log‑odds update of the structural prior:
logit P(path | X, E) = logit P(path | X) + α · LR_text
LR_text = clip( has_text · net_text · mean_conf · AF_gate , −3, +3 )


- `has_text ∈ {0,1}` is the **guard**: with no decided non‑circular sentence the text
  term is exactly 0, so ~99% of variants are provably unchanged by the text channel.
- `mean_conf` scales the update by extraction confidence.
- `AF_gate = 1 / (1 + (AF / θ)²)`, θ = 1e−3, is an **ACMG‑inspired (BA1/BS1)
  population‑frequency gate**: a common variant's literature mentions are suppressed,
  preventing frequent benign polymorphisms from being falsely upgraded (worked example
  rs11571833, AF 0.0044 → gate 0.049).
- `clip(·,−3,+3)` stops one overconfident sentence from dominating.

**α selection (the key safeguard).** α is chosen on *out‑of‑fold* structural
predictions restricted to train‑fold text‑bearing variants, minimising **balanced**
log‑loss (positives and negatives each weighted 0.5) with a parsimony rule (smallest α
within +0.01 of the minimum). Ordinary log‑loss is deliberately *not* used because the
text subset is 90% pathogenic and would reward "any text ⇒ pathogenic"; the balanced
criterion yields α = 4 (interior minimum), versus α = 16 under ordinary loss.

## 7. Evaluation protocol

- **Full test set** (n=3,271): AUROC, AUPRC, Brier, balanced Brier, **Brier Skill
  Score vs the prevalence baseline**, ECE, calibration slope/intercept.
- **Matched text‑bearing slice** (test‑fold ∩ `text_n>0`, n=30): the same metrics,
  reported with **1,000‑replicate bootstrap 95% CIs** on absolute metrics and on
  fused−structural deltas. Because this slice is 90% pathogenic and tiny, the
  prevalence baseline is strong and *all* models (including structural) show negative
  absolute BSS; we therefore interpret the **delta** (fusion vs structural) and the
  calibration slope/intercept shift, not the absolute BSS, and state the subset
  degeneracy explicitly.
- **Ablations**: α = 0 (pure structural) vs fused with vs without the AF gate; AF
  threshold sensitivity (θ ∈ {2e−4 … 1e−2}); α sensitivity (descriptive).
- **Uncertainty triage**: VUS/conflicting variants (not in the supervised pool) are
  scored with the same aggregation; conflict/volume/circularity distributions are
  compared against confidently labelled variants (figure only — no pseudo‑labels).
- **Leakage controls**: variant‑level dedup; stratified split on `VariationID`; α fit
  only on train‑fold text‑bearing rows; circular sentences excluded from evidence
  strength.

Structural feature importance (permutation, AUROC drop, test fold):
`is_frameshift` 0.180, `is_synonymous` 0.109, `AF` 0.057, `is_intron` 0.015,
`is_splice_site` 0.008, `SIFT` 0.006, `is_stop_gained` 0.004, `PolyPhen` 0.000,
`is_missense` −0.000 — i.e. consequence class and population frequency dominate,
consistent with high‑confidence ClinVar labels.
