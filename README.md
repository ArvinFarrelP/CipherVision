# 🔐 CipherVision - Classical Cipher Analysis & Visualization Tool

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Cryptography](https://img.shields.io/badge/Cryptography-Classical%20Ciphers-purple.svg)
![Visualization](https://img.shields.io/badge/Data%20Visualization-Matplotlib-orange.svg)
![UI](https://img.shields.io/badge/UI-ttkbootstrap-green.svg)
![Status](https://img.shields.io/badge/Status-Educational%20Project-brightgreen.svg)

**CipherVision** is a cryptographic analysis and visualization tool designed to demonstrate how classical substitution ciphers work and how they can be broken using **frequency analysis**.

This project helps learners understand the fundamentals of **cryptography and cryptanalysis** through interactive experimentation.

---

# ✨ Features

### 🔑 Encryption Tool

- Encrypt plaintext using classical substitution techniques
- Simple graphical interface for experimenting with cipher text
- Educational demonstration of classical cryptographic methods

### 📊 Frequency Analysis Tool

- Automatically calculates letter frequency distribution
- Visualizes frequency patterns using charts
- Helps demonstrate how substitution ciphers can be broken

### 🖥 Visualization

- Frequency graphs using **matplotlib**
- Clean GUI using **ttkbootstrap**
- Easy experimentation with ciphertext samples

---

# 🧠 Concepts Demonstrated

CipherVision demonstrates several important cryptographic concepts:

- Classical substitution ciphers
- Frequency analysis
- Cryptanalysis techniques
- Statistical patterns in language
- Visualization for security analysis

---

# 🚀 Quick Start

## 1. Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

---

## 2. Install Dependencies

```bash
pip install ttkbootstrap matplotlib numpy
```

or

```bash
python -m pip install matplotlib numpy ttkbootstrap
```

---

## 3. Run the Program

### Encryption Tool

```bash
python encrypt_text.py
```

### Frequency Analysis Tool

```bash
python frequency_analysis.py
```

---

# 🧪 Dummy Test Text

You can use the following text samples for testing:

```
THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
CRYPTOGRAPHY IS THE ART OF SECRET COMMUNICATION.
FREQUENCY ANALYSIS HELPS TO BREAK SIMPLE SUBSTITUTION CIPHERS.
LEARNING BY DOING MAKES THE PROCESS MORE FUN AND MEMORABLE.
```

---

# 📦 Build Standalone Application

Install PyInstaller:

```bash
pip install pyinstaller
```

Build executable:

```bash
pyinstaller --onefile --windowed frequency_analysis.py
pyinstaller --onefile --windowed encrypt_text.py
```

Executable files will appear in the `dist` folder.

---

# 👨‍💻 Contributors

- **Arvin Farrel Pramuditya**
- Daniel Aquaries Pratama
  https://github.com/danielaquaries20

---

# 📚 Educational Purpose

CipherVision is an educational project created to demonstrate how classical cryptographic systems work and how statistical methods like **frequency analysis** can be used to break simple substitution ciphers.

---

# 📄 License

MIT License
