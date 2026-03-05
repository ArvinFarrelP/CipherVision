import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# --- Fungsi substitusi sederhana ---


def generate_key():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "CDEFGHIJKLMNOPQRSTUVWXYZAB"  # contoh key geser 2
    return dict(zip(alphabet, key))


def encrypt(plain_text, key_map):
    plain_text = plain_text.upper()
    return "".join([key_map.get(c, c) for c in plain_text])

# --- Plot gabungan (single plot) - WARNA DIUBAH ---


def plot_single(plain_text, cipher_text):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    plain_counter = Counter([c for c in plain_text.upper() if c in alphabet])
    cipher_counter = Counter([c for c in cipher_text.upper() if c in alphabet])

    plain_sorted = sorted(plain_counter.items(),
                          key=lambda x: x[1], reverse=True)
    cipher_mapped = [
        (cipher_counter.get(generate_key()[ch], 0), generate_key()[ch])
        for ch, _ in plain_sorted
    ]

    plain_letters = [ch for ch, _ in plain_sorted]
    plain_freq = [freq for _, freq in plain_sorted]
    cipher_freq = [freq for freq, _ in cipher_mapped]
    cipher_letters = [c for _, c in cipher_mapped]

    x = np.arange(len(plain_letters))
    width = 0.4

    plt.figure(figsize=(12, 6))
    plt.bar(
        x - width / 2,
        plain_freq,
        width,
        label="Plain Text (" + "".join(plain_letters) + ")",
        color="blue",  # DIUBAH: biru seperti dual plot
    )
    plt.bar(
        x + width / 2,
        cipher_freq,
        width,
        label="Cipher Text (" + "".join(cipher_letters) + ")",
        color="gold",  # DIUBAH: gold/kuning seperti dual plot
    )

    plt.xticks(x, plain_letters)
    plt.xlabel("Huruf Plaintext (Cipher di legenda)")
    plt.ylabel("Frekuensi")
    plt.title("Perbandingan Frekuensi (Sorted by Plaintext Frequency)")
    plt.legend()
    plt.show()

# --- Plot terpisah (dual plot) - WARNA TETAP ---


def plot_dual(plain_text, cipher_text):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    plain_counter = Counter([c for c in plain_text.upper() if c in alphabet])
    cipher_counter = Counter([c for c in cipher_text.upper() if c in alphabet])

    # Plaintext
    plt.figure(figsize=(12, 5))
    p_sorted = sorted(plain_counter.items(), key=lambda x: x[1], reverse=True)
    plt.bar([ch for ch, _ in p_sorted], [
            freq for _, freq in p_sorted], color="blue")
    plt.title("Frekuensi Huruf Plaintext (Descending)")
    plt.xlabel("Huruf")
    plt.ylabel("Frekuensi")

    # Ciphertext
    plt.figure(figsize=(12, 5))
    c_sorted = sorted(cipher_counter.items(), key=lambda x: x[1], reverse=True)
    plt.bar([ch for ch, _ in c_sorted], [
            freq for _, freq in c_sorted], color="gold")
    plt.title("Frekuensi Huruf Ciphertext (Descending)")
    plt.xlabel("Huruf")
    plt.ylabel("Frekuensi")

    plt.show()

# --- GUI Modern dengan ttkbootstrap ---


class ModernCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Substitution Cipher Analyzer")
        self.root.geometry("1000x700")
        self.root.state('zoomed')  # Fullscreen

        # Available themes
        self.themes = ["darkly", "solar",
                       "superhero", "cyborg", "vapor", "morph"]

        self.setup_ui()

    def setup_ui(self):
        # Default theme
        self.style = tb.Style("darkly")

        # Main container
        main_container = tb.Frame(self.root, padding=30)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header dengan theme selector
        header_frame = tb.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title
        title_frame = tb.Frame(header_frame)
        title_frame.pack(fill=tk.X)

        tb.Label(title_frame, text="SUBSTITUTION CIPHER ANALYZER",
                 font=("Arial", 22, "bold"), bootstyle=PRIMARY).pack()

        tb.Label(title_frame, text="Analisis Frekuensi Huruf untuk Kriptografi",
                 font=("Arial", 12), bootstyle=SECONDARY).pack()

        # Theme selector
        theme_frame = tb.Frame(header_frame)
        theme_frame.pack(fill=tk.X, pady=(10, 0))

        tb.Label(theme_frame, text="Theme:",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT)

        self.theme_var = tk.StringVar(value="darkly")
        theme_combo = tb.Combobox(theme_frame, textvariable=self.theme_var,
                                  values=self.themes, state="readonly", width=12)
        theme_combo.pack(side=tk.LEFT, padx=10)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)

        # Input section
        input_frame = tb.Labelframe(
            main_container, text="INPUT PLAIN TEXT", padding=20)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        tb.Label(input_frame, text="Masukkan teks yang akan dienkripsi:",
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))

        # Text widget dengan scrollbar untuk input
        input_container = tb.Frame(input_frame)
        input_container.pack(fill=tk.BOTH, expand=True)

        self.entry = tb.Text(input_container, height=8,
                             font=("Consolas", 11), wrap=tk.WORD)
        scrollbar_input = tb.Scrollbar(
            input_container, orient=tk.VERTICAL, command=self.entry.yview)
        self.entry.configure(yscrollcommand=scrollbar_input.set)

        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_input.pack(side=tk.RIGHT, fill=tk.Y)

        # Button section
        button_frame = tb.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        tb.Button(button_frame, text="ENCRYPT & SINGLE PLOT",
                  command=self.run_single, bootstyle=SUCCESS,
                  width=25).pack(side=tk.LEFT, padx=(0, 15))

        tb.Button(button_frame, text="ENCRYPT & DUAL PLOT",
                  command=self.run_dual, bootstyle=INFO,
                  width=20).pack(side=tk.LEFT, padx=(0, 15))

        tb.Button(button_frame, text="COPY CIPHERTEXT",
                  command=self.copy_cipher, bootstyle=WARNING,
                  width=15).pack(side=tk.LEFT)

        # Result section
        result_frame = tb.Labelframe(
            main_container, text="HASIL ENKRIPSI", padding=20)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        tb.Label(result_frame, text="Ciphertext:",
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))

        # Text widget dengan scrollbar untuk hasil
        result_container = tb.Frame(result_frame)
        result_container.pack(fill=tk.BOTH, expand=True)

        self.result_text = tb.Text(result_container, height=6, font=("Consolas", 11),
                                   foreground="#2ecc71", wrap=tk.WORD, state="disabled")
        scrollbar_result = tb.Scrollbar(
            result_container, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar_result.set)

        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_result.pack(side=tk.RIGHT, fill=tk.Y)

        # Key information
        key_frame = tb.Labelframe(
            main_container, text="KEY SUBSTITUSI", padding=20)
        key_frame.pack(fill=tk.X)

        key_map = generate_key()
        key_text = " | ".join([f"{k}→{v}" for k, v in key_map.items()])

        tb.Label(key_frame, text=key_text, font=("Courier", 10),
                 bootstyle=SECONDARY).pack()

        # Status bar
        self.status = tb.Label(main_container, text="Ready - Masukkan teks untuk memulai analisis",
                               bootstyle=SECONDARY)
        self.status.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

    def change_theme(self, event=None):
        selected_theme = self.theme_var.get()
        self.style = tb.Style(selected_theme)
        self.status.config(text=f"Theme diubah ke: {selected_theme}")

    def run_single(self):
        text = self.entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning(
                "Input Kosong", "Masukkan teks terlebih dahulu!")
            return

        self.status.config(text="Memproses Single Plot...")
        self.root.update()

        key_map = generate_key()
        cipher = encrypt(text, key_map)

        # Update result
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", cipher)
        self.result_text.config(state="disabled")

        plot_single(text, cipher)
        self.status.config(text="Single Plot berhasil ditampilkan!")

    def run_dual(self):
        text = self.entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning(
                "Input Kosong", "Masukkan teks terlebih dahulu!")
            return

        self.status.config(text="Memproses Dual Plot...")
        self.root.update()

        key_map = generate_key()
        cipher = encrypt(text, key_map)

        # Update result
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", cipher)
        self.result_text.config(state="disabled")

        plot_dual(text, cipher)
        self.status.config(text="Dual Plot berhasil ditampilkan!")

    def copy_cipher(self):
        cipher = self.result_text.get("1.0", tk.END).strip()
        if cipher:
            self.root.clipboard_clear()
            self.root.clipboard_append(cipher)
            self.status.config(
                text="Ciphertext berhasil disalin ke clipboard!")
        else:
            messagebox.showwarning(
                "Kosong", "Tidak ada ciphertext untuk disalin.")


# --- Main Application ---
if __name__ == "__main__":
    root = tb.Window("Substitution Cipher Analyzer", "darkly")
    app = ModernCipherApp(root)
    root.mainloop()
