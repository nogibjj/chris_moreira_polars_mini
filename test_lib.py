import polars as pl
import pytest
from lib import (
    dataset_import,
    calculate_mean,
    calculate_median_value_creation,
    calculate_std_value_creation,
    plot_value_creation_by_industry,  # Ensure this is imported
)


def test_dataset_import():
    """Test that the dataset is loaded without nulls."""
    path = "test_data/unicorn_companies.csv"
    df = dataset_import(path)
    assert df.null_count().sum().sum() == 0  # Correctly check for null values


def test_calculate_mean():
    """Test the mean calculation."""
    data = pl.DataFrame({"value_creation": [1, 2, 3, 4, 5]})
    result = calculate_mean(data)
    assert result == 3.0  # Expected mean


def test_calculate_median_value_creation():
    """Test the median calculation."""
    data = pl.DataFrame({"value_creation": [1, 2, 3, 4, 5]})
    result = calculate_median_value_creation(data)
    assert result == 3.0  # Expected median


def test_calculate_std_value_creation():
    """Test the standard deviation calculation."""
    data = pl.DataFrame({"value_creation": [1, 2, 3, 4, 5]})
    result = calculate_std_value_creation(data)
    assert result == pytest.approx(1.5811388300841898, rel=1e-9)  # Updated expected std


# Test cases for plot_value_creation_by_industry
@pytest.mark.skip(reason="Skipping plot testing in automated environments")
def test_plot_value_creation_by_industry():
    df_edited_o = dataset_import("test_data/unicorn_companies.csv")
    save_directory = "test_plots/"
    plot_value_creation_by_industry(df_edited_o, save_directory)
    # No assertion, just ensure no errors in the plot generation
