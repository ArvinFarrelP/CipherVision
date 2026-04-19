# CipherVision

CipherVision is a lightweight tool for analyzing and visualizing classical substitution ciphers using frequency analysis.

## Features

- Substitution cipher encryption
- Letter frequency analysis
- Visualization with matplotlib
- Simple GUI (ttkbootstrap)
- Standalone executable support

## Requirements

- Python 3.10+
- matplotlib
- numpy
- ttkbootstrap

## Installation

```bash
pip install matplotlib numpy ttkbootstrap
```

## Usage

Encrypt text:

```bash
python encrypt_text.py
```

Run frequency analysis:

```bash
python frequency_analysis.py
```

## Build (Windows)

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed frequency_analysis.py
python -m PyInstaller --onefile --windowed encrypt_text.py
```

Output:

```bash
dist/
```

Run:

```bash
dist/frequency_analysis.exe
```

## Sample

```
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
CRYPTOGRAPHY IS THE ART OF SECRET COMMUNICATION.
FREQUENCY ANALYSIS HELPS TO BREAK SIMPLE SUBSTITUTION CIPHERS.
```

## Contributors

- Daniel Aquaries Pratama
- Arvin Farrel Pramuditya
