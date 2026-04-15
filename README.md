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

## Run

Create `.env` file in the project's root and define the `CRYPTO__PRE_SHARED_SECRET` environment variable

```env
CRYPTO__PRE_SHARED_SECRET="your-random-shared-secret"
```

This value should be a securely generated random string. It is used as a pre-shared secret for cryptographic operations.

For example, you can use this command to generate it

```shell
openssl rand -hex 32
```

**Important:** The same secret must be configured on both the client and the server.

Run the `main.py` file

```shell
python -O src/main.py
```

**Note:** `-O` is an optional flag that removes unnecessary `assert`s — you can omit it and run `python src/main.py`

## Configuration

### Cryptographic Standard

Select the cryptographic standardused to establish a secure TCP connection via the `CRYPTO__ML_KEM` environment variable

```env
CRYPTO__ML_KEM="512"
```

Supported values are `512` *(default)*, `768` and `1024`

## License

yttg-cli is a free, open-source software distributed under the [GPLv3 License](LICENSE.txt)
