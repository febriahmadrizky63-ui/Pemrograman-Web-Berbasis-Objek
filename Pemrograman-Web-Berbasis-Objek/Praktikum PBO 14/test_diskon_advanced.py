import unittest
from diskon_service import DiskonCalculator

class TestDiskonLanjut(unittest.TestCase):
    
    def setUp(self):
        self.calc = DiskonCalculator()

    def test_diskon_float_ganjil(self):
        """
        Tes 5: Menguji angka desimal (float).
        Kasus: Harga 999 dengan diskon 33%.
        Hitungan manual: 999 * 33 / 100 = 329.67.
        Harga Akhir: 999 - 329.67 = 669.33.
        """
        hasil = self.calc.hitung_diskon(999, 33)
        
        # Kita pakai assertAlmostEqual karena komputer kadang 
        # menghitung koma dengan sedikit selisih (misal 669.330000001)
        self.assertAlmostEqual(hasil, 669.33, places=2)

    def test_edge_case_nol(self):
        """Tes 6: Menguji jika harga awalnya 0."""
        hasil = self.calc.hitung_diskon(0, 50)
        self.assertEqual(hasil, 0.0)

if __name__ == '__main__':
    unittest.main()