# Reproducibility Guide

This document ensures that researchers can replicate the EvidVar results exactly. Due to the nature of web APIs (ClinVar, Ensembl, PubMed) and stochastic ML models, strict bit-for-bit reproducibility is challenging. However, we provide strategies to achieve statistical reproducibility.

## 1. Environment Setup

### Hardware Requirements
*   **GPU:** NVIDIA T4 or equivalent (recommended for NLP inference speed). CPU-only execution is supported but significantly slower (~10x).
*   **RAM:** Minimum 16 GB recommended (for loading large Pandas DataFrames).
*   **Storage:** ~2 GB free space for intermediate files and caches.

### Software Dependencies
Install the required packages using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
 ```

###Key Versions Tested:
Python: 3.10+
pandas: >=2.0.0
scikit-learn: >=1.3.0
transformers: >=4.30.0
torch: >=2.0.0
tqdm: >=4.65.0

###Random Seeds
All stochastic processes are seeded with RANDOM_STATE = 42. This applies to:
Train/Test splits (sklearn.model_selection.train_test_split).
Gradient Boosting initialization (HistGradientBoostingClassifier).
Bootstrap resampling (np.random.default_rng(42)).
K-Fold cross-validation (KFold(random_state=42)).

## 2. Data Versioning Challenges
Public databases change daily. To reproduce specific results, you must pin the data snapshots.

###ClinVar Snapshot
* **Current Behavior:** Downloads the latest variant_summary.txt.gz from NCBI FTP.
* **Reproduction Strategy:** For exact replication, download the archive from a specific date (e.g., October 2026 snapshot) and place it in data/raw/. Update the script to skip downloading if the file exists.

###Ensembl Release
* **Current Behavior:** Queries the live REST API (rest.ensembl.org).
* **Reproduction Strategy:** The code uses a local JSON cache (data/interim/ensembl_cache.json).
  * Run the pipeline once to populate the cache.
  * Commit the cache file (or share it separately) to freeze the annotations.
  * Subsequent runs will load from cache, ensuring identical features regardless of Ensembl updates.

###PubMed Search
* **Current Behavior:** Fetches top 5,000 relevance-sorted abstracts.
* **Reproduction Strategy:** The search term and limit are hardcoded. However, PubMed indexing changes.
   * Save the resulting pubmed_abstracts.csv.gz immediately after generation.
   * Share this CSV to ensure downstream text mining operates on the exact same corpus.

## 3. Step-by-Step Execution Order
Run the cells in the Jupyter Notebook (01_Setup_and_ClinVar_Exploration.ipynb) in sequential order:
*Cell 1:* Install deps and create directory structure.
*Cell 2:* Download ClinVar & Extract BRCA/rsIDs. (Output: brca_with_rsid.csv.gz)
*Cell 3:* Label cleaning & Train/Test Splitting. (Output: train_set.csv.gz, val_set.csv.gz, test_set.csv.gz)
*Cell 4:* Ensembl VEP Annotation. (Output: clinvar_brca_annotated_final.csv.gz, ensembl_cache.json)
*Note:* This step involves network calls. If interrupted, re-run to resume from cache.
*Cell 5:* Structural Baseline Model Training. (Output: baseline_structural_model.pkl)
*Cell 6A:* PubMed Abstract Retrieval. (Output: pubmed_abstracts.csv.gz)
*Cell 6B:* Strict HGVS Sentence Mining. (Output: evidence_sentences.csv.gz)
*Cell 7A:* Evidence Cleaning & Tagging. (Output: evidence_clean_*.csv.gz)
*Cell 7B/7C:* Zero-Shot NLP Polarity Extraction. (Output: evidence_nlp_polarity.csv.gz)
*Note:* Requires GPU for reasonable speed. Uses deberta-v3-base-zeroshot-v1.
*Cell 8A:* Per-Variant Text Aggregation. (Output: variant_features_supervised.csv.gz)
*Cell 8B/8C/8D:* Fusion, Calibration, Bootstrap, and Final Metrics. (Output: Tables in results/tables/, Figures in results/figures/)

## 4. Verification Checks
To verify your reproduction was successful, check the following outputs against the values reported in docs/results_summary.md:
Variant Universe Size: Should be exactly 16,355 labeled variants.
* **Evidence Sentences:** Should yield approximately 912 clean sentences.
* **Structural AUROC (Test Set):** Expected 0.9028 ± 0.0005.
* **Fused AUROC (Test Set):** Expected 0.9040 ± 0.0005.
* **Selected Alpha:** Must be 4.0 (based on balanced log-loss minimization).
If these values deviate significantly (>0.01 difference in AUROC), investigate:
*Did you use the cached Ensembl data?
*Is the random seed set to 42 everywhere?
*Did the PubMed search return a different number of abstracts due to API changes?

## 5. Docker Container (Future Work)
While currently distributed as Colab notebooks, a Docker image is planned for production-grade reproducibility. This will bundle:
* Specific versions of Python libraries.
* Frozen copies of ClinVar/Ensembl/PubMed data snapshots.
* Pre-trained model weights.
Stay tuned to the repository releases for the docker-compose.yml configuration.

