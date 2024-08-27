"""Download and prepare data about postal codes in Switzerland"""

# %% Imports
import io
import pathlib
import tempfile
import zipfile

import polars as pl
import requests

# %% Download Poland data from geonames.org
COUNTRY = "PL"
URL = f"https://download.geonames.org/export/zip/{COUNTRY}.zip"
OUTPUT_PATH = pathlib.Path("postal_codes.csv")

# %% Download ZIP file from server
response = requests.get(URL)
if not response:
    response.raise_for_status()


# %% Read postal codes from ZIP file
with zipfile.ZipFile(io.BytesIO(response.content), mode="r") as archive:
    raw_codes = archive.read(f"{COUNTRY}.txt")

# Save the postal code to a temporary file
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = pathlib.Path(temp_dir) / "raw_codes.csv"
    temp_path.write_bytes(raw_codes)

    # %% Parse postal codes into a DataFrame and save them to disk
    (
        pl.scan_csv(
            temp_path,
            has_header=False,
            separator="\t",
            new_columns=[
                "country",
                "postal_code",
                "name",
                "province",
                "province_code",
                "district",
                "district_code",
                "municipality",
                "municipality_code",
                "latitude",
                "longitude",
                "accuracy",
            ],
        )
        .select(pl.all().exclude("accuracy"))
        .sink_csv(OUTPUT_PATH)
    )
