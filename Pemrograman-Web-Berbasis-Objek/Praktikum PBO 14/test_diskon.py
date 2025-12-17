import unittest
from diskon_service import DiskonCalculator

class TestDiskonCalculator(unittest.TestCase):
    
    def setUp(self):
        """Persiapan sebelum setiap tes dijalankan."""
        self.calc = DiskonCalculator()

    def test_diskon_normal(self):
        """Tes 1: Harga 1000 diskon 10% harus jadi 900."""
        hasil = self.calc.hitung_diskon(1000, 10)
        self.assertEqual(hasil, 900.0)

    def test_diskon_nol(self):
        """Tes 2: Diskon 0% harga tetap."""
        hasil = self.calc.hitung_diskon(500, 0)
        self.assertEqual(hasil, 500.0)

    def test_diskon_full(self):
        """Tes 3: Diskon 100% harga jadi 0."""
        hasil = self.calc.hitung_diskon(750, 100)
        self.assertEqual(hasil, 0.0)

    def test_input_negatif(self):
        """Tes 4: Diskon negatif tidak boleh bikin harga turun drastis."""
        hasil = self.calc.hitung_diskon(500, -5)
        self.assertGreaterEqual(hasil, 500)

if __name__ == '__main__':
    unittest.main()