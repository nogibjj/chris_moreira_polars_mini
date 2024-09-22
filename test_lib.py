import os
import polars as pl
from lib import (
    dataset_import,
    data_modeling,
    calculate_mean,
    calculate_median_value_creation,
    calculate_std_value_creation,
    plot_value_creation_by_industry,
)

DATASET_PATH = (
    r"C:/Users/chris/Downloads/IDS706/"
    r"chris_moreira_polars_mini/test_data/unicorn_companies.csv"
)


def test_import():
    df = dataset_import(DATASET_PATH)
    assert df is not None
    assert isinstance(df, pl.DataFrame)


def test_modeling():
    df_raw = dataset_import(DATASET_PATH)
    df_edited = data_modeling(df_raw)
    assert "value_creation" in df_edited.columns


def test_mean():
    df_raw = dataset_import(DATASET_PATH)
    df_edited = data_modeling(df_raw)
    mean_value = calculate_mean(df_edited)
    assert isinstance(mean_value, (int, float))


def test_median():
    df_raw = dataset_import(DATASET_PATH)
    df_edited = data_modeling(df_raw)
    median_value = calculate_median_value_creation(df_edited)
    assert isinstance(median_value, (int, float))


def test_std():
    df_raw = dataset_import(DATASET_PATH)
    df_edited = data_modeling(df_raw)
    std_value = calculate_std_value_creation(df_edited)
    assert isinstance(std_value, (int, float))


def test_plot():
    df_raw = dataset_import(DATASET_PATH)
    df_edited = data_modeling(df_raw)

    df_edited = df_edited.with_columns(pl.col("value_creation").cast(pl.Float64))

    save_dir = r"C:/Users/chris/Downloads/IDS706/"
    r"chris_moriera_valuecreation_pandas/"
    plot_value_creation_by_industry(df_edited, save_dir)

    assert os.path.exists(
        os.path.join(save_dir, "value_creation_boxplot.png")
    ), "Plot file was not saved"


if __name__ == "__main__":
    test_import()
    test_modeling()
    test_mean()
    test_median()
    test_std()
    test_plot()
    print("All tests passed!")
