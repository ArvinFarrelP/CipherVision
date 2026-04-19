# CipherVision

CipherVision is a cryptographic analysis and visualization tool designed to demonstrate how classical substitution ciphers work and how they can be broken using frequency analysis.

## Description

This project helps users understand the fundamentals of cryptography and cryptanalysis through simple, interactive experimentation using a graphical interface.

## Features

- Encrypt text using classical substitution ciphers
- Automatically calculate letter frequency distribution
- Visualize frequency patterns using matplotlib
- Simple GUI built with ttkbootstrap

## Concepts

- Classical substitution ciphers
- Frequency analysis
- Cryptanalysis techniques
- Statistical patterns in language

## Installation

Activate virtual environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install matplotlib numpy ttkbootstrap
```

## Usage

Run encryption tool:

```bash
python encrypt_text.py
```

Run frequency analysis tool:

```bash
python frequency_analysis.py
```

## Sample Text

```
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
CRYPTOGRAPHY IS THE ART OF SECRET COMMUNICATION.
FREQUENCY ANALYSIS HELPS TO BREAK SIMPLE SUBSTITUTION CIPHERS.
LEARNING BY DOING MAKES THE PROCESS MORE FUN AND MEMORABLE.
```

## Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed frequency_analysis.py
pyinstaller --onefile --windowed encrypt_text.py
```

## Contributors

- Daniel Aquaries Pratama
- Arvin Farrel Pramuditya

## Purpose

This project is intended for educational purposes to demonstrate how classical cryptographic systems work and how statistical methods can be used to break them.
