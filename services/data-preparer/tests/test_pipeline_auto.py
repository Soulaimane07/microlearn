import pandas as pd


def test_auto_pipeline_imputes_and_keeps_rows():
    """Automatic pipeline should impute missing numeric and categorical values and keep rows."""
    from app.services.pipeline import run_pipeline

    df = pd.DataFrame({
        'id': [1, 2, 3],
        'value': [1.0, None, 3.0],
        'cat': ['a', None, 'b'],
        'date_col': ['2020-01-01', None, '2020-03-03']
    })

    processed = run_pipeline(df)

    # Should keep all rows
    assert len(processed) == 3

    # Numeric column 'value' should be imputed (no NaNs)
    assert 'value' in processed.columns
    assert processed['value'].isna().sum() == 0

    # Categorical 'cat' should be imputed/encoded and not contain NaNs
    # After encoding it may be numeric; ensure no NaNs in that column name if present
    if 'cat' in processed.columns:
        assert processed['cat'].isna().sum() == 0
