"""Reconstructed NPPES prefilter, NOT the verified original extraction.
Usage: python scripts/reconstruct_nppes_filter.py path/to/npidata_pfile.csv output.csv
Compare output with data/zip_dermatologist_counts.csv before using.
"""
import sys
from pathlib import Path
import pandas as pd
TAXONOMY='207N00000X'
def main(input_file, output_file):
    # Header-only read to select fields and avoid holding the ~10GB CSV in memory.
    headers=pd.read_csv(input_file,nrows=0).columns.tolist()
    tax=[c for c in headers if 'Healthcare Provider Taxonomy Code' in c]
    zipcol='Provider Business Practice Location Address Postal Code'
    if not tax or zipcol not in headers:raise ValueError('Required NPPES fields missing')
    npi='NPI'
    seen=set();counts={}
    for chunk in pd.read_csv(input_file,usecols=[npi,zipcol]+tax,dtype=str,chunksize=100000,low_memory=False):
        matches=chunk[tax].eq(TAXONOMY).any(axis=1)
        for _,row in chunk.loc[matches,[npi,zipcol]].iterrows():
            ident=row[npi]
            if not isinstance(ident,str) or ident in seen:continue
            seen.add(ident)
            z=str(row[zipcol])[:5]
            if len(z)!=5 or not z.isdigit():continue
            counts[z]=counts.get(z,0)+1
    result=pd.DataFrame([(z,c) for z,c in sorted(counts.items())],columns=[zipcol,'dermatologist_count'])
    result.to_csv(output_file,index=False)
    print('Unique NPIs with taxonomy:',len(seen),'valid-ZIP count:',result.dermatologist_count.sum())
    print('Reference original ZIP total: 25392; reconstructed result must be compared, not assumed equivalent.')
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python scripts/reconstruct_nppes_filter.py input.csv output.csv')
    main(sys.argv[1],sys.argv[2])
