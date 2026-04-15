# yttg-cli

## Prerequisites

- [Python](https://www.python.org/) 3.14 or newer

## Installation

First, clone the repo to the target machine

```shell
git clone https://github.com/BesserwisserErsterKlasse/yttg-cli
```

Change into the project directory

```shell
cd yttg-cli
```

Create a virtual environment

```shell
python3.14 -m venv .venv
```

And activate it

- On Linux / macOS

```shell
source .venv/bin/activate
```

- On Windows (PowerShell)

```shell
.venv\Scripts\Activate.ps1
```

Install the dependencies

```shell
pip install -e .
```

Run the `main.py` file

```shell
python -O src/main.py
```

**Note:** `-O` is an optional flag that removes unnecessary `assert`s — you can omit it and run `python src/main.py`

## License

yttg-cli is a free, open-source software distributed under the [GPLv3 License](LICENSE.txt)
