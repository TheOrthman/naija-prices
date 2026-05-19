import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.extract.scrape_prices import scrape_nairametrics
from src.load.load_to_sqlite import load_csv
import subprocess

def run_pipeline():
    csv = scrape_nairametrics()
    load_csv(csv)
    subprocess.run(["python", "src/transform.py"])
    print("Pipeline complete")

if __name__ == "__main__":
    run_pipeline()