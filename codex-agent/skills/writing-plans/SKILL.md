---
name: writing-plans
description: Tasdiqlangan spetsifikatsiyani mikrotapshiriqlarga bo'lingan, ketma-ket bajariladigan va tekshiruv mezoniga ega bo'lgan mukammal amalga oshirish rejasiga (Implementation Plan) aylantirish mahorati.
---

# 📝 Writing Granular Plans (Amalga Oshirish Rejasi)

Superpowers metodologiyasiga ko'ra, har bir reja shunchalik aniq va tushunarli bo'lishi kerakki, uni hatto kontekstdan bexabar bo'lgan yangi subagent ham 100% to'g'ri bajara olsin.

## Reja Talablari (Plan Specifications):

1. **Kichik va Mustaqil Qadamlar (Atomic Steps):**
   Har bir qadam 5-15 daqiqada bajariladigan bitta aniq o'zgarishdan iborat bo'lishi kerak (masalan: bitta model yaratish, bitta funksiya testini yozish).

2. **Har bir qadam uchun 3 ta majburiy band:**
   - **Fayllar:** Qaysi fayllar o'zgaradi yoki yaratiladi (`[file_path]`).
   - **Harakat:** Aniq nima qilinadi (aniq funksiya yoki parametr nomlari bilan).
   - **Tekshirish (Verification):** Bu qadam to'g'ri bajarilganini qanday isbotlaymiz? (qaysi test yoki terminal buyrug'i bilan).

3. **Reja namunasi:**
   ```markdown
   ### 1-Vazifa: Foydalanuvchi modeli va parollarni shifrlash
   - **Fayllar:** `src/models/user.js`, `tests/user.test.js`
   - **Harakat:** Bcrypt bilan shifrlash metodini yozish.
   - **Test:** `npm test tests/user.test.js` (Failing test yozib, so'ngra ishlatish).
   ```
