
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

INPUT = Path("data/raw/clinvar_variant_summary.txt.gz")
OUT_FILTERED = Path("data/processed/clinvar_brca_filtered.csv.gz")
OUT_TABLE_CS = Path("results/tables/clinvar_brca_clinical_significance_counts.csv")
OUT_TABLE_RS = Path("results/tables/clinvar_brca_review_status_counts.csv")
OUT_FIG = Path("results/figures/clinvar_brca_label_distribution.png")

def main():
    if not INPUT.exists():
        raise FileNotFoundError("ClinVar file missing. Run download script first.")
    
    print("Reading ClinVar data...")
    # Read only necessary columns to save memory/time if possible, 
    # but full read is safer for exploration initially.
    df = pd.read_csv(INPUT, sep="\t", compression="gzip", low_memory=False)
    
    print(f"Total rows: {len(df):,}")
    
    # Find Columns dynamically
    cols = df.columns.tolist()
    gene_col = next((c for c in cols if 'gene' in c.lower()), None)
    cs_col = next((c for c in cols if 'clinical' in c.lower() or 'significanc' in c.lower()), None)
    rs_col = next((c for c in cols if 'review' in c.lower()), None)
    
    if not gene_col or not cs_col:
        print("Columns detected:", cols[:20])
        raise ValueError("Could not auto-detect Gene/ClinicalSignificance columns. Please check column names.")
        
    print(f"Using Gene Column: {gene_col}")
    print(f"Using Clinical Sig Column: {cs_col}")
    print(f"Using Review Status Column: {rs_col}")
    
    # Filter BRCA1/BRCA2
    mask = df[gene_col].astype(str).str.contains(r'\bBRCA[12]\b', case=False, regex=True, na=False)
    brca_df = df[mask].copy()
    
    print(f"BRCA Rows: {len(brca_df):,}")
    
    # Save filtered data
    OUT_FILTERED.parent.mkdir(parents=True, exist_ok=True)
    brca_df.to_csv(OUT_FILTERED, index=False, compression='gzip')
    print(f"Saved filtered data to: {OUT_FILTERED}")
    
    # Count Clinical Significance
    vc_cs = brca_df[cs_col].fillna('Unknown').value_counts()
    OUT_TABLE_CS.parent.mkdir(parents=True, exist_ok=True)
    vc_cs.to_csv(OUT_TABLE_CS)
    print("\n--- Clinical Significance Counts ---")
    print(vc_cs.head(10))
    
    # Count Review Status
    if rs_col:
        vc_rs = brca_df[rs_col].fillna('Unknown').value_counts()
        OUT_TABLE_RS.parent.mkdir(parents=True, exist_ok=True)
        vc_rs.to_csv(OUT_TABLE_RS)
        print("\n--- Review Status Counts ---")
        print(vc_rs.head(10))
        
    # Plot
    top_n = 10
    plot_data = vc_cs.head(top_n)[::-1]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=plot_data.values, y=plot_data.index, palette='viridis')
    plt.title(f"Top {top_n} Clinical Significance Categories for BRCA1/2")
    plt.xlabel("Count")
    plt.ylabel("Category")
    plt.tight_layout()
    
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_FIG, dpi=150)
    plt.close()
    print(f"\nSaved figure to: {OUT_FIG}")

if __name__ == "__main__":
    main()
