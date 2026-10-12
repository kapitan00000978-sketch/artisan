# 💻 DASTURIY ARXITEKTURA VA MUHANDISLIK STANDARTLARI

Dasturchi AI Agentlar uchun qat'iy talablar:

1. **Type Safety & Validatsiya:**
   - Hech qanday `any` tipi yo'q. Barcha kiruvchi ma'lumotlar Zod, Pydantic yoki qat'iy schema bilan validatsiya qilinadi.
2. **Crash-Proof Error Handling:**
   - Har bir tashqi I/O operatsiyasi (DB, API, Fayl) `try/catch` bilan himoyalanadi.
   - Markaziy xatolik boshqaruvchisi (Global Error Handler) bo'lishi shart.
3. **Resurslar va Xotira Himoyasi:**
   - Har bir ochilgan ulanish (Database connection, Redis client, File descriptor) to'g'ri yopiladi.
   - DoS va xotira to'lib ketishining oldini olish uchun request body size limits qo'yiladi.
