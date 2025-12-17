# Analisis Refactoring SOLID - Studi Kasus Registrasi Mahasiswa

## 1. Identifikasi Masalah (Code Smell)
Pada kode awal (`ValidatorManager`), ditemukan pelanggaran prinsip SOLID:

### a. Pelanggaran SRP (Single Responsibility Principle)
* **Masalah:** Method `validate` dalam `ValidatorManager` menangani dua logika bisnis yang sangat berbeda: menghitung jatah SKS berdasarkan IPK **dan** mengecek riwayat kelulusan mata kuliah (prasyarat).
* **Dampak:** Jika Rektorat mengubah aturan batas SKS, kita harus mengedit file yang sama yang memuat logika prasyarat. Ini meningkatkan risiko ketidaksengajaan merusak fitur lain.

### b. Pelanggaran OCP (Open/Closed Principle)
* **Masalah:** Kode menggunakan `if type == 'sks': ... elif type == 'prasyarat': ...`.
* **Dampak:** Kode ini **tertutup untuk ekstensi**. Jika ada validasi baru (misalnya: Cek Bebas Pustaka atau Cek Tunggakan UKT), kita terpaksa harus membongkar class `ValidatorManager` dan menambah blok `elif` baru. Ini melanggar prinsip bahwa kelas harus tertutup untuk modifikasi.

### c. Pelanggaran DIP (Dependency Inversion Principle)
* **Masalah:** Sistem bergantung pada implementasi konkret, bukan abstraksi. Pemanggilan validasi dilakukan secara eksplisit dengan string `"sks"` atau `"prasyarat"`.
* **Dampak:** Ketergantungan tinggi (high coupling). Sulit untuk menukar atau menambah validator secara dinamis saat *runtime*.

## 2. Solusi Refactoring

### Implementasi DIP & OCP
Saya membuat abstraksi berupa Abstract Base Class bernama `IValidasiRule`.
* **DIP:** `SistemRegistrasi` sekarang tidak peduli validator apa yang dijalankan, selama validator itu mematuhi kontrak `IValidasiRule`.
* **OCP:** Untuk menambah validasi baru (seperti `AturanKeuangan` pada baris akhir kode), saya cukup membuat class baru yang mewarisi `IValidasiRule` tanpa menyentuh kode `SistemRegistrasi` sama sekali.

### Implementasi SRP
Saya memecah logika validasi menjadi kelas-kelas terpisah:
1.  `AturanSks`: Hanya fokus menghitung matematika IPK vs SKS.
2.  `AturanPrasyarat`: Hanya fokus mengecek list string riwayat mata kuliah.
3.  `AturanKeuangan`: Hanya fokus mengecek status pembayaran.

Setiap kelas kini memiliki satu alasan tunggal untuk berubah.