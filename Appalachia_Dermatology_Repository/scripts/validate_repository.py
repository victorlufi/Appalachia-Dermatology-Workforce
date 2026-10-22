"""Verify ZIP allocation and headline statistics against the frozen master workbook."""
from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data'
def main():
    zipdf=pd.read_csv(D/'zip_dermatologist_counts.csv',dtype=str)
    zcol='Provider Business Practice Location Address Postal Code'
    zipdf['ZIP']=zipdf[zcol].str[:5].str.zfill(5)
    zipdf['dermatologist_count']=pd.to_numeric(zipdf['dermatologist_count'])
    cross=pd.read_excel(D/'HUD_USPS_ZIP_COUNTY_092025.xlsx',dtype={'ZIP':str,'COUNTY':str})
    cross['ZIP']=cross['ZIP'].str.zfill(5);cross['COUNTY']=cross['COUNTY'].str.zfill(5)
    cross['TOT_RATIO']=pd.to_numeric(cross['TOT_RATIO'],errors='coerce').fillna(0)
    merged=zipdf[['ZIP','dermatologist_count']].merge(cross[['ZIP','COUNTY','TOT_RATIO']],on='ZIP',how='left')
    matched=merged.dropna(subset=['COUNTY']).copy()
    sums=matched.groupby('ZIP')['TOT_RATIO'].transform('sum')
    matched=matched.loc[sums>0].copy()
    matched['allocated']=matched['dermatologist_count']*matched['TOT_RATIO']/matched.groupby('ZIP')['TOT_RATIO'].transform('sum')
    county=matched.groupby('COUNTY')['allocated'].sum()
    master=pd.read_excel(D/'Appalachia_Master_Analysis_Dataset.xlsx',sheet_name='County_Level_Data',dtype={'county_fips':str})
    master['county_fips']=master['county_fips'].str.zfill(5)
    print('ZIP total:',zipdf.dermatologist_count.sum())
    print('Reallocated total:',round(county.sum(),6))
    print('Frozen master total:',round(master.dermatologist_count.sum(),6))
    aligned=master.set_index('county_fips')['dermatologist_count'].reindex(county.index).fillna(0)
    print('County allocation max absolute discrepancy:',round(float((county-aligned).abs().max()),8))
    print('Master county count:',len(master),'Appalachian counties:',int(master.is_appalachia.sum()))
    for label, subset in [('Appalachia',master[master.is_appalachia==True]),('Non-Appalachia',master[master.is_appalachia==False])]:
        rate=100000*subset.dermatologist_count.sum()/subset.population.sum()
        zeros=int((subset.dermatologist_count==0).sum())
        pop_zero=100*subset.loc[subset.dermatologist_count==0,'population'].sum()/subset.population.sum()
        print(f'{label}: density={rate:.4f}, zero counties={zeros}, population in zero counties={pop_zero:.3f}%')
    print('REFERENCE: 25392 ZIP, ~25358 allocated, 3235 counties, 423 ARC, 4.79/7.67 densities, 186/1358 zero counties')
if __name__=='__main__':main()
