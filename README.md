# LAB 5.1: Cryptography Toolkit
## Group : 16
A comprehensive Python toolkit for cryptographic operations including encryption, decryption, and hashing.

## Features

- **Symmetric Encryption**
  - AES (Advanced Encryption Standard)
  - DES (Data Encryption Standard)
  - Triple DES

- **Asymmetric Encryption**
  - RSA

- **Hashing**
  - MD5
  - SHA-1
  - SHA-256
  - SHA-512

- **Utilities**
  - Encoding/Decoding (Base64, Hex)
  - Key Generation
  - Input Validation

## Project Structure

```
Lab5-ISSecurity/
├── README.md
├── requirements.txt
├── main.py
└── src
    ├── asymmetric
    │   └── rsa_tool.py
    ├── core
    │   ├── input_handler.py
    │   ├── menu_asymmetric.py
    │   ├── menu_hash.py
    │   ├── menu_symmetric.py
    │   ├── output_handler.py
    ├── hash
    │   ├── md5.py
    │   └── sha256.py
    └── symmetric
        ├── aes.py
        ├── des.py
        └── tripledes.py
```

## Installation

1. Clone the repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py
```

## Requirements

- Python 3.7+

## License

MIT License
