# EvidVar

**EvidVar** is a reproducible NLP + probabilistic‑genetics pipeline that interprets
BRCA1/BRCA2 germline variants by fusing structured genomic annotations (ClinVar,
Ensembl) with sentence‑level evidence mined from biomedical literature (PubMed),
and by quantifying *uncertainty* rather than only predicting a label.

## Research question

> Can textual evidence extracted from biomedical literature improve **calibrated**
> probabilistic classification of BRCA1/BRCA2 variants beyond structured genomic
> annotations alone — and can that evidence be integrated *safely* (gated by
> confidence, specificity, provenance and population frequency) so that sparse,
> one‑sided literature never damages a strong structural baseline?

## Headline result (honest framing)

Literature evidence is **sparse** (usable decided, non‑circular sentences exist for
~0.9% of high‑confidence variants: 149/16,355) and **one‑sided** (the zero‑shot
extractor yields essentially no benign‑supporting evidence). EvidVar therefore does
**not** claim a large discrimination gain. It claims a *reproducible, evidence‑gated,
calibration‑focused* fusion that:

1. leaves variants without usable text **unchanged by construction**;
2. on the text‑bearing subset **consistently improves calibration** (Brier, balanced
   Brier, ECE and Brier Skill Score all favoured in **100% of 1,000 bootstrap
   replicates**; AUROC unchanged);
3. corrects residual one‑sided false upgrades on common benign polymorphisms via an
   **ACMG‑inspired (BA1/BS1) population‑frequency gate** (worked example: rs11571833);
4. releases a **912‑sentence annotated evidence benchmark** for variant interpretation.

Full‑set performance: structural AUROC **0.903** (BSS **0.51**); fused AUROC **0.904**.
See `docs/results_summary.md` for every table and figure.

## Pipeline
ClinVar variant_summary ──
├─► normalize + label + quality filter ─► train/val/test splits
Ensembl VEP (rsID) ─────── │
▼
structured features (consequence flags, SIFT, PolyPhen, AF)
│
PubMed BRCA abstracts ─► HGVS sentence mining ─► zero‑shot polarity (DeBERTa‑v3)
│ + confidence + conflict + circularity
▼
per‑variant text aggregation (confidence/specificity‑weighted)
│
Bayesian log‑odds fusion = prior(structural)
+ α · gated_text_LR
▼
calibrated P(pathogenic) + uncertainty + evidence explanation


## Data sources (all public)

- **ClinVar** `variant_summary.txt.gz` (NCBI FTP) — labels, review status, HGVS (`Name`), rsID (`RS# (dbSNP)`).
- **Ensembl REST** `/vep/human/id/` and `/variation/human/` — consequence, SIFT, PolyPhen, allele frequency.
- **PubMed / NCBI E‑utilities** — BRCA1/2 abstracts (esearch + efetch).
- **Zero‑shot NLI model**: `MoritzLaurer/deberta-v3-base-zeroshot-v1` (Hugging Face).

## Reproduce (Colab, in order)

The project was built as an ordered sequence of notebook cells; run them top‑to‑bottom:

| Cell | Purpose | Output |
|------|---------|--------|
| 1 | env + folders | `data/`, `src/`, `results/` skeleton |
| 2 | download ClinVar, extract BRCA + rsID | `data/interim/brca_with_rsid.csv.gz` |
| 3 | label map + quality filter + stratified split | `data/processed/{train,val,test}_set.csv.gz` |
| 4 | Ensembl VEP annotation (batched, cached, resumable) | `data/processed/clinvar_brca_annotated_final.csv.gz` |
| 5 | structural baseline (HistGradientBoosting) | `models/baseline_structural_model.pkl` |
| 6A | PubMed abstract fetch (5,000 → ~4,645) | `data/interim/pubmed_abstracts.csv.gz` |
| 6B | strict HGVS sentence mining (chunked, memory‑safe) | `data/processed/evidence_sentences.csv.gz` |
| 7A | token/dedup cleanup + evidence‑type flags | `data/processed/evidence_clean_*.csv.gz` |
| 7B/7C | zero‑shot polarity + confidence + conflict + circularity | `data/processed/evidence_nlp_polarity.csv.gz` |
| 8A | per‑variant text aggregation + balance diagnostics | `data/processed/variant_features_supervised.csv.gz` |
| 8B/8C | fusion + bootstrap + ablation + case studies | `results/tables/*_8C.csv`, figures |
| 8D | **balanced** α selection + prevalence‑aware calibration | `results/tables/*_8D.csv`, `models/fusion_config_8D.json` |
| 9A | this documentation | `README.md`, `docs/*.md` |

Raw ClinVar (~435 MB) is **not** committed; `src/` scripts re‑download it. Processed
tables, models, figures and the benchmark **are** committed (small).

## Released benchmark

`data/processed/evidence_nlp_polarity.csv.gz` — 912 BRCA1/2 evidence sentences with
variant ID, PMID, matched HGVS token, evidence type, zero‑shot polarity, confidence,
conflict score and circularity flag. Intended as a starting point for evaluating
literature‑based variant evidence extraction. See `docs/methods.md` §Evidence mining.

## Limitations (read before citing)

See `docs/limitations.md`. In brief: ~0.9% text coverage; one‑sided text signal;
the text‑bearing subset is 90% pathogenic and n=30 (so absolute BSS there is negative
for *all* models — a subset artefact, explained in `results_summary.md`); ClinVar
labels are curated consensus, not gold truth; abstracts (not full text) were mined;
the NLP step is zero‑shot, not fine‑tuned; no temporal split yet. **Not for clinical use.**

## License & citation

Code: MIT (see `LICENSE`). Data: respect NCBI/Ensembl terms of use; cite ClinVar,
Ensembl and PubMed/NCBI as per their policies. If you use the benchmark, cite this
repository and the underlying resources.

## Disclaimer

Research/educational prototype for evidence‑aware variant *prioritisation and
uncertainty triage*. **Not** a diagnostic tool and **not** intended for clinical
decision‑making or patient management.
