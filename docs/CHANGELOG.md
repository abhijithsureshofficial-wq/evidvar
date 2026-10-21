# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release of EvidVar pipeline.
- Documentation: README, Methods, Limitations, Results Summary.
- Benchmark dataset: `evidence_nlp_polarity.csv.gz` (912 annotated sentences).

### Changed
- None.

### Fixed
- None.

## [0.1.0] - 2026-10-21

### Added
- **Data Ingestion**: Scripts to download ClinVar `variant_summary.txt.gz` and extract BRCA1/BRCA2 variants with rsIDs.
- **Annotation Pipeline**: Integration with Ensembl REST API (`/vep/human/id/`) for structured genomic features (Consequence, SIFT, PolyPhen, AF).
- **Literature Mining**: 
  - PubMed abstract retrieval via NCBI E-utilities.
  - Strict HGVS regex matching to link abstracts to specific variants (precision-first approach).
  - Zero-shot NLP polarity extraction using `MoritzLaurer/deberta-v3-base-zeroshot-v1`.
- **Modeling**:
  - Structural baseline model using `HistGradientBoostingClassifier`.
  - Bayesian log-odds fusion mechanism integrating text evidence as a gated likelihood ratio.
  - ACMG-inspired BA1/BS1 population-frequency gate to suppress evidence for common benign polymorphisms.
- **Evaluation**:
  - Comprehensive metrics: AUROC, AUPRC, Brier Score, Balanced Brier, ECE, Calibration Slope/Intercept.
  - Bootstrap confidence intervals (1,000 replicates) for matched text-bearing slices.
  - Ablation studies for alpha selection and AF thresholds.
- **Documentation**: 
  - `docs/methods.md`: Detailed algorithmic description.
  - `docs/limitations.md`: Honest reporting of sparse coverage and one-sided signal.
  - `docs/results_summary.md`: Key findings and interpretation guidelines.
  - `README.md`: Project overview and reproduction instructions.

### Security
- No sensitive data processed; all inputs are from public databases (ClinVar, PubMed, Ensembl).

[Unreleased]: https://github.com/your-username/evidvar/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-username/evidvar/releases/tag/v0.1.0