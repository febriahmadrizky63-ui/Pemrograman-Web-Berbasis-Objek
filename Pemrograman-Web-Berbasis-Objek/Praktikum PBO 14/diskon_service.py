import pdb

class DiskonCalculator:
    """Menghitung harga akhir setelah diskon."""
    
    def hitung_diskon(self, harga_awal: float, persentase_diskon: int) -> float:
        # pdb.set_trace() # <--- Kita matikan debugger karena sudah ketemu bugnya
        
        # RUMUS YANG BENAR (Sudah dibagi 100)
        jumlah_diskon = (harga_awal * persentase_diskon) / 100
        
        harga_akhir = harga_awal - jumlah_diskon
        return harga_akhir

# --- UJI COBA MANUAL ---
if __name__ == '__main__':
    calc = DiskonCalculator()
    hasil = calc.hitung_diskon(1000, 10)
    print(f"Hasil Akhir: {hasil}")