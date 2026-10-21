# Ethics and Data Use Policy

EvidVar is a research tool designed for computational biology and bioinformatics education. It processes publicly available data to generate hypotheses about genetic variant pathogenicity. This document outlines the ethical considerations, data usage restrictions, and disclaimers associated with this project.

## 1. Not for Clinical Use

**CRITICAL DISCLAIMER:**  
EvidVar outputs are **NOT** intended for medical diagnosis, treatment decisions, patient management, or clinical reporting. 

*   The models are trained on curated but potentially noisy consensus labels from ClinVar.
*   The literature mining component relies on zero-shot NLP, which lacks the nuance of expert human curation.
*   Performance metrics (AUROC ~0.90) reflect statistical association in a specific dataset, not clinical sensitivity/specificity in a diverse patient population.

Any use of EvidVar results in a clinical setting is strictly prohibited and could lead to harmful outcomes. Users assume all risk for any misuse of this software.

## 2. Data Sources and Licensing

EvidVar aggregates data from three primary public sources. Users must comply with the terms of service for each:

### ClinVar (NCBI)
*   **License:** Public Domain / CC0.
*   **Usage:** We use ClinVar for ground-truth labels and HGVS identifiers.
*   **Attribution:** Cite Landrum MJ, et al. "ClinVar: improving access to variant interpretations and supporting evidence." *Nucleic Acids Res.* 2018.

### PubMed / MEDLINE (NCBI)
*   **License:** Public Access / Fair Use.
*   **Usage:** We retrieve abstracts solely for text mining and evidence extraction. We do not redistribute full-text articles.
*   **Restriction:** Do not scrape excessive volumes violating NCBI's rate limits (we implement polite delays and batch sizes).
*   **Attribution:** Cite National Center for Biotechnology Information. "PubMed Database."

### Ensembl (EMBL-EBI)
*   **License:** Apache 2.0 / Creative Commons Attribution 4.0 International.
*   **Usage:** We query the REST API for variant consequences (VEP) and frequencies.
*   **Restriction:** Adhere to Ensembl's fair use policy. Do not hammer the server; use caching mechanisms provided in the code.
*   **Attribution:** Cite Martin FJ, et al. "Ensembl 2020." *Nucleic Acids Res.* 2020.

## 3. Privacy and Human Subjects

*   **No PII:** EvidVar does not process Personally Identifiable Information (PII) or Protected Health Information (PHI).
*   **Aggregate Data:** Input data consists of anonymized germline variant records and published scientific literature.
*   **Genetic Sensitivity:** While BRCA1/2 variants are clinically sensitive, the data used here is already public. However, researchers should remain mindful that re-identification risks exist in genomics generally. This tool does not attempt to link variants to individuals.

## 4. Bias and Fairness

*   **Dataset Imbalance:** The training data is heavily skewed toward European ancestry populations due to historical biases in GWAS and sequencing efforts. Allele frequencies (AF) derived from gnomAD may not accurately represent global diversity.
*   **Literature Bias:** Evidence mined from PubMed reflects publication bias. Well-studied variants have more literature support, while rare or novel variants may appear "unknown" simply due to lack of study, not lack of pathogenicity.
*   **Algorithmic Bias:** The zero-shot NLP model may perform differently on technical jargon vs. plain language descriptions found in older papers.

Users are encouraged to evaluate performance across different ancestral groups before drawing general conclusions.

## 5. Responsible AI Practices

*   **Uncertainty Quantification:** EvidVar explicitly reports uncertainty (via calibration metrics and VUS triage) rather than providing binary black-box answers.
*   **Transparency:** The methodology, including limitations and failure modes (e.g., circular reasoning detection), is fully documented in `docs/methods.md` and `docs/limitations.md`.
*   **Reproducibility:** The entire pipeline is open-source and containerizable (Colab notebooks), allowing peers to verify results.

## 6. Contact

For questions regarding ethics or data use, please open an issue on the GitHub repository.