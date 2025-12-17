import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# ==========================================
# KONFIGURASI LOGGING (Langkah 2)
# ==========================================
# Konfigurasi dasar: Semua log level INFO ke atas akan ditampilkan
# Format: Waktu Level NamaLogger Pesan
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(name)s %(message)s'
)

# Buat logger khusus untuk modul ini
LOGGER = logging.getLogger('CheckoutSystem')

# ==========================================
# BAGIAN AWAL: MODEL DATA
# ==========================================
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# ==========================================
# INTERFACE (ABSTRAKSI)
# ==========================================
class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    @abstractmethod
    def send(self, order: Order):
        pass

# ==========================================
# IMPLEMENTASI KONKRIT
# ==========================================
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        # Kita gunakan logger juga di sini agar terlihat rapi
        LOGGER.info(f"Payment: Memproses Kartu Kredit untuk {order.customer_name}.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        LOGGER.info(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# ==========================================
# KELAS KOORDINATOR (Langkah 1: Docstring & Langkah 2: Logging)
# ==========================================
class CheckoutService:
    """
    Kelas high-level untuk mengkoordinasi proses transaksi pembayaran.
    Kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP).
    """
    
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Menginisialisasi CheckoutService dengan dependensi yang diperlukan.

        Args:
            payment_processor (IPaymentProcessor): Implementasi interface pembayaran.
            notifier (INotificationService): Implementasi interface notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        """
        Menjalankan proses checkout dan memvalidasi pembayaran.

        Args:
            order (Order): Objek pesanan yang akan diproses.

        Returns:
            bool: True jika checkout sukses, False jika gagal.
        """
        # Logging alih-alih print() (Langkah 2)
        LOGGER.info(f"Memulai checkout untuk {order.customer_name}. Total: {order.total_price}")
        
        # Delegasi ke payment processor
        payment_success = self.payment_processor.process(order)
        
        if payment_success:
            order.status = "paid"
            # Delegasi ke notifier
            self.notifier.send(order)
            
            LOGGER.info("Checkout Sukses. Status pesanan: PAID.")
            return True
        else:
            LOGGER.error("Pembayaran gagal. Transaksi dibatalkan.")
            return False

# ==========================================
# EKSEKUSI & PEMBUKTIAN
# ==========================================

if __name__ == "__main__":
    print("\n=== MULAI PROGRAM (LOGGING VERSION) ===\n")

    # Setup Data
    Febri_order = Order("Febri", 500000)
    email_service = EmailNotifier()

    # Skenario 1: Menggunakan Credit Card
    cc_processor = CreditCardProcessor()
    checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
    
    # Eksekusi
    checkout_cc.run_checkout(Febri_order)

    # Skenario 2: Pembuktian OCP (QRIS)
    print("\n--- Skenario 2: QRIS git init---")
    
    class QrisProcessor(IPaymentProcessor):
        def process(self, order: Order) -> bool:
            LOGGER.info("Payment: Memproses QRIS Code.")
            return True

    budi_order = Order("Budi", 100000)
    qris_processor = QrisProcessor()

    checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)

    checkout_qris.run_checkout(budi_order)
