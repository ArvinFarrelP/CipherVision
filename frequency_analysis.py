import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import string
import collections
import random
import json
import matplotlib.pyplot as plt
from tkinter import simpledialog
import subprocess
import sys
import os


# ===================================================== #
# || Deklarasi dan Inisialisasi Data yang diperlukan || #
# ===================================================== #

# =========================
# Konfigurasi & data bahasa
# =========================

ENGLISH_FREQ_ORDER = "ETAOINSHRDLUCMFYWGPBVKXQJZ"

COMMON_BIGRAMS_EN = [
    "TH",
    "HE",
    "IN",
    "ER",
    "AN",
    "RE",
    "ON",
    "AT",
    "EN",
    "ND",
    "TI",
    "ES",
    "OR",
    "TE",
    "OF",
    "ED",
    "IS",
    "IT",
    "AL",
    "AR",
]
COMMON_TRIGRAMS_EN = [
    "THE",
    "AND",
    "ING",
    "HER",
    "ERE",
    "ENT",
    "THA",
    "NTH",
    "WAS",
    "ETH",
]
COMMON_WORDS_EN = [
    "THE",
    "AND",
    "OF",
    "TO",
    "IN",
    "IS",
    "IT",
    "YOU",
    "THAT",
    "FOR",
    "ON",
    "WITH",
    "AS",
    "I",
    "THIS",
]

COMMON_BIGRAMS_ID = ["AN", "NG", "DA", "KA",
                     "YA", "LA", "TU", "DI", "KE", "SA", "TA"]
COMMON_TRIGRAMS_ID = ["DAN", "YANG", "ING", "KAN", "NGA", "ANG", "BER", "TER"]
COMMON_WORDS_ID = [
    "DAN",
    "YANG",
    "ADA",
    "INI",
    "UNTUK",
    "KEPADA",
    "DALAM",
    "ITU",
    "DARI",
    "KITA",
    "ANDA",
]

# =========================
# Utilitas analisis & skor
# =========================


def normalize_text(text):
    return "".join(ch for ch in text.upper() if ch in string.ascii_uppercase)


def frequency_analysis(text):
    norm = normalize_text(text)
    total = len(norm)
    counter = collections.Counter(norm)
    return counter, total


def proportions(counter, total):
    return {
        k: (counter.get(k, 0) / total * 100 if total > 0 else 0.0)
        for k in string.ascii_uppercase
    }


def suggest_mapping(counter):
    cipher_order = [l for l, _ in sorted(
        counter.items(), key=lambda x: (-x[1], x[0]))]
    suggestion = {}
    for i, c in enumerate(cipher_order):
        if i < len(ENGLISH_FREQ_ORDER):
            suggestion[c] = ENGLISH_FREQ_ORDER[i]
    return suggestion


def apply_mapping(text, mapping, unknown_char="·"):
    out = []
    for ch in text:
        up = ch.upper()
        if up in string.ascii_uppercase:
            mapped = mapping.get(up)
            if mapped:
                out.append(mapped if ch.isupper() else mapped.lower())
            else:
                out.append(unknown_char)
        else:
            out.append(ch)
    return "".join(out)


def ngram_analysis(text, n=2, top_k=10):
    norm = normalize_text(text)
    ngrams = [norm[i: i + n] for i in range(len(norm) - n + 1)]
    counter = collections.Counter(ngrams)
    return counter.most_common(top_k)


def score_text_rich(text, lang="EN"):
    text = text.upper()
    if lang.upper() == "ID":
        bigrams, trigrams, words = (
            COMMON_BIGRAMS_ID,
            COMMON_TRIGRAMS_ID,
            COMMON_WORDS_ID,
        )
    else:
        bigrams, trigrams, words = (
            COMMON_BIGRAMS_EN,
            COMMON_TRIGRAMS_EN,
            COMMON_WORDS_EN,
        )
    score = 0
    for bg in bigrams:
        score += text.count(bg)  # bobot 1
    for tg in trigrams:
        score += 2 * text.count(tg)  # bobot 2
    for w in words:
        score += 3 * text.count(w)  # bobot 3
    return score


# =========================
# Attack utilitas
# =========================


def caesar_decrypt(ciphertext, shift):
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def caesar_attack(ciphertext, lang="EN"):
    results = {}
    best_shift, best_text, best_score = 0, "", -1
    for shift in range(26):
        candidate = caesar_decrypt(ciphertext, shift)
        s = score_text_rich(candidate, lang=lang)
        results[shift] = candidate
        if s > best_score:
            best_score, best_shift, best_text = s, shift, candidate
    return best_shift, best_text, best_score, results


