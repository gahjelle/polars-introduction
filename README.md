# Introduction to Polars

This repository contains material for the tutorial I presented at the [EuroSciPy 2024](https://www.euroscipy.org/2024/) conference in Szczecin.

## Topics

The tutorial cover the following topics:

1. DataFrames as Panels of Data
2. Create DataFrames
3. Work With Tidy Data
4. Manipulate DataFrames
5. Share Results and Insights
6. Lazy DataFrames

The workshop consists of 90 minutes of live code demonstrations and hands-on exercises.

## Data

The demos and examples use three public datasets:

1. [`data/postal_codes.csv`](data/postal_codes.csv): Postal Codes in Poland
2. [`data/billboard_songs.csv`](data/billboard_songs.csv) and [`data/billboard_ranks.csv`](data/billboard_ranks.csv): Top 100 songs on Billboard in 2000
3. [`data/schedule.csv`](data/schedule.csv): Workshop schedule

See [`data/`](data/) for more information, including licenses and links to the original datasets.

## Preparations

You should create a virtual environment and install Polars and other necessary dependencies.

> **Note:** Demonstrations were done on Linux Ubuntu with Python 3.12.5 and packages and versions specified in [`requirements.txt`](requirements.txt).

### Conda/Anaconda

If you're running **Anaconda** or **Miniconda**, you should set up a separate environment for this tutorial. You can use `conda` to do so:

```console
$ conda env create -n euroscipy-polars -f environment.yml
$ conda activate euroscipy-polars
```

Remember to activate your Conda environment.

### Pip

If you're using a plain Python distribution, then you can use `venv` to create a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/):

```console
$ python -m venv venv
$ source venv/bin/activate
(venv) $ python -m pip install -r requirements.in
```

On Windows, you don't need `source` when activating your virtual environment. You can type `venv\Scripts\activate` instead.

## Demonstrations

The workshop mostly consists of live code demonstrations. You can find simple notes from the demos in the file [`polars_introduction.py`](polars_introduction.py). Use `jupytext` to convert the notes to a Jupyter Notebook if you prefer.

---

Demonstration code, exercises, and solutions are licensed under an [MIT license](LICENSE).
