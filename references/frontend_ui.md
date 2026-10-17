# 🎨 Frontend & UI/UX Guild Reference
**Lead:** Elena 'The Visionary' Rostova (`ui_ux_designer`)  
**Domain:** Design Systems, WCAG Accessibility (A11y), Core Web Vitals & Ergonomics

---

## 🎯 Core Invariants
1. **Accessibility by Default:** All interactive elements must support keyboard navigation, ARIA landmarks, and meet WCAG AA contrast (4.5:1).
2. **Core Web Vitals:** First Contentful Paint < 1.2s, Largest Contentful Paint < 2.5s, Cumulative Layout Shift < 0.1.
3. **Design System Tokens:** Spacing, typography, and color palettes must derive from centralized design tokens; no arbitrary hardcoded pixels.
4. **Resilient Feedback:** Every asynchronous user interaction must display loading indicators and graceful error states.

---

## 📋 Quality & Security Checklist
- [ ] Keyboard focus states are visually distinctive and never suppressed (`outline: none` without replacement forbidden).
- [ ] Form inputs have associated `<label>` elements and explicit validation feedback.
- [ ] Responsive layout verified across mobile (375px), tablet (768px), and desktop (1440px) viewports.
- [ ] External links include `rel="noopener noreferrer"`.
- [ ] Animations use GPU-accelerated properties (`transform`, `opacity`) and respect `prefers-reduced-motion`.

---

## 🚫 Forbidden Anti-Patterns
- **Unlabeled Icon Buttons:** Interactive buttons containing only an icon without `aria-label` or screen-reader text.
- **Layout Shifts:** Images and dynamic embeds rendered without explicit `width` and `height` dimensions.
- **Silent Network Drops:** Failing an API call on form submission without notifying the user.