def decrypt_with_map_upper(text, mapping):
    out = []
    for ch in text.upper():
        if ch in string.ascii_uppercase:
            out.append(mapping.get(ch, ch))
        else:
            out.append(ch)
    return "".join(out)


# =========================
# Hint dinamis berposisi
# =========================


def find_trigram_recommendations(ciphertext, preview, target_trigrams):
    recs = []
    upper_preview = preview.upper()
    upper_cipher = ciphertext.upper()
    n = 3
    for tg in target_trigrams:
        for i in range(len(upper_preview) - n + 1):
            segment = upper_preview[i: i + n]
            # hitung huruf yang cocok
            matches = sum(1 for sp, tp in zip(segment, tg) if sp == tp)
            dots = segment.count("·")
            if (
                matches >= 1 and matches + dots == 3
            ):  # minimal 1 cocok, sisanya boleh kosong
                for j, (sp, tp) in enumerate(zip(segment, tg)):
                    if sp == "·":
                        cipher_char = upper_cipher[i + j]
                        if cipher_char in string.ascii_uppercase:
                            recs.append(
                                f"Segmen '{segment}' (pos {i}-{i+n-1}) mirip '{tg}'. "
                                f"Cipher '{cipher_char}' kemungkinan = '{tp}'."
                            )
    return recs


# =========================
# GUI aplikasi
# =========================


class SubstitutionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Subtitution Analysis")

        self.ciphertext = ""
        self.mapping = {}
        self.hint_mapping = {}
        self.attack_preview = ""
        self.attack_mapping = {}
        self.lang = tk.StringVar(value="EN")

        # Layout utama kiri-kanan
        main = tk.PanedWindow(root, sashrelief="raised", sashwidth=6)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg="#fafafa")
        right = tk.Frame(main, bg="#ffffff")
        main.add(left, minsize=420)
        main.add(right, minsize=380)

        # Bahasa skor
        lang_frame = tk.LabelFrame(
            left,
            text="🌐 Bahasa Target",
            bg="#bbdefb",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
        )
        lang_frame.pack(fill="x", pady=5)
        ttk.Combobox(
            lang_frame, textvariable=self.lang, values=["EN", "ID"], width=5
        ).pack(side="left", padx=10, pady=10)

        # Input
        input_frame = tk.LabelFrame(
            left,
            text="📝 Input Ciphertext",
            bg="#e3f2fd",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
        )
        input_frame.pack(fill="x", pady=5)
        self.input_text = tk.Text(
            input_frame, height=6, font=("Consolas", 11), bg="#ffffff", fg="#000000"
        )
        self.input_text.pack(fill="both", expand=True, pady=(10, 0))

        # Analisis
        analysis_frame = tk.LabelFrame(
            left,
            text="🔍 Analisis & Hint",
            bg="#e8f5e9",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
        )
        analysis_frame.pack(fill="x", pady=5)
        tk.Button(
            analysis_frame,
            text="Analisis",
            bg="#4caf50",
            fg="white",
            command=self.analyze,
        ).pack(side="left", padx=3, pady=10)
        tk.Button(
            analysis_frame,
            text="Hint Lanjutan",
            bg="#4caf50",
            fg="white",
            command=self.advanced_hint,
        ).pack(side="left", padx=3, pady=10)
        tk.Button(
            analysis_frame,
            text="Histogram (cipher)",
            bg="#4caf50",
            fg="white",
            command=self.show_histogram_cipher,
        ).pack(side="left", padx=3, pady=10)

        # Attack
        attack_frame = tk.LabelFrame(
            left,
            text="⚡ Percobaan Dekripsi & Enkripsi",
            bg="#fff3e0",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
        )
        attack_frame.pack(fill="x", pady=5)
        tk.Button(
            attack_frame,
            text="Caesar Attack",
            bg="#fb8c00",
            fg="white",
            command=self.run_caesar_attack,
        ).pack(side="left", padx=3, pady=10)

        tk.Button(
            attack_frame,
            text="Coba Tebakan Acak",
            bg="#f57c00",
            fg="white",
            command=self.run_random_attack,
        ).pack(side="left", padx=3, pady=10)
        tk.Button(
            attack_frame,
            text="Optimasi Otomatis",
            bg="#ef6c00",
            fg="white",
            command=self.run_auto_tune,
        ).pack(side="left", padx=3, pady=10)

        tk.Button(
            attack_frame,
            text="Buka Aplikasi Enkripsi",
            bg="#9c27b0",
            fg="white",
            command=self.open_encryption_app
        ).pack(side="left", padx=3, pady=10)

        # Mapping manual
        map_frame = tk.LabelFrame(
            left,
            text="✍️ Mapping Manual",
            bg="#ede7f6",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
        )
        map_frame.pack(fill="x", pady=5)
        self.cipher_var = tk.StringVar()
        self.plain_var = tk.StringVar()
        ttk.Label(map_frame, text="Cipher").grid(
            row=0, column=0, padx=2, pady=(10, 2))
        ttk.Combobox(
            map_frame,
            textvariable=self.cipher_var,
            values=list(string.ascii_uppercase),
            width=5,
        ).grid(row=0, column=1, padx=2, pady=(10, 2))
        ttk.Label(map_frame, text="→ Plain").grid(
            row=1, column=0, padx=2, pady=(2, 10))
        ttk.Combobox(
            map_frame,
            textvariable=self.plain_var,
            values=list(string.ascii_uppercase),
            width=5,
        ).grid(row=1, column=1, padx=2, pady=(2, 10))
        tk.Button(
            map_frame,
            text="Map",
            bg="#7e57c2",
            fg="white",
            width=10,
            command=self.update_mapping,
        ).grid(row=0, column=4, padx=(10, 2), pady=(10, 2))
        tk.Button(
            map_frame,
            text="Reset",
            bg="#d32f2f",
            fg="white",
            width=10,
            command=self.reset_mapping,
        ).grid(row=0, column=5, padx=2, pady=(10, 2))
        tk.Button(
            map_frame,
            text="Simpan",
            bg="#1976d2",
            fg="white",
            width=10,
            command=self.save_mapping,
        ).grid(row=1, column=4, padx=(10, 2), pady=(2, 10))
        tk.Button(
            map_frame,
            text="Muat",
            bg="#0288d1",
            fg="white",
            width=10,
            command=self.load_mapping,
        ).grid(row=1, column=5, padx=2, pady=(2, 10))
        tk.Button(
            map_frame,
            text="Gunakan Shift dari Mapping",
            bg="#009688",
            fg="white",
            width=25,
            command=self.preview_shift_from_mapping,
        ).grid(row=0, column=6, pady=(10, 4))
        tk.Button(
            map_frame,
            text="Gunakan Kunci Substitusi",
            bg="#009688",
            fg="white",
            width=25,
            command=self.use_direct_key,
        ).grid(row=1, column=6, padx=2, pady=(2, 10))

        # Preview manual
        preview_frame = tk.LabelFrame(
            left,
            text="📖 Preview Dekripsi (Mapping Manual)",
            bg="#fffde7",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
        )
        preview_frame.pack(fill="both", expand=True, pady=5)
        self.output_text = tk.Text(
            preview_frame, height=10, bg="#fffde7", fg="#000000", font=("Consolas", 11)
        )
        self.output_text.pack(fill="both", expand=True, pady=(10, 0))

        # Panel kanan hasil
        result_frame = tk.LabelFrame(
            right,
            text="📊 Hasil Attack & Analisis",
            bg="#fff8e1",
            fg="#000000",
            font=("Segoe UI", 10, "bold"),
        )
        result_frame.pack(fill="both", expand=True, pady=5)
        self.attack_text = tk.Text(
            result_frame, height=16, bg="#fff8e1", fg="#000000", font=("Consolas", 11)
        )
        self.attack_text.pack(fill="both", expand=True, pady=(10, 0))

        ana_frame = tk.Frame(right, bg="#fff8e1")
        ana_frame.pack(fill="x", pady=4)
        tk.Button(
            ana_frame,
            text="Analisis frekuensi hasil attack",
            bg="#8d6e63",
            fg="white",
            command=self.analyze_attack_preview,
        ).pack(side="left", padx=3, pady=2)
        tk.Button(
            ana_frame,
            text="Histogram (attack plaintext)",
            bg="#8d6e63",
            fg="white",
            command=self.show_histogram_attack,
        ).pack(side="left", padx=3, pady=2)
        tk.Button(
            ana_frame,
            text="Terapkan attack → preview manual",
            bg="#6d4c41",
            fg="white",
            command=self.apply_attack_to_preview,
        ).pack(side="left", padx=3, pady=2)
        tk.Button(
            ana_frame,
            text="Gabungkan mapping attack → manual",
            bg="#6d4c41",
            fg="white",
            command=self.merge_attack_mapping,
        ).pack(side="left", padx=3, pady=2)

        # Status & progress
        self.status = tk.StringVar(value="Status: siap")
        status_frame = tk.Frame(root, bg="#fafafa")
        status_frame.pack(fill="x")
        tk.Label(
            status_frame, textvariable=self.status, bg="#fafafa", fg="#000000"
        ).pack(side="left", padx=6, pady=4)

        self.progress = ttk.Progressbar(
            root, orient="horizontal", length=200, mode="determinate"
        )
        self.progress.pack(fill="x", padx=6, pady=4)

    # ====== Utilitas UI ======
    def set_status(self, text):
        self.status.set(f"Status: {text}")

    def update_preview_manual(self):
        mapping_effective = dict(self.hint_mapping)
        mapping_effective.update(self.mapping)
        decrypted = apply_mapping(self.ciphertext, mapping_effective)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", decrypted)

    # ====== Analisis & hint ======
    def analyze(self):
        self.ciphertext = self.input_text.get("1.0", "end").strip()
        if not self.ciphertext:
            messagebox.showwarning(
                "Peringatan", "Masukkan ciphertext terlebih dahulu.")
            return
        counter, total = frequency_analysis(self.ciphertext)
        self.hint_mapping = suggest_mapping(counter)
        self.update_preview_manual()
        self.set_status(
            f"Analisis selesai. Total huruf: {total}. Hint awal diterapkan (bisa dioverride)."
        )

    def show_histogram_cipher(self):
        if not self.ciphertext:
            messagebox.showwarning(
                "Peringatan", "Analisis dulu sebelum menampilkan histogram."
            )
            return

        counter, total = frequency_analysis(self.ciphertext)

        # Sort berdasarkan frekuensi
        items = sorted(counter.items(), key=lambda x: -x[1])
        letters = [l for l, _ in items]
        values = [counter[l] for l in letters]

        plt.figure(figsize=(12, 5))
        bars = plt.bar(letters, values, color="#4C78A8")

        # Mewarnai top 5
        for i, bar in enumerate(bars):
            if i < 5:
                bar.set_color("#f28e2b")

        # Label persentase
        for i, v in enumerate(values):
            plt.text(i, v + 0.5, f"{v/total*100:.1f}%",
                     ha="center", fontsize=8)

        plt.title("Histogram Frekuensi Huruf (Ciphertext, diurutkan)")
        plt.xlabel("Huruf")
        plt.ylabel("Jumlah")

        # Gambaran distribusi bahasa target
        lang = self.lang.get().upper()
        if lang == "EN":
            english_freq = {
                "E": 12.7,
                "T": 9.1,
                "A": 8.2,
                "O": 7.5,
                "I": 7.0,
                "N": 6.7,
                "S": 6.3,
                "H": 6.1,
                "R": 6.0,
                "D": 4.3,
                "L": 4.0,
                "C": 2.8,
                "U": 2.8,
                "M": 2.4,
                "W": 2.4,
                "F": 2.2,
                "G": 2.0,
                "Y": 2.0,
                "P": 1.9,
                "B": 1.5,
                "V": 1.0,
                "K": 0.8,
                "J": 0.15,
                "X": 0.15,
                "Q": 0.1,
                "Z": 0.07,
            }
            ref_values = [english_freq.get(
                l, 0) / 100 * total for l in letters]
            plt.plot(
                letters,
                ref_values,
                color="red",
                marker="o",
                linestyle="--",
                label="Distribusi EN",
            )
            plt.legend()

        elif lang == "ID":
            indonesian_freq = {
                "A": 19.0,
                "N": 15.0,
                "I": 9.0,
                "E": 9.0,
                "U": 8.0,
                "T": 7.0,
                "R": 6.0,
                "K": 6.0,
                "S": 5.0,
                "D": 4.0,
                "M": 4.0,
                "L": 3.0,
                "O": 3.0,
                "G": 2.0,
                "B": 2.0,
                "P": 2.0,
                "H": 1.0,
                "Y": 1.0,
                "J": 1.0,
                "C": 1.0,
                "W": 1.0,
                "F": 0.5,
                "Z": 0.5,
                "V": 0.2,
                "X": 0.1,
                "Q": 0.1,
            }
            ref_values = [indonesian_freq.get(
                l, 0) / 100 * total for l in letters]
            plt.plot(
                letters,
                ref_values,
                color="red",
                marker="o",
                linestyle="--",
                label="Distribusi ID",
            )
            plt.legend()

        plt.show()

    def advanced_hint(self):
        if not self.ciphertext:
            messagebox.showwarning(
                "Peringatan", "Analisis dulu sebelum menggunakan hint lanjutan."
            )
            return

        # Preview mapping saat ini
        mapping_effective = dict(self.hint_mapping)
        mapping_effective.update(self.mapping)
        preview = apply_mapping(self.ciphertext, mapping_effective)

        # Data menyesuaikan bahasa yang dipilih
        if self.lang.get().upper() == "ID":
            trigram_list = COMMON_TRIGRAMS_ID
        else:
            trigram_list = COMMON_TRIGRAMS_EN

        # Rekomendasi spesifik posisi & huruf cipher
        trigram_recs = find_trigram_recommendations(
            self.ciphertext, preview, trigram_list
        )

        # Ringkasan ngram top (ciphertext)
        bigrams = ngram_analysis(self.ciphertext, n=2, top_k=10)
        trigrams = ngram_analysis(self.ciphertext, n=3, top_k=10)

        msg = "=== Saran Hint Dinamis (berposisi) ===\n"
        if trigram_recs:
            msg += "\n".join("- " + r for r in trigram_recs) + "\n"
        else:
            msg += "- Belum ada segmen trigram yang bisa direkomendasikan.\n"
        msg += "\n=== Bigram Ciphertext Teratas ===\n"
        for bg, count in bigrams:
            msg += f"{bg} : {count}\n"
        msg += "\n=== Trigram Ciphertext Teratas ===\n"
        for tg, count in trigrams:
            msg += f"{tg} : {count}\n"

        trigrams_preview = ngram_analysis(preview, n=3, top_k=10)
        msg += "\n=== Trigram Preview (plaintext sementara) ===\n"
        for tg, count in trigrams_preview:
            msg += f"{tg} : {count}\n"

        messagebox.showinfo("Hint Lanjutan", msg)

    # ====== Percobaan Dekripsi ======
    def ask_shift_with_slider(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Pilih Shift Caesar")
        dialog.grab_set()  # fokus ke dialog

        tk.Label(
            dialog, text="Geser slider untuk memilih shift (-25 sampai 25)").pack(pady=10)

        shift_var = tk.IntVar(value=0)
        slider = tk.Scale(
            dialog,
            from_=-25, to=25,
            orient="horizontal",
            variable=shift_var,
            length=300,
            tickinterval=5
        )
        slider.pack(padx=10, pady=10)

        result = {"shift": None}

        def confirm():
            result["shift"] = shift_var.get()
            dialog.destroy()

        tk.Button(dialog, text="OK", command=confirm).pack(pady=10)

        dialog.wait_window()  # tunggu sampai dialog ditutup
        return result["shift"]

    # ====== Mmebuka Aplikasi kedua lewat CMD ======
    # def open_encryption_app(self):
    #     try:
    #         subprocess.Popen([sys.executable, "encrypth_text.py"])
    #         self.set_status("Aplikasi enkripsi dibuka.")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Gagal membuka aplikasi enkripsi: {e}")

    # ====== Mmebuka Aplikasi kedua lewat .exe ======
    def open_encryption_app(self):
        try:
            exe_path = os.path.join(os.path.dirname(
                sys.executable), "encrypt_text.exe")
            subprocess.Popen([exe_path])
            self.set_status("Aplikasi enkripsi dibuka.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Gagal membuka aplikasi enkripsi: {e}")

    # ====== Mapping manual ======
    def update_mapping(self):
        c = self.cipher_var.get().upper()
        p = self.plain_var.get().upper()
        if c in string.ascii_uppercase and p in string.ascii_uppercase:
            self.mapping[c] = p
            self.update_preview_manual()
            self.set_status(f"Mapping diperbarui: {c} → {p}")
        else:
            messagebox.showerror("Error", "Pilih huruf A–Z untuk mapping.")

    def reset_mapping(self):
        self.mapping = {}
        self.update_preview_manual()
        self.set_status("Mapping manual dikosongkan (hint awal tetap ada).")

    def save_mapping(self):
        if not self.mapping:
            messagebox.showinfo("Info", "Mapping manual kosong.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.mapping, f, ensure_ascii=False, indent=2)
        self.set_status(f"Mapping disimpan ke {path}")

    def load_mapping(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                if k not in string.ascii_uppercase or v not in string.ascii_uppercase:
                    raise ValueError("Format mapping tidak valid.")
            self.mapping = data
            self.update_preview_manual()
            self.set_status(f"Mapping dimuat dari {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat mapping: {e}")

    # ====== Attack (progress bar di GUI) ======
    def preview_shift_from_mapping(self):
        # cek apakah user sudah isi mapping
        c = ""
        p = ""
        if hasattr(self, "cipher_entry"):  # kalau pakai Entry
            c = self.cipher_entry.get().upper()
            p = self.plain_entry.get().upper()
        elif hasattr(self, "cipher_var"):  # kalau masih pakai Combobox
            c = self.cipher_var.get().upper()
            p = self.plain_var.get().upper()

        if not c or not p:
            messagebox.showinfo(
                "Info",
                "Fitur ini hanya bisa dipakai bila Anda sudah menentukan minimal satu mapping Cipher → Plain.\n"
                "Silakan isi dulu huruf Cipher dan huruf Plain di Mapping Manual.",
            )
            return

        if c in string.ascii_uppercase and p in string.ascii_uppercase:
            shift = (ord(c) - ord(p)) % 26
            preview = caesar_decrypt(self.ciphertext, shift)
            self.attack_preview = preview
            self.attack_text.delete("1.0", "end")
            self.attack_text.insert(
                "1.0",
                f"[Preview Caesar berdasarkan {c}->{p}, shift {shift}]\n\n{preview}",
            )
            self.set_status(
                f"Preview Caesar dibuat dengan shift {shift} dari {c}->{p}")
        else:
            messagebox.showerror(
                "Error", "Isi Cipher dan Plain dengan huruf A–Z.")

    def run_caesar_attack(self):
        self.ciphertext = self.input_text.get("1.0", "end").strip()
        if not self.ciphertext:
            messagebox.showwarning(
                "Peringatan", "Masukkan ciphertext terlebih dahulu.")
            return

        # Tanya user apakah mau input shift manual
        choice = messagebox.askyesno(
            "Caesar Attack",
            "Apakah Anda ingin memasukkan shift secara manual?\n"
            "Ya = input manual, Tidak = cari otomatis terbaik.",
        )

        if choice:  # === Mode manual ===
            shift = self.ask_shift_with_slider()
            if shift is None:
                return

            preview = caesar_decrypt(self.ciphertext, shift)
            self.attack_preview = preview
            self.attack_mapping = {}
            self.attack_text.delete("1.0", "end")
            self.attack_text.insert(
                "1.0", f"[Caesar shift {shift} (manual via slider)]\n\n{self.attack_preview}"
            )
            self.set_status(
                f"Preview Caesar dengan shift {shift} ditampilkan.")

        else:  # === Mode otomatis (brute force terbaik) ===
            best_shift, best_text, best_score, _ = caesar_attack(
                self.ciphertext, lang=self.lang.get()
            )
            self.attack_preview = best_text
            self.attack_mapping = {}
            self.attack_text.delete("1.0", "end")
            self.attack_text.insert(
                "1.0",
                f"[Caesar shift {best_shift}, skor {best_score}]\n\n{self.attack_preview}",
            )
            self.set_status(
                f"Caesar attack selesai. Shift terbaik: {best_shift} (skor {best_score})."
            )

    def preview_caesar_shift(self):
        self.ciphertext = self.input_text.get("1.0", "end").strip()
        if not self.ciphertext:
            messagebox.showwarning(
                "Peringatan", "Masukkan ciphertext terlebih dahulu.")
            return

        shift = self.shift_var.get()
        preview = caesar_decrypt(self.ciphertext, shift)

        self.attack_preview = preview
        self.attack_mapping = {}
        self.attack_text.delete("1.0", "end")
        self.attack_text.insert(
            "1.0",
            f"[Caesar shift {shift} via slider]\n\n{self.attack_preview}"
        )
        self.set_status(f"Preview Caesar dengan shift {shift} ditampilkan.")

    def run_random_attack(self):
        self.ciphertext = self.input_text.get("1.0", "end").strip()
        if not self.ciphertext:
            messagebox.showwarning(
                "Peringatan", "Masukkan ciphertext terlebih dahulu.")
            return
        try:
            iterations = simpledialog.askinteger(
                "Random Attack",
                "Jumlah iterasi (disarankan 8000–20000):",
                initialvalue=12000,
                minvalue=1000,
                maxvalue=200000,
            )
            if iterations is None:
                return
        except Exception:
            iterations = 12000

        # Progress bar
        self.progress.pack(fill="x", padx=6, pady=4)
        self.progress["maximum"] = iterations
        self.progress["value"] = 0
        self.root.update_idletasks()

        # Inisialisasi hill-climbing (random)
        letters = list(string.ascii_uppercase)
        shuffled = letters[:]
        random.shuffle(shuffled)
        mapping = dict(zip(letters, shuffled))

        best_mapping = mapping
        best_plain = decrypt_with_map_upper(self.ciphertext, best_mapping)
        best_score = score_text_rich(best_plain, lang=self.lang.get())

        for i in range(iterations):
            a, b = random.sample(letters, 2)
            new_mapping = best_mapping.copy()
            new_mapping[a], new_mapping[b] = new_mapping[b], new_mapping[a]

            new_plain = decrypt_with_map_upper(self.ciphertext, new_mapping)
            new_score = score_text_rich(new_plain, lang=self.lang.get())

            if new_score > best_score:
                best_mapping, best_plain, best_score = new_mapping, new_plain, new_score

            if i % 500 == 0:
                self.progress["value"] = i
                self.root.update_idletasks()

        self.progress["value"] = iterations
        self.root.update_idletasks()
        self.progress.pack_forget()

        self.attack_preview = best_plain
        self.attack_mapping = best_mapping
        self.attack_text.delete("1.0", "end")
        self.attack_text.insert(
            "1.0",
            f"[Random substitution, skor {best_score}, iterasi {iterations}]\n\n{self.attack_preview}",
        )
        self.set_status(
            f"Random attack selesai. Skor {best_score}. Mapping tersedia untuk merge."
        )

    def run_auto_tune(self):
        self.ciphertext = self.input_text.get("1.0", "end").strip()
        if not self.ciphertext:
            messagebox.showwarning(
                "Peringatan", "Masukkan ciphertext terlebih dahulu.")
            return
        if not self.hint_mapping:
            messagebox.showinfo(
                "Info", "Belum ada hint mapping. Jalankan 'Analisis' terlebih dahulu."
            )
            return
        try:
            iterations = simpledialog.askinteger(
                "Auto-Tune Attack",
                "Jumlah iterasi (disarankan 8000–20000):",
                initialvalue=15000,
                minvalue=1000,
                maxvalue=300000,
            )
            if iterations is None:
                return
        except Exception:
            iterations = 15000

        # Progress bar
        self.progress.pack(fill="x", padx=6, pady=4)
        self.progress["maximum"] = iterations
        self.progress["value"] = 0
        self.root.update_idletasks()

        # Inisialisasi dari hint mapping
        letters = list(string.ascii_uppercase)
        used = set(self.hint_mapping.values())
        unused = [l for l in letters if l not in used]
        mapping = dict(self.hint_mapping)
        for c in letters:
            if c not in mapping:
                mapping[c] = unused.pop() if unused else random.choice(letters)

        best_mapping = mapping
        best_plain = decrypt_with_map_upper(self.ciphertext, best_mapping)
        best_score = score_text_rich(best_plain, lang=self.lang.get())

        for i in range(iterations):
            a, b = random.sample(letters, 2)
            new_mapping = best_mapping.copy()
            new_mapping[a], new_mapping[b] = new_mapping[b], new_mapping[a]

            new_plain = decrypt_with_map_upper(self.ciphertext, new_mapping)
            new_score = score_text_rich(new_plain, lang=self.lang.get())

            if new_score > best_score:
                best_mapping, best_plain, best_score = new_mapping, new_plain, new_score

            if i % 500 == 0:
                self.progress["value"] = i
                self.root.update_idletasks()

        self.progress["value"] = iterations
        self.root.update_idletasks()
        self.progress.pack_forget()

        self.attack_preview = best_plain
        self.attack_mapping = best_mapping
        self.attack_text.delete("1.0", "end")
        self.attack_text.insert(
            "1.0",
            f"[Auto-Tune, skor {best_score}, iterasi {iterations}]\n\n{self.attack_preview}",
        )
        self.set_status(
            "Auto-Tune selesai. Mapping siap pakai dan bisa di-merge.")

    # ====== Analisis hasil attack ======
    def analyze_attack_preview(self):
        if not self.attack_preview:
            messagebox.showinfo(
                "Info", "Belum ada hasil attack untuk dianalisis.")
            return
        c_counter, c_total = frequency_analysis(self.ciphertext)
        c_prop = proportions(c_counter, c_total)
        a_counter, a_total = frequency_analysis(self.attack_preview)
        a_prop = proportions(a_counter, a_total)

        def top_list(counter, prop, top=10):
            items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))[:top]
            lines = [f"{l}: {counter[l]} ({prop[l]:.2f}%)" for l, _ in items]
            return "\n".join(lines)

        msg = "=== Perbandingan Frekuensi ===\n"
        msg += f"\nCiphertext (total {c_total}):\n{top_list(c_counter, c_prop)}\n"
        msg += f"\nAttack plaintext (total {a_total}):\n{top_list(a_counter, a_prop)}\n"
        messagebox.showinfo("Analisis Attack", msg)

    def show_histogram_attack(self):
        if not self.attack_preview:
            messagebox.showinfo(
                "Info", "Belum ada hasil attack untuk ditampilkan histogramnya."
            )
            return

        counter, total = frequency_analysis(self.attack_preview)

        # Sort berdasarkan frekuensi
        items = sorted(counter.items(), key=lambda x: -x[1])
        letters = [l for l, _ in items]
        values = [counter[l] for l in letters]

        plt.figure(figsize=(12, 5))
        bars = plt.bar(letters, values, color="#4C78A8")

        # Mewarnai top-5
        for i, bar in enumerate(bars):
            if i < 5:
                bar.set_color("#f28e2b")

        # Label persentase
        for i, v in enumerate(values):
            plt.text(i, v + 0.5, f"{v/total*100:.1f}%",
                     ha="center", fontsize=8)

        plt.title("Histogram Frekuensi Huruf (Plaintext hasil attack, diurutkan)")
        plt.xlabel("Huruf")
        plt.ylabel("Jumlah")

        # Distribusi bahasa target berdasarkan pilihan
        lang = self.lang.get().upper()
        if lang == "EN":
            english_freq = {
                "E": 12.7,
                "T": 9.1,
                "A": 8.2,
                "O": 7.5,
                "I": 7.0,
                "N": 6.7,
                "S": 6.3,
                "H": 6.1,
                "R": 6.0,
                "D": 4.3,
                "L": 4.0,
                "C": 2.8,
                "U": 2.8,
                "M": 2.4,
                "W": 2.4,
                "F": 2.2,
                "G": 2.0,
                "Y": 2.0,
                "P": 1.9,
                "B": 1.5,
                "V": 1.0,
                "K": 0.8,
                "J": 0.15,
                "X": 0.15,
                "Q": 0.1,
                "Z": 0.07,
            }
            ref_values = [english_freq.get(
                l, 0) / 100 * total for l in letters]
            plt.plot(
                letters,
                ref_values,
                color="red",
                marker="o",
                linestyle="--",
                label="Distribusi EN",
            )
            plt.legend()

        elif lang == "ID":
            indonesian_freq = {
                "A": 19.0,
                "N": 15.0,
                "I": 9.0,
                "E": 9.0,
                "U": 8.0,
                "T": 7.0,
                "R": 6.0,
                "K": 6.0,
                "S": 5.0,
                "D": 4.0,
                "M": 4.0,
                "L": 3.0,
                "O": 3.0,
                "G": 2.0,
                "B": 2.0,
                "P": 2.0,
                "H": 1.0,
                "Y": 1.0,
                "J": 1.0,
                "C": 1.0,
                "W": 1.0,
                "F": 0.5,
                "Z": 0.5,
                "V": 0.2,
                "X": 0.1,
                "Q": 0.1,
            }
            ref_values = [indonesian_freq.get(
                l, 0) / 100 * total for l in letters]
            plt.plot(
                letters,
                ref_values,
                color="red",
                marker="o",
                linestyle="--",
                label="Distribusi ID",
            )
            plt.legend()

        plt.show()

    def apply_attack_to_preview(self):
        if not self.attack_preview:
            messagebox.showinfo(
                "Info", "Belum ada hasil attack untuk diterapkan.")
            return
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", self.attack_preview)
        self.set_status(
            "Hasil attack diterapkan ke preview manual (mapping manual tetap)."
        )

    def merge_attack_mapping(self):
        if not self.attack_mapping:
            messagebox.showinfo(
                "Info", "Tidak ada mapping dari hasil attack untuk digabungkan."
            )
            return
        self.mapping.update(self.attack_mapping)
        self.update_preview_manual()
        self.set_status("Mapping attack digabungkan ke mapping manual.")

    def use_direct_key(self):
        key = simpledialog.askstring(
            "Masukkan Kunci Substitusi",
            "Masukkan 26 huruf (A–Z) sebagai kunci substitusi.\n"
            "Contoh: QWERTYUIOPASDFGHJKLZXCVBNM\n"
            "(Plain A→Q, B→W, dst.)",
        )
        if not key:
            return

        key = key.upper()
        if len(key) != 26 or not all(ch in string.ascii_uppercase for ch in key):
            messagebox.showerror("Error", "Kunci harus 26 huruf A–Z.")
            return
        if len(set(key)) != 26:
            messagebox.showerror("Error", "Kunci tidak boleh ada huruf ganda.")
            return

        # Buat mapping cipher→plain (dibalik!)
        letters = list(string.ascii_uppercase)
        mapping = {}
        for plain, cipher in zip(letters, key):
            mapping[cipher] = plain

        # Terapkan mapping
        self.mapping = mapping
        self.update_preview_manual()
        self.set_status("Kunci substitusi diterapkan untuk dekripsi.")


# =========================
# Main
# =========================

if __name__ == "__main__":
    root = tk.Tk()
    app = SubstitutionGUI(root)
    root.mainloop()
