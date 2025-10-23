# TrendAnalysis
Stock trend analysis project

## Archived files & local cleanup

As part of keeping the repository focused on the MVP scikit-learn workflow, some older or heavyweight files have been moved to an `archive/` folder. These include time-series/LSTM training scripts and model artifacts which are not required for the quick MVP.

If you need to regenerate local artifacts:

- To recreate the local sqlite database used for development (if removed): run the data collection or DB init scripts in `scripts/`.
- Preprocessing steps are in `mvp/mvp_preprocessing.py` and `scripts/data_preprocessing.py`.

If you accidentally deleted a generated file and need it back, you can retrieve it from the Git history or the `archive/` folder if preserved.

