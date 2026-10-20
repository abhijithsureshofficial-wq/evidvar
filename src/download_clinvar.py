
import requests
from pathlib import Path
import sys

URL = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
DEST = Path("data/raw/clinvar_variant_summary.txt.gz")

def download():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        print(f"File already exists: {DEST}")
        return
    
    print(f"Downloading from {URL}...")
    with requests.get(URL, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(DEST, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = 100 * downloaded // total
                        sys.stdout.write(f"\rProgress: {pct}% ({downloaded//1024//1024} MB)")
                        sys.stdout.flush()
    print("\nDownload complete.")

if __name__ == "__main__":
    download()
