---
name: systematic-debugging
description: Har qanday xatolik, bug yoki nosozlikni taxminiy (patch-and-pray) tuzatmasdan, 4 bosqichli ilmiy ildiz sababni aniqlash va tekshirish metodologiyasi.
---

# 🔍 Systematic Debugging (Tizimli Nosozliklarni Qidirish)

Superpowers metodologiyasiga ko'ra: **Hech qachon "balki mana bu ish berar" deb ko'r-ko'rona kodni o'zgartirmang.**

## 4 Bosqichli Ilmiy Sikl:

### 1. Qayta Takrorlash (Reproduce):
- Xatoni barqaror va minimal ssenariy bilan qayta takrorlaydigan test yoki buyruq yozing.
- Xato xabari (Stack trace) va loglarni to'liq o'qing. Taxmin qilmang, faktlarga tayanib ishlang.

### 2. Izolyatsiya Qilish (Isolate):
- Muammo qaysi aniq qatlamda: tarmoqdami, ma'lumotlar bazasidami, serializatsiyadami yoki mantiqiy shartdami?
- Loglar qo'shish yoki bisection orqali muammo manzilini toraytiring.

### 3. Gipoteza Va Tekshiruv (Hypothesize & Validate):
- "Muammo X sababli yuz bermoqda, chunki Y sodir bo'lyapti" degan aniq farazni tuzing.
- Farazni tasdiqlaydigan bitta maqsadli tekshiruv o'tkazing.

### 4. Ildiz Sababni Bartaraf Etish (Root-Cause Fix & Guard):
- Faqatgina alomatni (symptom) emas, muammoning asl ildizini tuzating.
- Xuddi shu xato kelajakda yana qaytmasligi uchun **Regression Test** qo'shing.
- Barcha mavjud testlar muvaffaqiyatli o'tganini tekshiring.
