# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Introduction to Polars
#
# **EuroSciPy 2024, Szczecin**
#
# Contact: **Geir Arne Hjelle**, `geirarne@gmail.com`, <https://github.com/gahjelle/polars-introduction>
#
# **Agenda:**
#
# 1. DataFrames for Structuring Data
# 2. Create DataFrames
# 3. Work With Tidy Data
# 4. Manipulate DataFrames
# 5. Share Results and Insights
# 6. Saving the Best for Last: Polars is Lazy!

# %% [markdown]
# ## DataFrames for Structuring Data
#
# A **DataFrame** is the main data structure used in Polars. A DataFrame is analogous to a structured spread sheet. In particular:
#
# - A DataFrame is a **two-dimensional** table of rows and columns
# - Each column has a **name**
# - All values in a column have the **same data type**
# - Each row group related data
#
# Here are some examples of tables organized as DataFrames:
#
# | Time                | Room 6                                                        | Room 5                                                                     |
# | :------------------ | :------------------------------------------------------------ | :------------------------------------------------------------------------- |
# | 2024-08-26 09:00:00 | Introduction to Python                                        | What is the magic of magic methods in the Python language?                 |
# | 2024-08-26 11:00:00 | Introduction to NumPy                                         | Decorators - A deep dive                                                   |
# | 2024-08-26 14:00:00 | Introduction to matplotlib for data visualization with Python | Probabilistic classification and cost-sensitive learning with scikit-learn |
# | 2024-08-26 16:00:00 | Image Analysis in Python with scikit-image                    | Using the Array API to write code that runs with NumPy, Cupy, and PyTorch  |
# | 2024-08-27 09:00:00 | Introduction to Polars: Fast and readable data analysis       | Building robust workflows with strong provenance                           |
# | 2024-08-27 11:00:00 | Using Wikipedia as a language corpus for NLP                  | Combining Python and Rust to create Polars plugins                         |
# | 2024-08-27 14:00:00 | Introduction to machine learning with scikit-learn and pandas | Multi-dimensional arrays with Scipp                                        |
# | 2024-08-27 16:00:00 | A hitchhiker's guide to contributing to open source           | sktime - Python toolbox for time series                                    |
#
# A subset of the data can be presented as follows:
#
# | Room | 09:00                                                   | 11:00                                              | 14:00                                                         | 16:00                                               |
# | :--- | :------------------------------------------------------ | :------------------------------------------------- | :------------------------------------------------------------ | :-------------------------------------------------- |
# | 6    | Introduction to Polars: Fast and readable data analysis | Using Wikipedia as a language corpus for NLP       | Introduction to machine learning with scikit-learn and pandas | A hitchhiker's guide to contributing to open source |
# | 5    | Building robust workflows with strong provenance        | Combining Python and Rust to create Polars plugins | Multi-dimensional arrays with Scipp                           | sktime - Python toolbox for time series             |
#

# %% [markdown]
# ## Create DataFrames
#
# At a high level, you can create DataFrames in two ways:
#
# 1. From an existing Python data structure in memory, typically nested `dict` and/or `list`
# 2. From a data source like a file, database, etc
#
# You use `pl.DataFrame()` to convert an existing Python data structure. There are several `read_*()` and `scan_*()` functions in Polars that construct DataFrames from different data sources.

# %%
import polars as pl

# %%
# Create a DataFrame from a list of dictionaries
tutorials = [
    {
        "time": "09:00",
        "room_6": "Introduction to Polars: Fast and readable data analysis",
        "room_5": "Building robust workflows with strong provenance",
    },
    {
        "time": "11:00",
        "room_6": "Using Wikipedia as a language corpus for NLP",
        "room_5": "Combining Python and Rust to create Polars plugins",
    },
    {
        "time": "14:00",
        "room_6": "Introduction to machine learning with scikit-learn and pandas",
        "room_5": "Multi-dimensional arrays with Scipp",
    },
    {
        "time": "16:00",
        "room_6": "A hitchhiker's guide to contributing to open source",
        "room_5": "sktime - Python toolbox for time series",
    },
]

pl.DataFrame(tutorials)

# %%
# Create a DataFrame from a dictionary of lists
tutorials = {
    "time": ["09:00", "11:00", "14:00", "16:00"],
    "room_6": [
        "Introduction to Polars: Fast and readable data analysis",
        "Using Wikipedia as a language corpus for NLP",
        "Introduction to machine learning with scikit-learn and pandas",
        "A hitchhiker's guide to contributing to open source",
    ],
    "room_5": [
        "Building robust workflows with strong provenance",
        "Combining Python and Rust to create Polars plugins",
        "Multi-dimensional arrays with Scipp",
        "sktime - Python toolbox for time series",
    ],
}
pl.DataFrame(tutorials)

# %%
# Create a DataFrame from a CSV file
pl.read_csv("data/billboard_songs.csv")

# %%
[function for function in dir(pl) if function.startswith("read_")]

# %% [markdown]
# You can also read files directly from the Internet by supplying a URL. Some sites have extra support, like for
# example [Hugging Face](https://huggingface.co/docs/hub/en/datasets-polars) with a special `hf://` protocol.

