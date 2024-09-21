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


def plot_value_creation_by_industry(df, save_directory):
    # Check if value_creation is in the expected format, if not, create it
    if "value_creation" not in df.columns:
        raise ValueError("The DataFrame does not contain a 'value_creation' column.")

    # Extract industries and value creation directly
    industries = df["Industry"].to_list()
    value_creation = df["value_creation"].to_list()

    # Create a new DataFrame for plotting
    plot_df = pl.DataFrame(
        {"Industry": industries, "Value Creation": value_creation}
    ).to_pandas()  # Convert to pandas for Seaborn compatibility

    # Create the boxplot
    plt.figure(figsize=(12, 6))  # Optional: Adjust figure size for better visualization
    sns.boxplot(
        x="Industry",
        y="Value Creation",
        data=plot_df,
        palette="Spectral",
        hue="Industry",
        legend=False,
    )
    plt.title("Value Creation by Industry")
    plt.xlabel("Industry")
    plt.ylabel("Value Creation (in billions)")
    plt.xticks(rotation=45)  # Rotate x labels for better readability
    plt.tight_layout()  # Adjust layout to prevent clipping

    # Save the plot
    plt.savefig(os.path.join(save_directory, "value_creation_boxplot.png"))
    plt.close()  # Close the plot to free memory


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
