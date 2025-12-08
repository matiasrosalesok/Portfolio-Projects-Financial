"""
Simple exporter: convierte Parquet de ejemplo a CSV para PowerBI.
Uso: python scripts/export_powerbi_dataset.py --in sample.parquet --out sample.csv
"""
import argparse
import pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--in', dest='infile', required=True)
    p.add_argument('--out', dest='outfile', required=True)
    args = p.parse_args()

    df = pd.read_parquet(args.infile)
    df.to_csv(args.outfile, index=False)
    print(f"Exported {args.infile} -> {args.outfile}")

if __name__ == '__main__':
    main()