# %%
pl.read_csv(
    "hf://datasets/commoncrawl/statistics/tlds.csv"
)

# %%
pl.read_parquet(
    "hf://datasets/commoncrawl/statistics@~parquet/Top-level domains/train/0000.parquet"
)

# %% [markdown]
# ## Work With Tidy Data
#
# Hadley Wickham introduced the term **tidy data** (<https://tidyr.tidyverse.org/articles/tidy-data.html>). Data tidying is a way to **structure DataFrames to facilitate analysis**.
#
# A DataFrame is tidy if:
#
# - Each variable is a column
# - Each observation is a row
# - Each DataFrame contains one observational unit
#
# Note that tidy data principles are closely tied to normalization of relational databases.
#
# Is the following DataFrame tidy?

# %%
schedule = pl.DataFrame(tutorials)
schedule

# %% [markdown]
# What about the following DataFrame?

# %%
schedule.transpose(include_header=True, header_name="room", column_names="time")

# %% [markdown]
# What are the variables in the dataset? Time slots, rooms, and tutorial titles. They should each be their own column. Tidy the dataset:

# %%
(
    schedule.unpivot(index="time", variable_name="room", value_name="title").sort(
        by=["time", "room"]
    )
)

# %% [markdown]
# Being conscious of tidy data lets you standardize your **data cleaning** and **analysis**:
#
# 1. Tidy your data set
# 2. Clean your data (e.g. check outliers, parse dates, impute missing values)
# 3. Analyze
# 4. Share and visualize
#
# **Note:** Datasets from Hadley Wickham's Tidy Data paper are at <https://github.com/hadley/tidy-data/tree/master/data>

# %% [markdown]
# ## Manipulate DataFrames
#
# Polars DataFrames have many methods you can use to manipulate your data, and
# you'll explore some of them now. In a tidy workflow, you think about methods
# in different categories:
#
# - **Filter:** remove observations
# - **Transform:** add or modify variables based on existing variables
# - **Aggregate:** collapse multiple values into a single value
# - **Sort:** change the order of observations
#
# Polars uses the concept of **contexts** which map fairly nicely with the tidy categories:
#
# - **Selection**
# - **Filter**
# - **Group by / Aggregation**

# %%
schedule = pl.read_csv("data/schedule.csv", try_parse_dates=True)
schedule

# %%
songs = pl.read_csv("data/billboard_songs.csv")
ranks = pl.read_csv("data/billboard_ranks.csv", try_parse_dates=True)
songs

# %% [markdown]
# ### Filter

# %%
songs.select(pl.col("artist", "track", "time"))

# %%
schedule.select(pl.col("timestamp", "title"))

# %%
schedule.select(pl.all().exclude("room"))

# %%
schedule.filter(pl.col("room") == 5)

# %%
schedule.filter(pl.col("timestamp").dt.hour() == 11)

# %%
schedule.filter(pl.col("title").str.starts_with("Intro"))

# %%
schedule.filter(pl.col("title").str.contains("scikit"))

# %%
songs.filter(pl.col("artist") == "Jay-Z").select(pl.col("track", "time"))

# %%
ranks.select(pl.col(pl.Int64))

# %% [markdown]
# ### Aggregate

# %%
ranks.sum()

# %%
ranks.select(pl.col(pl.Int64)).mean()

# %%
ranks.group_by("id").agg(pl.len())  #.sort(by=pl.col("len"), descending=True)

# %%
ranks.group_by("id").agg(pl.first("date", "rank"))

# %%
ranks.group_by("id").agg(pl.first("date"), pl.min("rank"))

# %%
ranks.group_by("id").agg(
    pl.first("date").alias("date_entered"), pl.min("rank").alias("best_rank")
)

# %%
billboard = songs.join(ranks, left_on="id", right_on="id", how="inner")
billboard

# %%
for song_id, info in billboard.group_by("id"):
    if info["rank"].min() == 1:
        print(info.filter(pl.col("rank") == 1))

# %% [markdown]
# ### Transform

# %%
schedule.select(
    pl.col("timestamp").dt.date().alias("date"),
    pl.col("timestamp").dt.time().alias("time"),
    pl.col("room"),
    pl.col("title"),
)

# %%
schedule.with_columns(
    pl.col("timestamp").dt.date().alias("date"),
    pl.col("timestamp").dt.time().alias("time"),
).drop("timestamp")

# %%
(
    billboard.group_by("id", artist="artist", track="track")
    .agg(
        pl.col("date").min().alias("date_entered"),
        pl.col("rank").min().alias("peak_position"),
        pl.col("rank").len().alias("num_weeks"),
        pl.col("rank").mean().alias("avg_position"),
    )
    .with_columns((pl.col("num_weeks") * (100 - pl.col("avg_position"))).alias("score"))
)

# %% [markdown]
# ### Sort

# %%
scored_billboard = (
    billboard.group_by("id", artist="artist", track="track")
    .agg(
        pl.col("date").min().alias("date_entered"),
        pl.col("rank").min().alias("peak_position"),
        pl.col("rank").len().alias("num_weeks"),
        pl.col("rank").mean().alias("avg_position"),
    )
    .with_columns((pl.col("num_weeks") * (100 - pl.col("avg_position"))).alias("score"))
)


