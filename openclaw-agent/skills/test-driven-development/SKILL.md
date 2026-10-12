---
name: test-driven-development
description: Qat'iy Test-Driven Development (TDD) sikli: avval qizil (failing) test yozish, so'ngra minimal kod yozib testni yashil (passing) qilish va oxirida refaktoring qilish.
---

# 🔴🟢🔵 Test-Driven Development (TDD Protocol)

Superpowers tizimining oltin qoidasi: **Muvaffaqiyatsiz (qizil) test yozilmagunicha, bitta ham qator ishlab chiqarish kodi yozilmaydi.**

## TDD Uchburchagi (Red -> Green -> Refactor):

1. **1-QADAM: QIZIL (RED) — Test yozish va xatolikni ko'rish:**
   - Kutilayotgan xatti-harakat uchun test yozing.
   - Testni ishga tushiring va uning aynan kutilgan sabab bilan yiqilishini (fail) o'z ko'zingiz bilan tasdiqlang.
   - *Agar test darhol o'tib ketsa — demak test noto'g'ri yozilgan yoki sinov o'rinsiz!*

2. **2-QADAM: YASHIL (GREEN) — Minimal ishlaydigan kod:**
   - Testni o'tkazish uchun zarur bo'lgan eng sodda va to'g'ri kodni yozing.
   - Ortiqcha keraksiz arxitekturani qo'shmang, faqat testni o'tkazing.
   - Testni qayta ishga tushiring: barcha testlar yashil (pass) bo'lishi shart.

3. **3-QADAM: REFAKTORING (REFACTOR) — Tozalash:**
   - Kodni tartibga soling, takrorlanishlarni (DRY) yo'qoting, o'zgaruvchi nomlarini chiroyli qiling.
   - Testlar yana yashil ekanligiga ishonch hosil qiling.

## Qat'iy Taqiqlangan:
- Test yozmasdan turib kod berish.
- Testni keyinga surish ("keyinroq test qo'shib qo'yamiz" degan gap Usta uchun taqiqlangan).
