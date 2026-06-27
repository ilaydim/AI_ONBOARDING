# QA Team

The team responsible for quality assurance across all TechNova products — ensuring what we ship works as expected.

## Team Structure
- 4 QA Engineers (1 junior, 2 mid, 1 senior/QA Lead)
- Works embedded within product squads

## Tech Stack
- **E2E Testing**: Playwright (TypeScript)
- **API Testing**: Pytest + requests / Postman collections
- **Performance Testing**: k6
- **Test Management**: Linear (test cases as tickets), Confluence (test plans)
- **Bug Tracking**: Linear (`bug` label)

## Responsibilities
- Writing and maintaining automated test suites
- Manual exploratory testing for new features
- Regression testing before releases
- Performance and load testing
- Test environment management
- Bug reporting and tracking

## Testing Strategy

### Test Pyramid
```
         [E2E Tests]           ← fewer, slower, critical paths
       [Integration Tests]     ← API contracts, service integration
     [Unit Tests]              ← many, fast, developer-owned
```

- **Unit tests**: Developer responsibility (minimum 70% coverage)
- **Integration tests**: QA + developers collaborate
- **E2E tests**: QA-owned, run in CI on staging

### What QA Tests
- All new features before release
- Regression suite on every deploy to staging
- Performance test before major releases
- Security scanning (OWASP ZAP) quarterly

## Bug Severity Levels
| Level | Description | SLA |
|---|---|---|
| P0 - Critical | Production down, data loss | Fix within 2 hours |
| P1 - High | Core feature broken | Fix within 1 day |
| P2 - Medium | Feature degraded, workaround exists | Fix within 1 sprint |
| P3 - Low | Minor issue, cosmetic | Backlog |

## Definition of Done
A feature is "done" when:
1. Unit tests written and passing
2. E2E test written for happy path
3. QA sign-off on staging
4. No P0/P1 bugs open
5. Release notes written
