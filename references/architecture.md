# 🏛️ Architecture Guild Reference
**Lead:** Marcus 'The Vanguard' Sterling (`software_architect`)  
**Domain:** Clean Modular Architecture, Dependency Injection, Circuit Breakers & Resilience

---

## 🎯 Core Invariants
1. **Explicit Boundaries:** Components must communicate across well-defined interfaces; no hidden global state or tight circular couplings.
2. **Zero Stubs:** Code must be fully implemented; zero `// TODO`, `// FIXME`, or placeholder pass bodies in production paths.
3. **Fail Fast with Grace:** Unrecoverable invariant violations fail immediately; transient network dependencies must use Circuit Breakers and timeouts.
4. **Dependency Inversion:** Depend upon abstractions, not concrete implementations. Service instantiation occurs at the composition root.

---

## 📋 Quality & Security Checklist
- [ ] Explicit interfaces/abstract classes decoupling high-level policy from low-level details.
- [ ] Configurable timeouts and fallback strategies on every external network call.
- [ ] No bare exception catches or swallowed failures (`except: pass` strictly forbidden).
- [ ] Comprehensive unit verification covering both happy paths and edge failure modes.
- [ ] Resource cleanup guaranteed via deterministic context managers (`with`, `using`, `try...finally`).

---

## 🚫 Forbidden Anti-Patterns
- **God Objects / Monolith Modules:** Mixing business logic, persistence, and HTTP handling in a single class or file.
- **Hidden Side Effects:** Functions mutating arguments or reading ambient environment without explicit declaration.
- **Premature Concurrency:** Adding threads/processes without proving memory barrier safety and lock contention budgets.
