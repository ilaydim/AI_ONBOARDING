# QA — Technologies, Links & Standards

## Internal Resources
- **Confluence**: `QA` space — test plans, test strategies, bug templates
- **Linear**: All bugs tracked with `bug` label, severity in title
- **GitHub**: `technova/qa-automation` — Playwright + k6 test suites
- **Postman**: `TechNova API` collection (shared workspace)
- **Datadog**: Synthetic monitoring for critical flows

## Tech Documentation

### Playwright (E2E Testing)
- Tests in `tests/e2e/` directory
- Page Object Model pattern
- Run against staging before every production release
```bash
# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/login.spec.ts

# Run in UI mode (debugging)
npx playwright test --ui

# Generate report
npx playwright show-report
```

### Pytest (API Testing)
- Tests in `tests/api/`
- Fixtures for auth tokens, test data setup/teardown
```bash
# Run API tests
pytest tests/api/ -v

# Run with coverage
pytest tests/api/ --cov=. --cov-report=html
```

### k6 (Performance Testing)
- Scripts in `tests/performance/`
- Run before major releases or when load characteristics change
```bash
# Smoke test (1 VU, 1 minute)
k6 run tests/performance/smoke.js

# Load test (50 VUs, 10 minutes)
k6 run --vus 50 --duration 10m tests/performance/load.js
```

## Bug Reporting Template
```
**Title**: [P1] Login fails with special characters in password

**Environment**: Staging / Production
**Browser/Client**: Chrome 120 / API
**Steps to Reproduce**:
1. Go to login page
2. Enter username with special chars
3. Click Login

**Expected**: Login succeeds
**Actual**: 500 error returned

**Logs/Screenshots**: [attached]
```

## Test Coverage Standards
- New features: Happy path E2E test required before release
- Bug fixes: Regression test required (so it never recurs)
- APIs: Contract tests for all public endpoints
- Performance: Baseline established for all P0 user flows

## Key Contacts
- **QA Lead**: Test strategy, automation architecture
- **#qa** Slack: QA team discussions
- **#bugs** Slack: Bug triage and prioritization
- **#releases** Slack: Release coordination
