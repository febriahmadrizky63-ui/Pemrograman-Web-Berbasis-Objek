from abc import ABC, abstractmethod
from dataclasses import dataclass

# ==========================================
# BAGIAN AWAL: MODEL DATA (Harus Paling Atas)
# ==========================================
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# ==========================================
# LANGKAH 1: KODE BERMASALAH (The God Class)
# ==========================================
# Kita tulis ini hanya sebagai contoh kode buruk.
# Tidak kita pakai di program utama agar tidak bingung.

class OrderManager: # Melanggar SRP, OCP, DIP
    def process_checkout(self, order: Order, payment_method: str):
        print(f"Memulai checkout untuk {order.customer_name}...")
        
        # LOGIKA PEMBAYARAN (Pelanggaran OCP/DIP)
        if payment_method == "credit_card":
            print("Processing Credit Card...")
        elif payment_method == "bank_transfer":
            print("Processing Bank Transfer...")
        else:
            print("Metode tidak valid.")
            return False
            
        # LOGIKA NOTIFIKASI (Pelanggaran SRP)
        print(f"Mengirim notifikasi ke {order.customer_name}...")
        order.status = "paid"
        return True

# ==========================================
# LANGKAH 2: REFACTORING (SOLID)
# ==========================================

# 1. Definisi Kontrak/Interface (ABSTRAKSI)
# (Harus ditulis SEBELUM kelas yang memakainya)
class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    @abstractmethod
    def send(self, order: Order):
        pass

# 2. Implementasi Konkrit (Plug-in)
# (Kelas ini mewarisi Interface di atas)
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# 3. Kelas Koordinator (CheckoutService)
# (Menggunakan Dependency Injection)
class CheckoutService:
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        # DIP: Kita simpan abstraksinya, bukan konkretnya
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order):
        # Delegasi ke payment processor
        payment_success = self.payment_processor.process(order)
        
        if payment_success:
            order.status = "paid"
            # Delegasi ke notifier
            self.notifier.send(order)
            print("Checkout Sukses.")
            return True
        return False

# ==========================================
# LANGKAH 3: EKSEKUSI & PEMBUKTIAN OCP
# ==========================================

print("=== MULAI PROGRAM ===")

# Setup Data
febri_order = Order("Febri", 500000)
email_service = EmailNotifier()

# Skenario 1: Menggunakan Credit Card
print("\n--- Skenario 1: Credit Card ---")
cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
checkout_cc.run_checkout(febri_order)

# Skenario 2: Menambah Metode QRIS (Pembuktian OCP)
# Kita buat kelas baru di sini tanpa mengubah CheckoutService di atas
print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")

class QrisProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses QRIS Code.")
        return True

budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()

# Inject QRIS processor ke CheckoutService
checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)

checkout_qris.run_checkout(budi_order)
