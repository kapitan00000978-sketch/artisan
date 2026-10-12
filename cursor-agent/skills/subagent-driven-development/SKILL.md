---
name: subagent-driven-development
description: Murakkab rejalarni mustaqil subagentlar zanjiriga topshirish, ularning har bir natijasini alohida nazoratdan o'tkazish va birlashtirish mahorati.
---

# 🤖 Subagent-Driven Development (Avtonom Subagentlar Quvuri)

Katta vazifalar yagona kontekstda bajarilganda agentlar charchaydi yoki tafsilotlarni unuta boshlaydi. Superpowers bu muammoni **Subagentlar Zanjiri** orqali hal qiladi.

## Ishlash Tartibi:

1. **Rejani Bo'lib Berish:**
   - Har bir subagentga faqat `writing-plans` orqali tuzilgan bitta aniq mikrotapshiriq beriladi.
   - Har bir subagentga o'z vazifasining kutilayotgan natijasi va qabul qilish testi yetkaziladi.

2. **Har Qadamda Nazorat Gate'i (Review Gate):**
   - Subagent vazifani bajarib, testdan o'tkazgach, natija darhol qabul qilinmaydi.
   - Bosh nazoratchi (Critic) o'zgarishlarni tekshiradi:
     * *Faqat belgilangan fayllar o'zgardimi?*
     * *Boshqa narsalar buzilmadimi?*
     * *Testlar yashilmi?*

3. **Keyingi Qadamga O'tish:**
   - Faqat tekshiruvdan o'tgan qadam qabul qilinadi va keyingi subagent navbatdagi vazifani boshlaydi.
   - Bu butun tizimning barqaror va xatosiz yig'ilishini ta'minlaydi.
