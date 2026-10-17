# 🛡️ Security Guild Reference
**Lead:** Gabriel 'The Sentinel' Frost (`cybersecurity_auditor`)  
**Domain:** OWASP Top 10, Zero-Trust Architecture, Secret Protection & Input Sanitization

---

## 🎯 Core Invariants
1. **Never Trust Input:** All external parameters (query, headers, body, cookies) must be strictly validated against typed schemas before execution.
2. **Zero Hardcoded Secrets:** Passwords, API tokens, private keys, and HMAC secrets must reside in environment variables or vault backends; never in code or logs.
3. **Constant-Time Verification:** Secrets, hashes, and token signatures must be compared using constant-time algorithms (`hmac.compare_digest`, `crypto.timingSafeEqual`) to eliminate timing attacks.
4. **Parameterized Data Access:** Dynamic SQL queries with string concatenation or interpolation are strictly banned.

---

## 📋 Quality & Security Checklist
- [ ] Defense against SQLi, XSS, SSRF, IDOR, and command injection verified.
- [ ] Passwords hashed using memory-hard KDFs (Argon2id or bcrypt with cost >= 12).
- [ ] JWT tokens mandate explicit signature validation, valid expiration (`exp`), and algorithm pinning (HS256/RS256, rejecting `none`).
- [ ] Principle of least privilege enforced across database connections and API scopes.
- [ ] Rate limiting and brute-force protection applied to authentication endpoints.

---

## 🚫 Forbidden Anti-Patterns
- **Raw Dynamic Execution:** Using `eval()`, `exec()`, or unsanitized shell subprocess calls.
- **Leaked Stack Traces:** Surfacing internal stack traces or database schema errors in client HTTP responses.
- **Plain Text Storage:** Persisting secrets or sensitive tokens in plaintext within databases or caching layers.
