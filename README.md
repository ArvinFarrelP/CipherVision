Berikut README versi **lebih jelas, minimalis, dan sudah include bagian executable (.exe)**. Siap copy langsung:

````markdown
# CipherVision

CipherVision is a simple cryptographic analysis and visualization tool for learning how classical substitution ciphers work and how they can be broken using frequency analysis.

## Features

- Text encryption using substitution cipher
- Letter frequency analysis
- Visualization using matplotlib
- Simple GUI with ttkbootstrap
- Standalone executable support (.exe)

## Requirements

- Python 3.10+
- matplotlib
- numpy
- ttkbootstrap

## Installation

```bash
pip install matplotlib numpy ttkbootstrap
```
````

## Usage

Run encryption tool:

```bash
python encrypt_text.py
```

Run frequency analysis:

```bash
python frequency_analysis.py
```

## Build Executable (Windows)

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed frequency_analysis.py
python -m PyInstaller --onefile --windowed encrypt_text.py
```

Output will be available in:

```bash
dist/
```

Run:

```bash
dist/frequency_analysis.exe
```

## Sample Text

```
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
CRYPTOGRAPHY IS THE ART OF SECRET COMMUNICATION.
FREQUENCY ANALYSIS HELPS TO BREAK SIMPLE SUBSTITUTION CIPHERS.
```

## Contributors

- Daniel Aquaries Pratama
- Arvin Farrel Pramuditya
