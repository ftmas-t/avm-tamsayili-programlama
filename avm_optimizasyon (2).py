"""
Tamsayılı Programlama ile Yatırım Kararı: AVM Proje Seçimi
===========================================================
Bir inşaat şirketi 5 AVM projesinden hangilerini yapacağına karar veriyor.
Amaç: bütçe ve yasal kısıtlar altında toplam net kârı en büyük yapmak.

Her proje için bir 0-1 (evet/hayır) karar değişkeni kullanılır:
    x_j = 1  -> j'inci AVM inşa edilir
    x_j = 0  -> inşa edilmez

Kütüphane: scipy.optimize.milp (karma tamsayılı doğrusal programlama)
"""

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

# ---------------------------------------------------------------
# 1) Veri (bin TL)
# ---------------------------------------------------------------
projeler = ["AVM 1", "AVM 2", "AVM 3", "AVM 4", "AVM 5"]
kar      = np.array([200, 150, 140, 125, 180])
maliyet  = np.array([150,  90,  50,  80, 100])
butce    = 450

# ---------------------------------------------------------------
# 2) Kısıtlar:  alt_sinir <= A @ x <= ust_sinir
# ---------------------------------------------------------------
A = np.array([
    maliyet,            # (1) Bütçe:              toplam maliyet <= 450
    [1, 1, 0, 0, 1],    # (2) Çoktan seçmeli:     x1 + x2 + x5  = 1
    [0, 0, 1, 1, 0],    # (3) Karşılıklı dışlama: x3 + x4      <= 1
    [0, 0, 0, 1, -1],   # (4) Öncelik:            x4 - x5      <= 0  (4 yapılırsa 5 de yapılır)
])
alt_sinir = [-np.inf, 1, -np.inf, -np.inf]
ust_sinir = [butce,   1, 1,       0]

# ---------------------------------------------------------------
# 3) Çözüm
#    milp enküçükleme yapar; enbüyüklemek için kârı -1 ile çarparız.
# ---------------------------------------------------------------
sonuc = milp(
    c=-kar,
    constraints=LinearConstraint(A, alt_sinir, ust_sinir),
    integrality=np.ones(5),     # tüm değişkenler tamsayı
    bounds=Bounds(0, 1),        # 0 ile 1 arası -> 0-1 değişken
)

# ---------------------------------------------------------------
# 4) Sonuçları yazdır
# ---------------------------------------------------------------
x = np.round(sonuc.x).astype(int)

print("Durum:", "En iyi çözüm bulundu" if sonuc.success else sonuc.message)
print()
print(f"{'Proje':<8}{'Karar':<12}{'Kâr':>6}{'Maliyet':>10}")
for ad, karar, k, m in zip(projeler, x, kar, maliyet):
    print(f"{ad:<8}{'İNŞA ET' if karar else '-':<12}{k:>6}{m:>10}")
print()
print(f"Toplam kâr    : {kar @ x} bin TL")
print(f"Toplam maliyet: {maliyet @ x} / {butce} bin TL")

# ---------------------------------------------------------------
# 5) Kontrol: 2^5 = 32 olası seçimi tek tek deneyip aynı sonucu doğrula
# ---------------------------------------------------------------
from itertools import product

en_iyi = max(
    (np.array(s) for s in product([0, 1], repeat=5)
     if maliyet @ s <= butce and s[0] + s[1] + s[4] == 1
     and s[2] + s[3] <= 1 and s[3] <= s[4]),
    key=lambda s: kar @ s,
)
print(f"\nKaba kuvvet kontrolü: {kar @ en_iyi} bin TL "
      f"({'eşleşti ✓' if kar @ en_iyi == kar @ x else 'EŞLEŞMEDİ ✗'})")
