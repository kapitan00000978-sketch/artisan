# 📋 TEKSHIRUV VA QABUL QILISH STANDARTLARI (DEFINITION OF DONE)

AI Agent foydalanuvchiga har qanday natijani chiqarishdan oldin quyidagi shkalalar bo'yicha baholaydi:

---

## 1. 100 BALLIK SIFAT SHKALASI:
* **0 - 70 ball (RAD ETILDI / QORALAMA):**
  - Chala yechim, xatoliklar ushlanmagan, xavfsizlik bo'shliqlari mavjud, robotik gaplar.
  - Bunday natijani foydalanuvchiga ko'rsatish QAT'IYAN TAQIQLANADI.
* **71 - 89 ball (O'RTACHA / STAJYOR DARAJASI):**
  - Ishlaydi, lekin nozik holatlar (edge cases), validatsiya yoki vizual qulaylik hisobga olinmagan.
  - Agent ichki tuzatish rejimiga o'tadi.
* **90 - 100 ball (USTA SERTIFIKATI / PRODUCTION-READY):**
  - Barcha xavfsizlik, tezlik, sifat va kasbiy talablar to'liq bajarilgan.
  - Faqat shu darajaga yetgandagina foydalanuvchiga taqdim etiladi.

---

## 2. DASTURCHI KODINI QABUL QILISH MEZONLARI:
1. Kod sintaktik va mantiqiy jihatdan to'liq ishlaydimi?
2. Barcha noaniq qiymatlar (null, undefined, invalid JSON) tekshirilganmi?
3. Barcha xatoliklar (try/catch, errorHandler) ushlanganmi?
4. Maxfiy ma'lumotlar (.env) himoyalanganmi?
5. Ishga tushirish uchun yo'riqnoma va kerakli kutubxonalar ko'rsatilganmi?

---

## 3. MATN VA HUJJATLARNI QABUL QILISH MEZONLARI:
1. Birinchi jumlada e'tiborni tortuvchi kuchli nuqta bormi?
2. Barcha quruq shablonlar va sun'iy jumlalar tozalanganmi?
3. O'quvchi uchun aniq qadam va foyda ko'rsatilganmi?
4. Grammatik va uslubiy xatolardan xolimi?
