---
name: adversarial-code-review
description: Yozilgan kod va o'zgarishlarni reja, xavfsizlik, unumdorlik va qat'iy sifat mezonlari asosida shafqatsiz audit (kod taqrizi) qilish mahorati.
---

# 🛡️ Adversarial Code Review (Shafqatsiz Kod Taqrizi)

Superpowers tizimida hech qanday kod "ko'r-ko'rona ma'qullanmaydi" (No rubber-stamping).

## Taqrizchi Qoidalari (Reviewer Directives):

1. **Reja Bilan Muvofiqlik (Plan Adherence):**
   - Kod rejadagi talablarga 100% mos keladimi?
   - Rejadan tashqari ortiqcha yoki ruxsat etilmagan o'zgarishlar kiritilmaganmi?

2. **Xavfsizlik va Edge Cases (Hacker Mindset):**
   - Barcha kiruvchi ma'lumotlar tekshirilganmi?
   - Xatoliklar to'g'ri qayta ishlanadimi (uncaught exceptions yo'qmi)?
   - Resurslar oqishi (memory leaks, unclosed connections) xavfi yo'qmi?

3. **Taqriz Natijasi:**
   - **RAD ETILDI (Changes Requested):** Bitta bo'lsa ham xato yoki shubhali joy bo'lsa, aniq sabab bilan qaytariladi.
   - **QABUL QILINDI (LGTM - Approved):** Faqat barcha tekshiruvlar to'liq va benuqson o'tgandagina beriladi.
