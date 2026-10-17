# 🔌 API & DX Guild Reference
**Lead:** Diana 'The Closer' Drake (`conversion_copywriter`)  
**Domain:** REST/GraphQL Contract Design, Typed Error Envelopes & Developer Experience

---

## 🎯 Core Invariants
1. **Contract First:** APIs must adhere to explicit contracts (OpenAPI/Swagger or GraphQL SDL); breaking changes require API versioning.
2. **Predictable Errors:** Errors must return consistent envelopes (code, message, details, trace_id) with semantic HTTP status codes.
3. **Idempotent Mutations:** State-modifying requests (payments, creations) must support idempotency keys to avoid double-processing.
4. **Developer-Friendly Documentation:** Every endpoint and CLI command must provide working examples and clear parameter types.

---

## 📋 Quality & Security Checklist
- [ ] Semantic HTTP verbs used correctly (`GET` idempotent/safe, `POST` create, `PUT` replace, `PATCH` partial).
- [ ] Request and response payloads validated with strict schemas (Pydantic / Zod).
- [ ] Pagination follows standard envelope pattern (limit, offset/cursor, next_cursor, total).
- [ ] Deprecated fields marked with Sunset headers and backward-compatibility grace periods.
- [ ] Interactive docs or README examples provide copy-pasteable curl commands that work out of the box.

---

## 🚫 Forbidden Anti-Patterns
- **200 OK Error Responses:** Returning HTTP 200 with `{"error": "Unauthorized"}` in the response body.
- **Leaked Implementation Names:** Exposing internal database table names or backend module paths in API keys.
- **Unversioned Breaking Changes:** Renaming or removing JSON response fields without version increments.
