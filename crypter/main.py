#!/usr/bin/env python3
import argparse
from pathlib import Path
import os
from encrypt_decrypt import encrypt_file, decrypt_file
from key_manager import save_file_key, load_file_key

def derive_key_stem(path_str: str) -> str:
    """
    Given any file path — encrypted or decrypted — 
    resolve it and strip ALL extensions.
    e.g. "/…/encrypted/test.txt.enc" → "/…/encrypted/test"
    """
    p = Path(path_str).resolve()
    while p.suffix:
        p = p.with_suffix('')
    return str(p)

def get_output_path(input_path: str, mode: str, output_arg: str = None) -> str:
    inp = Path(input_path)
    if output_arg:
        return str(output_arg)

    folder = 'encrypted' if mode == 'encrypt' else 'decrypted'
    out_dir = inp.parent / folder
    out_dir.mkdir(parents=True, exist_ok=True)

    if mode == 'encrypt':
        return str(out_dir / (inp.name + '.enc'))
    # decrypt: strip ONE .enc if present
    stem = inp.with_suffix('').name if inp.suffix == '.enc' else inp.name
    return str(out_dir / stem)

def encrypt_file_with_password(input_file: str, output_file: str = None):
    if not output_file:
        output_file = get_output_path(input_file, 'encrypt')

    aes_key = os.urandom(32)
    iv      = os.urandom(16)

    # **Use the OUTPUT path here!**
    key_stem = derive_key_stem(output_file)

    save_file_key(key_stem, aes_key)
    encrypt_file(input_file, output_file, aes_key, iv)
    print(f"✅ Encrypted: {input_file} → {output_file}")

def decrypt_file_with_password(input_file: str, output_file: str = None):
    if not output_file:
        output_file = get_output_path(input_file, 'decrypt')

    # **Use the ENCRYPTED INPUT path here!**
    key_stem = derive_key_stem(input_file)
    aes_key  = load_file_key(key_stem)
    if not aes_key:
        return

    decrypt_file(input_file, output_file, aes_key)
    print(f"✅ Decrypted: {input_file} → {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="🔐 Encrypt or decrypt files with per-file AES keys."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    enc = sub.add_parser("encrypt", help="Encrypt a file")
    enc.add_argument("input", help="Input file to encrypt")
    enc.add_argument("-o", "--output", help="Custom output path (optional)")

    dec = sub.add_parser("decrypt", help="Decrypt a file")
    dec.add_argument("input", help="Encrypted file to decrypt")
    dec.add_argument("-o", "--output", help="Custom output path (optional)")

    args = parser.parse_args()
    if args.command == "encrypt":
        encrypt_file_with_password(args.input, args.output)
    else:
        decrypt_file_with_password(args.input, args.output)

if __name__ == "__main__":
    main()




'''import argparse
from pathlib import Path
import os
from encrypt_decrypt import encrypt_file, decrypt_file
from key_manager import save_file_key, load_file_key

# Helper function to get file stem (filename without extension or .enc)
def get_file_stem(file_path):
    path = Path(file_path)
    if path.suffix == '.enc':
        return path.with_suffix('').stem
    return path.stem

# Encrypt a file with password
def encrypt_file_with_password(input_file, output_file=None):
    if not output_file:
        # Default output filename for encrypted file
        output_file = input_file + ".enc"

    aes_key = os.urandom(32)
    iv = os.urandom(16)

    file_stem = get_file_stem(input_file)
    save_file_key(file_stem, aes_key)
    encrypt_file(input_file, output_file, aes_key, iv)
    print(f"✅ Encrypted: {input_file} → {output_file}")

# Decrypt a file with password
def decrypt_file_with_password(input_file, output_file=None):
    if not output_file:
        # Default output filename for decrypted file
        output_file = input_file.replace(".enc", ".decrypted")

    file_stem = get_file_stem(input_file)
    aes_key = load_file_key(file_stem)
    if not aes_key:
        return

    decrypt_file(input_file, output_file, aes_key)
    print(f"✅ Decrypted: {input_file} → {output_file}")

# Main function with argparse setup
def main():
    parser = argparse.ArgumentParser(description="🔐 Encrypt or decrypt files with per-file AES keys.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encrypt
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("input", help="Input file to encrypt")
    encrypt_parser.add_argument("-o", "--output", help="Output encrypted file name (optional)")

    # Decrypt
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("input", help="Encrypted file to decrypt")
    decrypt_parser.add_argument("-o", "--output", help="Output decrypted file name (optional)")

    args = parser.parse_args()

    if args.command == "encrypt":
        encrypt_file_with_password(args.input, args.output)
    elif args.command == "decrypt":
        decrypt_file_with_password(args.input, args.output)

# Entry point
if __name__ == "__main__":
    main()'''
