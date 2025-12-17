import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# ==========================================
# KONFIGURASI LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(name)s %(message)s'
)
LOGGER = logging.getLogger('RegistrationSystem')

# ==========================================
# DATA MODEL
# ==========================================
@dataclass
class Student:
    name: str
    gpa: float # IPK
    sks: int   # Total SKS yang diambil

# ==========================================
# ABSTRACTION (Interface)
# ==========================================
class IValidationRule(ABC):
    """
    Interface dasar untuk semua aturan validasi registrasi.
    Mengikuti prinsip Open/Closed Principle (OCP).
    """
    
    @abstractmethod
    def validate(self, student: Student) -> bool:
        """
        Memvalidasi data mahasiswa berdasarkan aturan tertentu.

        Args:
            student (Student): Objek mahasiswa yang akan divalidasi.

        Returns:
            bool: True jika lolos validasi, False jika gagal.
        """
        pass

# ==========================================
# CONCRETE RULES (Aturan Validasi)
# ==========================================
class NameLengthRule(IValidationRule):
    def validate(self, student: Student) -> bool:
        if len(student.name) < 3:
            LOGGER.warning(f"Validasi Gagal: Nama '{student.name}' terlalu pendek.")
            return False
        return True

class GpaRule(IValidationRule):
    def validate(self, student: Student) -> bool:
        if student.gpa < 2.0:
            LOGGER.warning(f"Validasi Gagal: IPK {student.gpa} tidak mencukupi (Min 2.0).")
            return False
        return True

class SksLimitRule(IValidationRule):
    def validate(self, student: Student) -> bool:
        if student.sks > 24:
            LOGGER.warning(f"Validasi Gagal: SKS {student.sks} melebihi batas (Max 24).")
            return False
        return True

# ==========================================
# MAIN SERVICE (RegistrationService)
# ==========================================
class RegistrationService:
    """
    Service utama untuk menangani proses registrasi mahasiswa.
    Kelas ini bertanggung jawab memanggil semua aturan validasi yang ada.
    """

    def __init__(self, rules: List[IValidationRule]):
        """
        Inisialisasi service dengan daftar aturan validasi.

        Args:
            rules (List[IValidationRule]): List berisi objek rule yang akan dicek.
        """
        self.rules = rules

    def register_student(self, student: Student) -> bool:
        """
        Mendaftarkan mahasiswa setelah melewati serangkaian validasi.

        Args:
            student (Student): Data mahasiswa yang akan didaftarkan.

        Returns:
            bool: True jika registrasi berhasil, False jika ada validasi yang gagal.
        """
        LOGGER.info(f"Memulai registrasi untuk mahasiswa: {student.name}")

        # Loop semua rule (OCP: Kita bisa tambah rule tanpa ubah kode ini)
        for rule in self.rules:
            if not rule.validate(student):
                LOGGER.error(f"Registrasi Ditolak untuk {student.name}.")
                return False
        
        # Jika lolos semua loop
        LOGGER.info(f"Registrasi BERHASIL untuk {student.name}.")
        return True

# ==========================================
# EKSEKUSI PROGRAM
# ==========================================
if __name__ == "__main__":
    print("\n=== SISTEM REGISTRASI MAHASISWA (LOGGING VERSION) ===\n")

    # 1. Setup Aturan (Dependency Injection)
    rules_list = [
        NameLengthRule(),
        GpaRule(),
        SksLimitRule()
    ]

    # 2. Setup Service
    service = RegistrationService(rules_list)

    # 3. Test Case 1: Mahasiswa Sukses
    student_andi = Student("Andi", 3.5, 20)
    service.register_student(student_andi)

    print("\n" + "-"*30 + "\n")

    # 4. Test Case 2: Gagal (SKS Berlebih)
    student_budi = Student("Budi", 3.0, 26) # SKS 26 (Over)
    service.register_student(student_budi)

    print("\n" + "-"*30 + "\n")

    # 5. Test Case 3: Gagal (IPK Rendah)
    student_caca = Student("Caca", 1.5, 18) # IPK 1.5 (Kurang)
    service.register_student(student_caca)