import polars as pl
import os
import sys
from unittest import mock, TestCase

# Ensure the directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main function from main.py
from main import main  # Import only the main function


class TestMain(TestCase):
    def test_main_plot(self):
        df_sample = pl.DataFrame(
            {
                "Valuation": [1.0, 2.0, 0.5, 1.5],
                "Funding": [0.5, 1.0, 0.25, 0.75],
                "Industry": ["Tech", "Health", "Finance", "Tech"],
            }
        )

        # Mock dataset import and data modeling from the 'lib' module
        with mock.patch("lib.dataset_import", return_value=df_sample), mock.patch(
            "lib.data_modeling", return_value=df_sample
        ), mock.patch(
            "main.plot_value_creation_by_industry"  # Mocking plot function
        ) as mock_plot:

            with mock.patch("builtins.print") as mock_print:
                main()  # Directly call the imported main function

                print("Main function executed.")
                print(f"Plot function called {mock_plot.call_count} times.")
                mock_plot.assert_called_once()

                print_outputs = [call[0][0] for call in mock_print.call_args_list]

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

                expected_save_dir = r"C:/Users/chris/Downloads/IDS706/chris_moriera_valuecreation_pandas/"
                assert os.path.exists(
                    expected_save_dir
                ), "Plot save directory does not exist"


if __name__ == "__main__":
    TestMain().test_main_plot()
