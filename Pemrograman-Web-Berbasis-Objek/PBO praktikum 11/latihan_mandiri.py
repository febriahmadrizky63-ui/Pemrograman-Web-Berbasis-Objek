from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

# ==========================================
# 0. DATA MODEL (Entitas Dasar)
# ==========================================
@dataclass
class Mahasiswa:
    nama: str
    ipk: float
    sks_diambil: int
    # List mata kuliah yang sudah lulus
    riwayat_matkul: List[str] = field(default_factory=list)

@dataclass
class MataKuliah:
    nama: str
    sks: int
    prasyarat: str = None  # Nama matkul prasyarat, misal: "Algoritma"

# ==========================================
# 1. KODE BURUK (Violation of SOLID)
# ==========================================
print("=== [1] CONTOH KODE BURUK (GOD CLASS) ===")

class ValidatorManager:
    """
    Kelas ini melanggar:
    - SRP: Mengurusi logika SKS DAN Prasyarat sekaligus.
    - OCP: Harus diubah (edit kodingan) jika ada validasi baru (misal: Cek Keuangan).
    """
    def validate(self, mhs: Mahasiswa, mk: MataKuliah, jenis_validasi: str):
        # Logika Validasi SKS
        if jenis_validasi == "sks":
            batas_sks = 24 if mhs.ipk >= 3.00 else 20
            if (mhs.sks_diambil + mk.sks) > batas_sks:
                print(f"[X] Gagal SKS: {mhs.nama} kelebihan SKS.")
                return False
            print("[v] Cek SKS OK.")
            return True
        
        # Logika Validasi Prasyarat
        elif jenis_validasi == "prasyarat":
            if mk.prasyarat and mk.prasyarat not in mhs.riwayat_matkul:
                print(f"[X] Gagal Prasyarat: Belum lulus {mk.prasyarat}.")
                return False
            print("[v] Cek Prasyarat OK.")
            return True
            
        else:
            print("Validasi tidak dikenal.")
            return False

# Simulasi Kode Buruk
bad_validator = ValidatorManager()
budi = Mahasiswa("Budi", ipk=2.5, sks_diambil=18, riwayat_matkul=[])
mk_berat = MataKuliah("Struktur Data", sks=3, prasyarat="Algoritma")

bad_validator.validate(budi, mk_berat, "sks")
bad_validator.validate(budi, mk_berat, "prasyarat")


# ==========================================
# 2. IMPLEMENTASI SOLID (REFACTORING)
# ==========================================
print("\n=== [2] HASIL REFACTORING (SOLID) ===")

# --- A. ABSTRAKSI (Implementasi DIP & OCP) ---
class IValidasiRule(ABC):
    """
    Kontrak (Interface): Semua aturan validasi WAJIB punya method validate.
    High-level module tidak perlu tahu detail aturan, cukup tahu kontrak ini.
    """
    @abstractmethod
    def validate(self, mhs: Mahasiswa, mk: MataKuliah) -> bool:
        pass

# --- B. IMPLEMENTASI KONKRIT (Implementasi SRP) ---
# Memecah logika menjadi kelas-kelas kecil (Satu kelas = Satu Aturan)

class AturanSks(IValidasiRule):
    def validate(self, mhs: Mahasiswa, mk: MataKuliah) -> bool:
        batas_sks = 24 if mhs.ipk >= 3.00 else 20
        total_rencana = mhs.sks_diambil + mk.sks
        
        if total_rencana > batas_sks:
            print(f"[SOLID-Fail] SKS Penuh. Batas: {batas_sks}, Total: {total_rencana}")
            return False
        print("[SOLID-OK] SKS Aman.")
        return True

class AturanPrasyarat(IValidasiRule):
    def validate(self, mhs: Mahasiswa, mk: MataKuliah) -> bool:
        if mk.prasyarat and mk.prasyarat not in mhs.riwayat_matkul:
            print(f"[SOLID-Fail] Belum lulus prasyarat: {mk.prasyarat}")
            return False
        print("[SOLID-OK] Prasyarat Terpenuhi.")
        return True

# --- C. KELAS KOORDINATOR (Dependency Injection) ---
class SistemRegistrasi:
    def __init__(self, daftar_aturan: List[IValidasiRule]):
        # DIP: Bergantung pada Abstraksi (IValidasiRule), bukan kelas konkret
        self.aturan = daftar_aturan

    def daftar_matkul(self, mhs: Mahasiswa, mk: MataKuliah):
        print(f"\n--- Memproses KRS: {mhs.nama} mengambil {mk.nama} ---")
        
        # Iterasi semua aturan yang disuntikkan (Open/Closed Principle)
        for aturan in self.aturan:
            if not aturan.validate(mhs, mk):
                print(">>> Hasil: DITOLAK sistem.")
                return
        
        print(">>> Hasil: BERHASIL ditambahkan ke KRS.")

# ==========================================
# 3. EKSEKUSI & PEMBUKTIAN OCP
# ==========================================

# Data Mahasiswa: Andi (IPK Bagus, tapi belum ambil Algoritma)
febri = Mahasiswa("Febri", ipk=3.8, sks_diambil=20, riwayat_matkul=[])
mk_tujuan = MataKuliah("Pemrograman Lanjut", sks=3, prasyarat="Algoritma")

# Skenario: Validasi Standar
aturan_standar = [AturanSks(), AturanPrasyarat()]
sistem = SistemRegistrasi(aturan_standar)
sistem.daftar_matkul(febri, mk_tujuan)

# --- PEMBUKTIAN OCP (CHALLENGE) ---
# Menambah aturan baru TANPA mengubah kelas SistemRegistrasi
print("\n[Challenge] Menambah Aturan Validasi Tagihan (Pembuktian OCP)")

class AturanKeuangan(IValidasiRule):
    def validate(self, mhs: Mahasiswa, mk: MataKuliah) -> bool:
        status_lunas = False # Simulasi belum bayar
        if not status_lunas:
            print("[SOLID-Fail] Mahasiswa ada tunggakan pembayaran.")
            return False
        return True

# Inject aturan baru ke sistem
aturan_ketat = [AturanSks(), AturanPrasyarat(), AturanKeuangan()]
sistem_baru = SistemRegistrasi(aturan_ketat)

# Tes ulang
sistem_baru.daftar_matkul(febri, mk_tujuan)