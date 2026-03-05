# Setup Instructions

## Activate Virtual Environment

.venv\Scripts\activate

## Install Dependencies

pip install ttkbootstrap matplotlib numpy
python -m pip install matplotlib numpy ttkbootstrap

## Run the Program

# Encryption Tool

python encrypt_text.py

# Frequency Analysis Tool

python frequency_analysis.py

## Dummy Test Text

THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
CRYPTOGRAPHY IS THE ART OF SECRET COMMUNICATION.
FREQUENCY ANALYSIS HELPS TO BREAK SIMPLE SUBSTITUTION CIPHERS.
LEARNING BY DOING MAKES THE PROCESS MORE FUN AND MEMORABLE.

## Build Application

pip install pyinstaller

pyinstaller --onefile --windowed frequency_analysis.py
pyinstaller --onefile --windowed encrypt_text.py
