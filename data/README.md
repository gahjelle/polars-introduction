# Datasets for Introduction to pandas

The **Introduction to pandas** workshop uses three public datasets in demonstrations and exercises.

## Postal Codes in Poland

- **Description:** <https://www.geonames.org/postalcode-search.html?country=pl>
- **Original data:** <https://download.geonames.org/export/zip/PL.zip>
- **Prepared data:** [`postal_codes.csv`](postal_codes.csv)

[`prepare_postal_codes.py`](prepare_postal_codes.py) downloads and converts the original data.

Postal code data are from the [GeoNames geographical database](https://www.geonames.org/) and licensed under a [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/).

## Top 100 Billboard in the year 2000

- **Description:** <https://tidyr.tidyverse.org/reference/billboard.html>
- **Original data:** <https://raw.githubusercontent.com/hadley/tidy-data/master/data/billboard.csv>
- **Prepared data:** [`billboard_songs.csv`](billboard_songs.csv), [`billboard_ranks.csv`](billboard_ranks.csv)

[`prepare_billboard.py`](prepare_billboard.py) downloads and converts the original data.
