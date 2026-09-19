# Household Income and Expenditure Analysis
# Data Cleaning and Basic Visualization

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv(r"C:\Practice\Household Income and Expenditure Analysis\Synthetic Data.csv")

# Basic Data Inspection
print(df.head())
print(df.shape)
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())

# Remove Missing Values
# Remove rows where Total_Household_Income is missing
df = df.dropna(subset=["Total_Household_Income"])


# Remove Duplicate Rows
df = df.drop_duplicates()

# Clean Text Columns
text_cols = [
    "Region",
    "Source_of_Income",
    "Main_Source_of_Water_Supply"
]

for col in text_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

# Expenditure Columns
expense_cols = [
    "Staple_Food_Expenditure",
    "Meat_Expenditure",
    "Seafood_Expenditure",
    "Leisure_Expenditure",
    "Alcohol_Expenditure",
    "Tobacco_Expenditure",
    "Medical_Expenditure",
    "Transportation_Expenditure",
    "Communication_Expenditure",
    "Utilities_Expenditure",
    "Education_Expenditure",
    "Crop_Farming_Expenditure"
]

# Keep only columns that exist in the dataset
expense_cols = [col for col in expense_cols if col in df.columns]

print("\nExpenditure columns used:")
print(expense_cols)

# Convert expenditure columns to numeric
for col in expense_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill missing expenditure values with 0
df[expense_cols] = df[expense_cols].fillna(0)

# Convert income to numeric
df["Total_Household_Income"] = pd.to_numeric(
    df["Total_Household_Income"],
    errors="coerce"
)

# Remove rows where income became NaN after conversion
df = df.dropna(subset=["Total_Household_Income"])

# *****************************************
# Outlier Treatment

# Cap income values above 50,000
df.loc[
    df["Total_Household_Income"] > 50000,
    "Total_Household_Income"
] = 50000

# *****************************************
# Create Total Expenditure
df["total_expenditure"] = df[expense_cols].sum(axis=1)

# *****************************************
# Create Savings
df["Savings"] = (
    df["Total_Household_Income"] -
    df["total_expenditure"]
)

# *****************************************
# Create Savings Rate
df["Savings_Rate"] = np.where(
    df["Total_Household_Income"] != 0,
    df["Savings"] / df["Total_Household_Income"],
    0
)

# *****************************************
# Flag Invalid Records
df["is_invalid"] = np.where(
    df["total_expenditure"] > df["Total_Household_Income"],
    1,
    0
)

# *****************************************
# Create Household ID
# *****************************************
if "Household_ID" not in df.columns:
    df.insert(0, "Household_ID", range(1, len(df) + 1))

# ****************************************
# Save Cleaned Dataset
# *****************************************
output_path = (
    r"C:\Practice\Household Income and Expenditure Analysis"
    r"\household_clean_python.csv"
)

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully.")
print("Final Shape:", df.shape)

# ******************************************
# Summary Statistics
# ******************************************
print("\nSummary Statistics:")
print(df[
    [
        "Total_Household_Income",
        "total_expenditure",
        "Savings",
        "Savings_Rate"
    ]
].describe())

# ******************************************
# Visualization 1: Income Distribution
# ******************************************
plt.figure(figsize=(8, 5))
plt.hist(df["Total_Household_Income"], bins=30)
plt.title("Distribution of Household Income")
plt.xlabel("Income")
plt.ylabel("Frequency")
plt.show()

# ******************************************
# Visualization 2: Total Income by Region
# ******************************************
if "Region" in df.columns:
    income_by_region = (
        df.groupby("Region")["Total_Household_Income"]
        .sum()
        .sort_values()
    )

    plt.figure(figsize=(8, 5))
    income_by_region.plot(kind="barh")
    plt.title("Total Income by Region")
    plt.xlabel("Total Income")
    plt.ylabel("Region")
    plt.show()

# ******************************************
# Visualization 3: Income vs Expenditure
# ******************************************
plt.figure(figsize=(8, 5))
plt.scatter(
    df["Total_Household_Income"],
    df["total_expenditure"],
    alpha=0.5
)
plt.title("Income vs Total Expenditure")
plt.xlabel("Total Household Income")
plt.ylabel("Total Expenditure")
plt.show()

# ******************************************
# Visualization 4: Correlation Heatmap
# ******************************************
heatmap_cols = [
    "Total_Household_Income",
    "total_expenditure",
    "Savings",
    "Savings_Rate",
    "Staple_Food_Expenditure",
    "Medical_Expenditure",
    "Utilities_Expenditure"
]

# Keep only columns that exist
heatmap_cols = [col for col in heatmap_cols if col in df.columns]

corr = df[heatmap_cols].corr()

plt.figure(figsize=(8, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

# ****************
# KPI Summary
# *****************
print("\nKPI Summary")
print("Total Income:", df["Total_Household_Income"].sum())
print("Total Expenditure:", df["total_expenditure"].sum())
print("Total Savings:", df["Savings"].sum())

savings_rate = (
    df["Savings"].sum() /
    df["Total_Household_Income"].sum()
)

print("Savings Rate:", savings_rate)
print("Number of Households:", len(df))