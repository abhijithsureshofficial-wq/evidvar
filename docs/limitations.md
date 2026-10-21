# Limitations and honest boundaries

These are stated up front because overclaiming here is the fastest route to rejection.
Each is also a concrete future‑work item.

1. **Sparse text coverage.** Usable decided, non‑circular literature evidence exists
   for only **149 / 16,355** high‑confidence BRCA1/2 variants (~0.9%). The fusion
   therefore cannot, by construction, move full‑set discrimination much; its value is
   on the minority of discussed variants and in *how* it handles them. Extending to
   full‑text (Europe PMC / OA articles) and to more genes would raise coverage.

2. **One‑sided text signal.** The zero‑shot extractor produced **0** benign‑supporting
   sentences. Text can only nudge toward pathogenic. We do **not** treat "no benign
   text" as benign evidence (the `has_text` guard + clipping enforce this), but a
   symmetric signal would require better benign phrasing templates or fine‑tuning.

3. **Pathogenic‑enriched, tiny matched subset.** The text‑bearing labelled subset is
   **90.6% pathogenic** and the test slice is **n = 30**. Consequently the *absolute*
   Brier Skill Score on that slice is negative for **every** model, including the
   strong structural one — a property of the degenerate subset and the prevalence
   baseline, not a failure of fusion. We report bootstrap deltas (100% favourable) and
   the calibration slope/intercept shift instead, and flag the slice‑level calibration
   parameters as unstable at this n.

4. **ClinVar labels are consensus, not gold truth.** Even after review‑status
   filtering, labels carry curator disagreement and temporal drift. We treat them as
   the best available approximation and exclude VUS/conflicting from supervised
   training rather than forcing a label.

5. **Abstracts, not full text.** Evidence is mined from PubMed abstracts only. Much
   functional/segregation detail lives in methods/results sections we did not parse,
   which caps recall and biases toward variants prominent in abstracts.

6. **Zero‑shot, not fine‑tuned, NLP.** Polarity comes from a general NLI model with
   two fixed hypotheses; it is not trained on variant‑interpretation text. The manual
   read of representative sentences (rescue‑context false positive, circular
   restatement, weak‑claim low confidence, common‑variant text trap) shows the failure
   modes a fine‑tuned biomedical classifier (e.g. PubMedBERT) would target. The
   912‑sentence file is released precisely to enable that.

7. **No temporal evaluation yet.** The current split is random at variant level. A
   prospective split (older literature → newer ClinVar reclassifications) is the
   strongest test of real‑world utility and is planned future work.

8. **Single‑gene family.** Results are BRCA1/2‑specific; consequence/frequency
   priors and literature density differ elsewhere. Generalisation requires a second
   panel (e.g. Lynch or cardiomyopathy genes) as a held‑out test.

9. **Not clinical.** This is a research/educational prototype for evidence
   prioritisation and uncertainty triage. It is **not** validated for diagnosis,
   screening, or patient management, and must not be used as such.
