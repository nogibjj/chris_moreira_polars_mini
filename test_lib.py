import pytest
from lib import (
    dataset_import,
    calculate_mean,
    calculate_median_value_creation,
    calculate_std_value_creation,
    plot_value_creation_by_industry,
)


# Test cases for dataset_import
def test_dataset_import():
    path = "test_data/unicorn_companies.csv"
    df = dataset_import(path)
    assert not df.isnull().values.any()  # Check if dataset contains any null values
    assert len(df) > 0  # Ensure dataset is not empty


# Test cases for calculate_mean
def test_calculate_mean():
    data = [1, 2, 3, 4, 5]
    mean = calculate_mean(data)
    assert mean == 3  # Mean of the dataset


# Test cases for calculate_median_value_creation
def test_calculate_median_value_creation():
    data = [1, 2, 3, 4, 5]
    median = calculate_median_value_creation(data)
    assert median == 3  # Median of the dataset


# Test cases for calculate_std_value_creation
def test_calculate_std_value_creation():
    data = [1, 2, 3, 4, 5]
    std = calculate_std_value_creation(data)
    assert round(std, 2) == 1.58  # Standard deviation


# Test cases for plot_value_creation_by_industry
@pytest.mark.skip(reason="Skipping plot testing in automated environments")
def test_plot_value_creation_by_industry():
    df_edited_o = dataset_import("test_data/unicorn_companies.csv")
    save_directory = "test_plots/"
    plot_value_creation_by_industry(df_edited_o, save_directory)
    # No assertion, just ensure no errors in the plot generation
