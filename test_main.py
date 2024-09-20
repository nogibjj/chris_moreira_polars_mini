import pandas as pd
import os
from unittest import mock
from main import main


def test_main_plot():
    # Sample DataFrame
    df_sample = pd.DataFrame(
        {
            "Valuation": ["$1B", "$2B", "$500M", "$1.5B"],
            "Funding": ["$500M", "$1B", "$250M", "$750M"],
            "Industry": ["Tech", "Health", "Finance", "Tech"],
        }
    )

    # Mock dataset import and data modeling
    with mock.patch("lib.dataset_import", return_value=df_sample), mock.patch(
        "lib.data_modeling", return_value=df_sample
    ), mock.patch("main.plot_value_creation_by_industry") as mock_plot:

        # Mock the print function to capture output
        with mock.patch("builtins.print") as mock_print:
            main()  # Call the main function
            mock_plot.assert_called_once()  # Ensure the plot function was called

            # Capture the print outputs
            print_outputs = [call[0][0] for call in mock_print.call_args_list]

            # Check if each statistic (std, mean, median) exists and is a number
            for line in print_outputs:
                if "Standard Deviation" in line:
                    std_value = line.split(":")[-1].strip()
                    assert std_value.replace(
                        ".", "", 1
                    ).isdigit(), "Standard deviation not a valid number"
                elif "Mean" in line:
                    mean_value = line.split(":")[-1].strip()
                    assert mean_value.replace(
                        ".", "", 1
                    ).isdigit(), "Mean not a valid number"
                elif "Median" in line:
                    median_value = line.split(":")[-1].strip()
                    assert median_value.replace(
                        ".", "", 1
                    ).isdigit(), "Median not a valid number"

            # Check if the plot was saved to the expected path
            expected_save_dir = (
                r"C:/Users/chris/Downloads/IDS706/chris_moriera_valuecreation_pandas/"
            )
            assert os.path.exists(
                expected_save_dir
            ), "Plot save directory does not exist"


if __name__ == "__main__":
    test_main_plot()
