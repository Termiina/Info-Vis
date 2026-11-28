
import pandas as pd
import re

source = "data/Air_Quality.csv"

columns = [
    "Facility Name", "Pollutant", "Amount",
    "Unit of Measure", "Report Date",
    "County Name", "City",
    "Latitude Degrees", "Latitude Minutes",
    "Latitude Seconds", "Longitude Degrees",
    "Longitude Minutes", "Longitude seconds",
    "Georeferenced Latitude & Longitude"
]

locations = set()
first_chunk = True

for chunk in pd.read_csv(
    source, usecols=columns, chunksize=100000
):
    # Keep only sulfur dioxide records
    so2 = chunk[chunk["Pollutant"] == "SO2"].copy()

    if so2.empty:
        continue

    # Save timeline data
    so2[[
        "Facility Name", "Amount",
        "Unit of Measure", "Report Date",
        "County Name", "City"
    ]].to_csv(
        "data/so2_emissions.csv",
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False

    # Extract map coordinates
    for _, row in so2.iterrows():
        point = row["Georeferenced Latitude & Longitude"]
        match = re.search(
            r"POINT\s*\(([-\d.]+)\s+([-\d.]+)\)",
            str(point)
        )

        if match:
            lon, lat = map(float, match.groups())
        else:
            try:
                lat = (
                    float(row["Latitude Degrees"])
                    + float(row["Latitude Minutes"]) / 60
                    + float(row["Latitude Seconds"]) / 3600
                )

                lon_deg = float(row["Longitude Degrees"])
                lon = (
                    lon_deg
                    - (1 if lon_deg < 0 else -1) *
                    (
                        float(row["Longitude Minutes"]) / 60
                        + float(row["Longitude seconds"]) / 3600
                    )
                )
            except (ValueError, TypeError):
                continue

        locations.add((
            row["Facility Name"], row["County Name"],
            row["City"], lat, lon
        ))

# Save unique monitoring locations
pd.DataFrame(
    locations,
    columns=[
        "Facility Name", "County Name",
        "City", "Latitude", "Longitude"
    ]
).to_csv("data/so2_locations.csv", index=False)

print("Finished processing SO2 data!")
print("Created so2_emissions.csv")
print("Created so2_locations.csv")
