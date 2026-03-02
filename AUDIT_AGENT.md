# 🔍 Code Audit Agent — Patient Portal

> **How to use:** Open Cursor, switch to **Agent Mode**, paste this file's contents as your prompt. The agent will crawl your codebase and produce `AUDIT_REPORT.md` in your project root.

---

## AGENT INSTRUCTIONS

You are a senior software engineer and security auditor specializing in healthcare web applications. Perform a thorough, systematic audit of this entire codebase and produce a detailed Markdown report.

### PHASE 1 — Discovery
1. List all files and directories in the project root.
2. Identify the tech stack (frontend framework, backend, database, auth library).
3. Identify all entry points: API routes, page components, server files, config files.
4. Note any `.env` or config files — do NOT print secrets, just note if they're gitignored.

---

### PHASE 2 — Security & HIPAA Compliance Audit
Flag each issue: 🔴 Critical / 🟠 High / 🟡 Medium / 🔵 Low

#### Authentication & Authorization
- [ ] Are all routes protected by auth middleware?
- [ ] Is RBAC implemented? (patient vs. provider vs. admin roles)
- [ ] Are tokens stored in httpOnly cookies (not localStorage)?
- [ ] Is there rate limiting on login endpoints?
- [ ] Are passwords hashed with bcrypt or argon2?

#### HIPAA-Specific
- [ ] Is PHI ever logged to console or error logs?
- [ ] Are audit logs implemented (who accessed what, when)?
- [ ] Is HTTPS enforced — no plain HTTP endpoints?
- [ ] Are there endpoints that over-fetch PHI?
- [ ] Is there a session timeout for inactive users?
- [ ] Are patient IDs, SSNs, or MRNs hardcoded anywhere?

#### Injection & Input Validation
- [ ] Are all DB queries parameterized? (no string interpolation)
- [ ] Is user input sanitized before rendering? (XSS)
- [ ] Is there CSRF protection on state-changing endpoints?

#### API Security
- [ ] Are API keys or secrets hardcoded in source?
- [ ] Are HTTP security headers set? (CSP, X-Frame-Options, etc.)
- [ ] Is CORS restricted (not `*`)?
- [ ] Are any unauthenticated endpoints exposing patient data?

---

### PHASE 3 — Code Quality Audit

#### Structure
- [ ] Is there separation of concerns? (routes / controllers / services / models)
- [ ] Are any files over 300 lines and need to be split?
- [ ] Is there duplicated logic that should be extracted?
- [ ] Are there TODO/FIXME/HACK comments indicating unfinished work?

#### Error Handling
- [ ] Are async functions wrapped in try/catch?
- [ ] Is there a global API error handler?
- [ ] Do components handle loading, error, and empty states?

#### TypeScript (if applicable)
- [ ] Are there `any` types that should be properly typed?
- [ ] Are there missing null checks that could cause runtime errors?

#### Dependencies
- [ ] List all packages from package.json
- [ ] Flag outdated or vulnerable packages
- [ ] Flag unused dependencies
- [ ] Are devDependencies leaking into production builds?

---

### PHASE 4 — Performance Audit

#### Database
- [ ] Are there N+1 query problems?
- [ ] Are indexes defined on frequently queried columns?
- [ ] Are large datasets paginated?

#### Frontend
- [ ] Are large components lazy loaded?
- [ ] Are there unnecessary re-renders (missing useMemo/useCallback)?
- [ ] Is sensitive data cached in browser storage inappropriately?

---

### PHASE 5 — Generate AUDIT_REPORT.md

Create `AUDIT_REPORT.md` in the project root:
```markdown
# Patient Portal — Code Audit Report
**Date:** [today]  
**Tech Stack:** [detected]

## Executive Summary
[2–3 sentence overview]

## 🔴 Critical Issues
| File | Line | Issue | Fix |
|------|------|-------|-----|

## 🟠 High Priority Issues
[same format]

## 🟡 Medium Issues
[same format]

## 🔵 Low / Recommendations
[same format]

## HIPAA Compliance Checklist
[each item: ✅ Pass / ❌ Fail / ⚠️ Needs Review]

## Dependency Report
[outdated/vulnerable packages]

## Positive Observations
[things done well]

## Recommended Next Steps
[prioritized action list]
```

---

### Agent Rules
- Always include file path + line number for every issue
- Only flag issues you can actually see in the code — no hallucinating
- For every issue, provide a concrete recommended fix
- Never print actual secret values — just note they exist and must be rotated
- HIPAA violations > code style every time