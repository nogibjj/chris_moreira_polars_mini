import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import os


def dataset_import(path):
    """Load dataset from a CSV file."""
    return pl.read_csv(path)


def data_modeling(df):
    """Modeling the dataset by cleaning and calculating 'value_creation'."""
    df_edited = df.drop_nulls(subset=["Valuation", "Funding"])

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
    """Calculate the mean of the 'value_creation' column."""
    return df_edited.select(pl.col("value_creation").mean()).to_numpy()[0][0]


def calculate_median_value_creation(df_edited):
    """Calculate the median of the 'value_creation' column."""
    return df_edited.select(pl.col("value_creation").median()).to_numpy()[0][0]


def calculate_std_value_creation(df_edited):
    """Calculate the standard deviation of the 'value_creation' column."""
    return df_edited.select(pl.col("value_creation").std()).to_numpy()[0][0]


def plot_value_creation_by_industry(df, save_directory):
    """Plot value creation by industry and save the plot."""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Convert Polars DataFrame to Pandas DataFrame for Seaborn plotting
    df_pandas = df.to_pandas()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Industry", y="value_creation", data=df_pandas, palette="coolwarm")
    plt.ylim(0, 50)
    plt.xticks(rotation=45, ha="right")
    plt.title("Value Creation by Industry")
    plt.tight_layout()
    plt.show()

    # Save the plot
    file_path = os.path.join(save_directory, "value_creation_by_industry.png")
    plt.savefig(file_path)
    plt.close()


# Specify the path to the CSV file
csv_path = "test_data/unicorn_companies.csv"  # Update this path as needed
df_raw_o = dataset_import(csv_path)
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
