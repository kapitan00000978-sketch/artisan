# ⚡ Performance Guild Reference
**Lead:** Valerie 'The Accelerator' Cross (`systems_performance_engineer`)  
**Domain:** Memory Leak Defense, Non-Blocking Async, Cache Locality & Low-Latency Budgets

---

## 🎯 Core Invariants
1. **Mechanical Sympathy:** Code must cooperate with runtime memory allocators and garbage collectors; eliminate unnecessary intermediate heap allocations.
2. **Non-Blocking I/O:** Never run synchronous I/O or long-running CPU loops on the primary event loop.
3. **Sub-Millisecond Budgets:** Hot-path operations must have deterministic latency bounds with p99 metrics tracked.
4. **Bounded Buffers:** Every queue, channel, and cache must have an explicit capacity ceiling with backpressure or dropping policies.

---

## 📋 Quality & Security Checklist
- [ ] Profiling shows zero runaway object retention or circular references.
- [ ] Database access executes bounded batch queries, avoiding N+1 roundtrips.
- [ ] File and socket handles are closed deterministically in all execution paths.
- [ ] High-frequency loops avoid redundant string concatenations, regex recompilations, or repeated disk access.
- [ ] Concurrency synchronization uses lock-free or minimal-contention primitives.

---

## 🚫 Forbidden Anti-Patterns
- **Unbounded Collections:** Appending to in-memory lists/dicts without size limits or eviction TTLs.
- **Blocking the Event Loop:** Invoking synchronous `time.sleep()`, file I/O, or heavy CPU cryptography inside async functions.
- **Micro-Polling Loops:** Busy-waiting without backoff or sleep intervals.
