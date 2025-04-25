# Crypter

A simple Python CLI to encrypt and decrypt individual files with per-file AES keys, wrapped by a password. Encrypted data (and its key/salt files) go into an `encrypted/` folder; decrypted output goes into `encrypted/decrypted/` by default. You can also override the output path.

---

Author - MAYANK

## Features

- AES-256-CBC encryption with PKCS#7 padding  
- Per-file random key + IV  
- Key-wrapping via password & PBKDF2-HMAC-SHA256 → Fernet  
- Automatic `encrypted/` and `decrypted/` subfolders  
- Optional `-o/--output` override  

---

## Prerequisites

- **Python 3.7** or later  
- **pip** (the Python package installer)  

> **Note:**  
> - You **do not** need to install `argparse`, `os`, or `pathlib`—they’re in the Python standard library.  
> - You **do** need the **cryptography** package.

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/mayank-comp/crypter.git
   cd crypter

    (Optional but recommended) Create & activate a virtual environment

python3 -m venv .venv
source .venv/bin/activate

Install dependencies

pip install cryptography

Or, if you include a requirements.txt:

    echo "cryptography>=3.4" > requirements.txt
    pip install -r requirements.txt

Usage

From the project root:

# Encrypt a file (prompts for password)
python main.py encrypt path/to/plain.txt
# → encrypted/plain.txt.enc + encrypted/plain.key + encrypted/plain.salt

# Decrypt it again
python main.py decrypt encrypted/plain.txt.enc
# → decrypted/plain.txt

Override the default output folder

By default, encryption goes into encrypted/ and decryption into decrypted/.
To specify a custom output path, use -o / --output:

# Encrypt into a single file
python main.py encrypt foo.bin -o /tmp/mycipher.dat

# Decrypt into a custom location
python main.py decrypt encrypted/foo.bin.enc -o ~/Downloads/foo.txt

Command-line help

Each command supports a --help flag:

python main.py encrypt --help
python main.py decrypt --help

Project layout

filecrypter/
├── encrypt_decrypt.py    # low-level AES routines
├── key_manager.py        # password → salt → key wrapping
├── main.py               # CLI entry point
├── requirements.txt      # optional
└── README.md

Disclaimer

Use at your own risk. The author provides this tool “as is” and is not responsible for any data loss, corruption, or misuse arising from its use. Always keep backups of your important files before encrypting or decrypting.

License

This project is released under the MIT License.
