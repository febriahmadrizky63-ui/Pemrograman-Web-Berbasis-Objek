# LAPORAN DEBUGGING (DEBUG_REPORT)

## 1. Deskripsi Bug
Ditemukan kesalahan perhitungan di mana hasil akhir lebih tinggi dari yang seharusnya. 
Dugaan awal: Ada penambahan pajak (PPN) sebesar 10% yang tidak sengaja tertulis di dalam rumus, padahal fitur PPN belum diminta.

## 2. Proses Penelusuran (Tracing)
Saya menggunakan `pdb` untuk melihat nilai variabel saat runtime. Berikut adalah log simulasi dari terminal:

(Pdb) n
> e:\praktikum\diskon_service.py(10)hitung_diskon()
-> harga_akhir = harga_awal - jumlah_diskon + (harga_awal * 0.1)

(Pdb) p harga_akhir
1100.0
(Pdb) p jumlah_diskon
100.0
(Pdb) p harga_awal * 0.1
100.0  <-- INI PENYEBABNYA (PPN 10% Masuk)

## 3. Perbaikan (Fix)
Saya menghapus bagian `+ (harga_awal * 0.1)` dari baris kode `harga_akhir`.

**Kode Sebelum:**
`harga_akhir = harga_awal - jumlah_diskon + (harga_awal * 0.1)`

**Kode Sesudah:**
`harga_akhir = harga_awal - jumlah_diskon`