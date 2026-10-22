# Dermatologist Access Disparities and Melanoma Outcomes in Appalachian Versus Non-Appalachian US Counties

Reproducibility materials for a county-level ecological dermatology workforce study. **This repository is a documented research archive, not a fully independent end-to-end replication pipeline.** The original exploratory notebook includes local Windows paths, iterative calculations and references to ARC classification files not supplied separately. The frozen master workbook is the reference dataset for the manuscript.

## Contents
- `data/Appalachia_Master_Analysis_Dataset.xlsx`: frozen analytic county-level data and summary worksheets.
- `data/zip_dermatologist_counts.csv`: original aggregated ZIP-level dermatologist counts (25,392 across 5,029 ZIPs).
- `data/HUD_USPS_ZIP_COUNTY_092025.xlsx`: September 2025 HUD ZIP/county crosswalk.
- `data/co-est2024-pop.xlsx`: Census county population file.
- `data/Melanoma_Incidence_CDC_NIH.csv`, `data/Melanoma_Mortality_CDC_NIH.csv`: original melanoma exports (2018–2022).
- `notebooks/original_exploratory_analysis.ipynb`: original working notebook, with cell outputs cleared to avoid unnecessary embedded plots; **not intended for clean sequential execution**.
- `scripts/validate_repository.py`: recomputes ZIP-to-county allocation and checks headline values against the frozen master.
- `scripts/reconstruct_nppes_filter.py`: explicitly **reconstructed**, unverified extraction script for the large NPPES CSV.

## Data provenance
- NPPES NPI dissemination: https://download.cms.gov/nppes/NPI_Files.html . Dermatology taxonomy `207N00000X` was used in the historical workflow. Exact original NPPES release and additional cleaning/deduplication steps are unverified.
- HUD USPS crosswalk: https://www.huduser.gov/portal/datasets/usps_crosswalk.html (supplied file labeled 09/2025). `TOT_RATIO` used for proportional county allocation and normalized within ZIP.
- US Census Bureau county population estimates: https://www.census.gov/programs-surveys/popest.html (2020–2024 file).
- Appalachian Regional Commission county definitions and subregions: https://www.arc.gov/appalachian-counties-served-by-arc/ . **The original ARC classification spreadsheet is not included**; classification is preserved in master workbook.
- NCI State Cancer Profiles: https://statecancerprofiles.cancer.gov/ (2018–2022 incidence/mortality extracts). Suppressed or unavailable rates are missing, not zero.

## Validation
```bash
python -m pip install -r requirements.txt
python scripts/validate_repository.py
```
The validator independently reallocates the provided ZIP-level counts with the HUD `TOT_RATIO` method and compares to the frozen county-level dataset. It does **not** regenerate the original ARC assignment, the entire manuscript, or every figure.

## Optional reconstruction of NPPES ZIP-level counts
```bash
python scripts/reconstruct_nppes_filter.py path/to/npidata_pfile.csv reconstructed_zip_counts.csv
```
This script processes NPPES in chunks, selects providers with taxonomy `207N00000X` in any taxonomy column, counts unique NPIs, and uses the first five characters of the practice ZIP. These details are reconstructed assumptions; do not replace the original supplied ZIP counts without confirming exact agreement.

## Caveats before manuscript publication
- Verify original NPPES file release and reconcile any date reported in manuscript.
- Verify the manuscript's figure and text RR/CI values agree.
- Add original ARC classification input, or document an exact version/download.
- Independently reproduce all melanoma analyses and figures before claiming complete reproducibility.
- Check source dataset licenses and attribution requirements before making the repository public.
- A GitHub repository URL and Zenodo DOI can be added only **after** actual publication/archive; none is assigned in this ZIP.

## Citation
Manuscript citation, GitHub URL, and Zenodo DOI: pending.
