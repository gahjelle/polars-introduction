"""Download and prepare billboard data Hadley Wickham's tidy data demo"""

# %% Imports
import pathlib

import polars as pl

# %% Set up input URL and output paths
URL = "https://raw.githubusercontent.com/hadley/tidy-data/master/data/billboard.csv"
OUTPUT_PATH_SONGS = pathlib.Path("billboard_songs.csv")
OUTPUT_PATH_RANKS = pathlib.Path("billboard_ranks.csv")

# %% Read and process dataset
import IPython

IPython.embed()
billboard = pl.scan_csv(
    URL, encoding="iso-8859-1", try_parse_dates=True["date.entered", "date.peaked"]
).rename(
    columns={
        "index": "id",
        "artist.inverted": "artist",
        "date.entered": "date_entered",
        "date.peaked": "date_peaked",
    }
)

# %% Store information about songs
billboard.loc[:, ["id", "artist", "track", "time", "genre"]].to_csv(
    OUTPUT_PATH_SONGS, index=False
)

# %% Store information about billboard ranks
(
    billboard.drop(columns=["year", "artist", "track", "time", "genre", "date_peaked"])
    .melt(id_vars=["id", "date_entered"], var_name="week", value_name="rank")
    .dropna(subset=["rank"])
    .assign(
        week=lambda df: df.week.str[1:-7].astype(int),
        date=lambda df: df.date_entered + pd.Timedelta(days=7) * (df.week - 1),
    )
    .astype({"rank": int})
    .loc[:, ["id", "date", "rank"]]
    .sort_values(by=["id", "date"])
    .to_csv(OUTPUT_PATH_RANKS, index=False)
)
