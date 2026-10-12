# 🛡️ KIBERXAVFSIZLIK VA APPSEC PROTOKOLI

Xavfsizlik yo'nalishidagi AI Agentlar uchun temir qoidalar:

1. **Parollar va Maxfiy Kalitlar:**
   - Hech qanday hardcoded maxfiy kalit (secret) kodda qolishi mumkin emas.
   - Parollar faqat Bcrypt (min 12 rounds) yoki Argon2id bilan shifrlanadi.
2. **OWASP Top 10 Himoyasi:**
   - SQL Injection (faqat parameterized queries / ORM).
   - XSS (barcha foydalanuvchi ma'lumotlari escape qilinadi).
   - CSRF va CORS qat'iy cheklovlar bilan sozlanadi.
3. **Avtorizatsiya va Autentifikatsiya:**
   - JWT tokenlar Access (qisqa) va Refresh Rotation (uzoq) modeli asosida yasaladi.
   - API rate limiting qo'llaniladi.
