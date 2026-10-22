# Appalachia Dermatology Workforce Study

County-level analysis of dermatologist access and melanoma outcomes in Appalachian and non-Appalachian US counties.

**Status: repository is being populated.** The complete data and notebook remain in the downloadable archive; they have not yet been uploaded to GitHub. Do not cite this as a complete reproducibility repository.

## Data sources
NPPES; HUD USPS ZIP-to-county crosswalk (September 2025); Census 2024 county population; Appalachian Regional Commission county definitions; NCI State Cancer Profiles (2018–2022).

## Validated workforce results
25,392 ZIP-level dermatologists; 25,358 allocated; 3,235 counties (423 Appalachian); 4.79 vs 7.67 dermatologists per 100,000; 186 vs 1,358 zero-dermatologist counties. County allocation reproduced the frozen master workbook exactly. Melanoma outcomes are not yet independently validated.

## Methodology and caveats
NPPES dermatology taxonomy 207N00000X; ZIP counts proportionally allocated to counties using normalized HUD TOT_RATIO. Exact original NPPES release is unverified. The original ARC spreadsheet is not separately included. The original notebook is exploratory and includes machine-specific paths. No Zenodo DOI is assigned.

## Complete archive
Upload the contents of the provided Appalachia_Dermatology_GitHub_Ready.zip to this repository root (not its enclosing folder). Preserve the data/, notebooks/, and scripts/ directories. Run `python -m pip install -r requirements.txt` then `python scripts/validate_repository.py`.
