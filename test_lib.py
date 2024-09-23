import pytest
import polars as pl  # Make sure to import Polars
from lib import (
    dataset_import,
    calculate_mean,
    calculate_median_value_creation,
    calculate_std_value_creation,
    plot_value_creation_by_industry,
)


def test_dataset_import():
    path = "test_data/unicorn_companies.csv"
    df = dataset_import(path)
    assert not df.null_count().any()  # Updated from is_null() to null_count()


def test_calculate_mean():
    data = pl.DataFrame({"value_creation": [1, 2, 3, 4, 5]})
    mean = calculate_mean(data)
    assert mean == 3.0


def test_calculate_median_value_creation():
    data = pl.DataFrame({"value_creation": [1, 2, 3, 4, 5]})
    median = calculate_median_value_creation(data)
    assert median == 3.0


def test_calculate_std_value_creation():
    data = pl.DataFrame({"value_creation": [1, 2, 3, 4, 5]})
    std = calculate_std_value_creation(data)
    assert std == pytest.approx(1.41421356, rel=1e-9)


# Test cases for plot_value_creation_by_industry
@pytest.mark.skip(reason="Skipping plot testing in automated environments")
def test_plot_value_creation_by_industry():
    df_edited_o = dataset_import("test_data/unicorn_companies.csv")
    save_directory = "test_plots/"
    plot_value_creation_by_industry(df_edited_o, save_directory)
    # No assertion, just ensure no errors in the plot generation
