import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def dataset_import(file_path=None):
    if file_path is None:
        base_path = os.getcwd()  # Get current working directory
        file_path = os.path.join(base_path, "test_data", "unicorn_companies.csv")
    df_raw = pl.read_csv(file_path)
    return df_raw


def data_modeling(df_raw):
    df_edited = df_raw.drop_nulls(subset=["Valuation", "Funding"])

    # Clean up the dollar sign and extract unit
    df_edited = df_edited.with_columns(
        [
            pl.col("Funding").str.replace(r"[$,]", "").alias("Funding_clean"),
            pl.col("Valuation").str.replace(r"[$,]", "").alias("Valuation_clean"),
        ]
    )

    # Extract numeric values and units
    df_edited = df_edited.with_columns(
        [
            pl.col("Funding_clean")
            .str.extract(r"(\d+)([MB])", 1)
            .cast(pl.Float64)
            .alias("funding_value"),
            pl.col("Funding_clean")
            .str.extract(r"(\d+)([MB])", 2)
            .alias("funding_unit"),
            pl.col("Valuation_clean")
            .str.extract(r"(\d+)([MB])", 1)
            .cast(pl.Float64)
            .alias("valuation_value"),
            pl.col("Valuation_clean")
            .str.extract(r"(\d+)([MB])", 2)
            .alias("valuation_unit"),
        ]
    )

    # Adjust values based on units
    df_edited = df_edited.with_columns(
        [
            (
                pl.when(pl.col("funding_unit") == "B")
                .then(pl.col("funding_value") * 1e9)
                .otherwise(pl.col("funding_value") * 1e6)
            ).alias("funding_value"),
            (
                pl.when(pl.col("valuation_unit") == "B")
                .then(pl.col("valuation_value") * 1e9)
                .otherwise(pl.col("valuation_value") * 1e6)
            ).alias("valuation_value"),
        ]
    )

    # Compute value creation in billions
    df_edited = df_edited.with_columns(
        ((pl.col("valuation_value") - pl.col("funding_value")) / 1e9).alias(
            "value_creation"
        )
    )

    return df_edited


def calculate_mean(df_edited):
    return df_edited["value_creation"].mean()


def calculate_median_value_creation(df_edited):
    return df_edited["value_creation"].median()


def calculate_std_value_creation(df_edited):
    return df_edited["value_creation"].std()


def plot_value_creation_by_industry(df_edited, save_dir):
    plt.figure(figsize=(12, 8))

    industries = df_edited["Industry"].to_list()
    value_creation = df_edited["value_creation"].to_list()

    # Create a boxplot with hue set to industries
    sns.boxplot(hue=industries, y=value_creation, palette="Spectral", legend=False)

    plt.title("Value Creation Variability per Industry", fontsize=16, fontweight="bold")
    plt.xlabel("Industry", fontsize=14)
    plt.ylabel("Value Creation (in Billions)", fontsize=14)

    plt.xticks(rotation=45, ha="right")
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    plot_path = os.path.join(save_dir, "value_creation_boxplot.png")
    plt.savefig(plot_path)
    plt.show()

    print(f"Plot saved to: {plot_path}")


# Call the functions to load and process the data
df_raw_o = dataset_import()
df_edited_o = data_modeling(df_raw_o)

# Calculate and print statistics
std_value_creation = calculate_std_value_creation(df_edited_o)
print("Standard Deviation of Value Creation (in billions):", std_value_creation)

mean_value_creation = calculate_mean(df_edited_o)
print("Mean of Value Creation (in billions):", mean_value_creation)

median_value_creation = calculate_median_value_creation(df_edited_o)
print("Median of Value Creation (in billions):", median_value_creation)

save_directory = r"C:/Users/chris/Downloads/IDS706/chris_moriera_valuecreation_pandas/"
plot_value_creation_by_industry(df_edited_o, save_directory)
