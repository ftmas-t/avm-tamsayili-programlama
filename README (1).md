# AVM Yatırım Kararı: Tamsayılı Programlama ile Proje Seçimi

Bir inşaat şirketinin 5 alışveriş merkezi projesinden hangilerini yapması gerektiğini, bütçe ve yasal kısıtlar altında toplam kârı en büyükleyecek şekilde belirleyen bir optimizasyon modeli.

## Problem

| AVM | Beklenen kâr (bin TL) | Maliyet (bin TL) |
|---|---|---|
| 1 | 200 | 150 |
| 2 | 150 | 90 |
| 3 | 140 | 50 |
| 4 | 125 | 80 |
| 5 | 180 | 100 |

**Kısıtlar**

- Bütçe en fazla 450 bin TL
- AVM 1, 2 ve 5'ten tam olarak biri yapılmalı
- AVM 3 ve 4'ten en fazla biri yapılabilir
- AVM 4 yapılırsa AVM 5 de yapılmalı

## Model (0–1 tamsayılı programlama)

xⱼ ∈ {0, 1}: j'inci AVM inşa edilirse 1, edilmezse 0

```
maks  Z = 200x₁ + 150x₂ + 140x₃ + 125x₄ + 180x₅

150x₁ + 90x₂ + 50x₃ + 80x₄ + 100x₅ ≤ 450   (bütçe)
x₁ + x₂ + x₅ = 1                            (çoktan seçmeli)
x₃ + x₄ ≤ 1                                 (karşılıklı dışlayıcı)
x₄ ≤ x₅                                     (öncelik / koşullu)
```

## Sonuç

**AVM 1 ve AVM 3 inşa edilmeli → toplam kâr 340 bin TL** (maliyet 200 bin TL).

Sonuç, 32 olası seçimin tamamı denenerek (kaba kuvvet) doğrulanmıştır.

## Çalıştırma

```bash
python3 -m pip install numpy scipy
python3 avm_optimizasyon.py
```

## Kullanılan araçlar

Python, NumPy, SciPy (`scipy.optimize.milp`)

## Notlar

- Kaynak kitapta son kısıt `x₄ = x₅` olarak yazılmıştır. Ancak "4 yapılırsa 5 de yapılmalı" ifadesinin doğru karşılığı `x₄ ≤ x₅`'tir; eşitlik, 5 yapıldığında 4'ü de zorunlu kılar. Bu veri setinde iki versiyon da aynı sonucu verir.
- Kitapta bütçe 450000 olarak yazılmış; tablo bin TL cinsinden olduğu için doğru değer 450'dir.
