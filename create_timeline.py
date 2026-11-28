
import pandas as pd

df = pd.read_csv("data/so2_emissions.csv")

# Keep pounds per hour measurements
df = df[df["Unit of Measure"] == "lbs/hr"].copy()

# Convert dates
df["Report Date"] = pd.to_datetime(
    df["Report Date"],
    format="%m/%d/%Y"
)

# Convert measurements to numbers
df["Amount"] = pd.to_numeric(
    df["Amount"], errors="coerce"
)

# Calculate average emissions for each date
timeline = (
    df.groupby("Report Date")["Amount"]
    .mean()
    .reset_index()
)

timeline.to_csv("data/timeline.csv", index=False)

print("Timeline CSV created!")
print(timeline.head())
