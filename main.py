import os
from lib import (
    dataset_import,
    data_modeling,
    calculate_mean,
    calculate_median_value_creation,
    calculate_std_value_creation,
    plot_value_creation_by_industry,
)


def main():
    # Load the dataset
    df_raw = dataset_import()

    # Model the data
    df_edited = data_modeling(df_raw)

    # Calculate statistics
    std_value_creation = calculate_std_value_creation(df_edited)
    mean_value_creation = calculate_mean(df_edited)
    median_value_creation = calculate_median_value_creation(df_edited)

    # Print calculated statistics (with formatting)
    print(
        f"Standard Deviation of Value Creation (in billions): "
        f"{std_value_creation:.4f}"
    )
    print(f"Mean of Value Creation (in billions): {mean_value_creation:.4f}")
    print(f"Median of Value Creation (in billions): {median_value_creation:.4f}")

    # Define the save directory for plots
    save_directory = (
        r"C:/Users/chris/Downloads/IDS706/chris_moriera_valuecreation_pandas/"
    )

    # Ensure the directory exists
    os.makedirs(save_directory, exist_ok=True)

    # Plot the data
    plot_value_creation_by_industry(df_edited, save_directory)


if __name__ == "__main__":
    main()