# %%
scored_billboard.sort(by="id")

# %%
scored_billboard.sort(by=pl.col("artist"))

# %%
scored_billboard.sort(by=pl.col("artist").str.to_lowercase())

# %%
scored_billboard.sort(by="num_weeks", descending=True)

# %%
scored_billboard.sort(by=["peak_position", "num_weeks"], descending=[False, True])

# %%
scored_billboard.sort(by=pl.col("score"), descending=True)

# %% [markdown]
# ## Share Results and Insights
#
# When you want to share your insights, you often want to **untidy** your data again:

# %%
schedule.pivot(on="room", index="timestamp", values="title")

# %% [markdown]
# In the same way you can use Polars to read from many different data sources, you can also write to many different outputs, both in memory and on file.

# %%
[
    method
    for method in dir(schedule)
    if method.startswith("to_") or method.startswith("write_")
]

# %%
(
    scored_billboard.sort(by="score", descending=True)
    .head(10)
    .select(pl.col("artist", "track", "num_weeks"))
    .write_csv("top_songs_2000.csv")
)

# %%
ranks.plot.scatter(x="date", y="rank", alpha=0.4)

# %%
from IPython.display import display

for id, group in billboard.filter(pl.col("id") < 5).group_by("id", maintain_order=True):
    display(
        group.plot.line(x="date", y="rank", title=f"{group.item(0, "artist")} - {group.item(0, "track")}")
        * group.plot.scatter(x="date", y="rank", marker="+")
    )

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Saving the Best for Last: Polars is Lazy!
#
# Polars fully supports so-called **lazy data frames** with `pl.LazyFrame()`. In a lazy data frame, no calculations are performed until necessary. This allows Polars to optimize the calculations and increase performance, often significantly.
#
# You should prefer lazy frames over eager frames in most cases! One notable exception is when you're doing exploratory work (or teaching a tutorial) where quickly iterating on your code is more important than the speed of calculations.
#
# To create a lazy data frame, you can do one of the following:
#
# - Read data with `scan_*()` instead of `read_*()`
# - Construct a data frame with `pl.LazyFrame()` instead of `pl.DataFrame()`
# - Convert an eager data frame by calling `.lazy()`

# %%
pl.scan_csv("data/schedule.csv")

# %%
pl.LazyFrame(tutorials)

# %%
billboard.lazy()

# %% [markdown]
# Look at some simple manipulation of the schedule:

# %%
tuesday_intro = (
    pl.scan_csv("data/schedule.csv")
    .with_columns(title=pl.col("title").str.to_uppercase())
    .filter(pl.col("timestamp") >= "2024-08-27")
)

# %% [markdown]
# At this point, no calculations have been made. The file hasn't even been read! You can explicitly tell Polars to run the query by calling `.collect()`:

# %%
tuesday_intro.collect()

# %% [markdown]
# Look again at the lazy data frame. Jupyter displays a query plan, which describes which calculations that will be carried out. However, note the comment about an **optimized** query plan:

# %%
tuesday_intro

# %%
tuesday_intro.show_graph()

# %% [markdown]
# Polars can do [several optimizations](https://docs.pola.rs/user-guide/lazy/optimizations/) before carrying out a query. In this case, it has realized that the filtering can be done earlier - actually while reading the file from disk - instead of first upper-casing many titles just to filter them out later!

# %% [markdown]
# ## Next Steps
#
# While Polars is still somewhat new, it recently reached its [**Version 1** milestone](https://pola.rs/posts/announcing-polars-1/) and is production ready!
#
# - [Polars documentation](https://docs.pola.rs/)
# - [Modern Polars](https://kevinheavey.github.io/modern-polars/): Comparison to pandas based on the [Modern pandas](http://tomaugspurger.net/posts/modern-1-intro/) blog post
# - [Effective Polars](https://store.metasnake.com/effective-polars): Book by Matt Harrison
# - [Polars Workshop](https://justinbois.github.io/dd-pol/2024/part_1/lessons/01/intro_to_polars.html): Notes by Justin Bois
# - [Great tables](https://posit-dev.github.io/great-tables/blog/polars-styling/): Present Polars data frames as beautiful tables

# %%
from great_tables import GT, loc, style

schedule_table = (
    schedule.pivot(on="room", index="timestamp", values="title")
    .select(
        pl.col("timestamp").dt.date().alias("Date"),
        pl.col("timestamp").dt.time().alias("Time"),
        pl.col("6").alias("Room 6"),
        pl.col("5").alias("Room 5"),
    )
)

(
    GT(schedule_table)
    .tab_header(
        title="EuroSciPy 2024",
        subtitle="Tutorials in Szczecin",
    )
    .tab_spanner(
        label="When",
        columns=["Date", "Time"],
    )
    .tab_style(
        style.text(weight="bold"),
        loc.body("Room 6", pl.col("Room 6").str.contains("Polars"))
    )
)
