# TechNova — General Processes & Tools

## Development Process

### Git & Version Control
- **Branching**: `main` is always deployable. Feature branches: `feature/<ticket-id>-short-desc`
- **Commits**: Conventional commits format (`feat:`, `fix:`, `chore:`, `docs:`)
- **PR size**: Aim for <400 lines changed. Large PRs require justification.
- **Squash merge**: All PRs squash-merged to main for clean history.

### Sprint Process (2-week sprints)
1. **Sprint Planning** (Monday, Week 1): Tickets pulled from backlog, effort estimated
2. **Development**: Feature branches, daily standups
3. **Code Review**: All PRs reviewed within 1 business day
4. **QA**: Tickets moved to QA when PR merged to staging
5. **Retrospective** (Friday, Week 2): What went well, what to improve
6. **Release** (Friday, Week 2): Tagged release deployed to production

### Ticket Management (Linear)
- All work tracked in Linear tickets
- Labels: `bug`, `feature`, `tech-debt`, `ops`
- Priority: P0 (critical), P1 (high), P2 (medium), P3 (low)
- Ticket format: `[TEAM-###] Short title`

## Deployment Pipeline

### Environments
- **local**: Developer machines
- **staging**: Auto-deployed on merge to `main`, used for QA
- **production**: Manual trigger, requires release tag

### CI/CD (GitHub Actions)
1. PR opened → lint, unit tests, integration tests run
2. All checks pass → PR can be merged
3. Merge to main → auto-deploy to staging
4. Release tag pushed → deploy to production via ArgoCD

### Monitoring & Observability
- **Metrics**: Datadog dashboards per service
- **Logs**: Structured JSON logs → Datadog Log Management
- **Alerts**: PagerDuty for P0/P1 incidents
- **Traces**: Distributed tracing via Datadog APM

## Communication Tools

| Tool | Purpose |
|------|---------|
| Slack | Real-time messaging, async standups |
| Linear | Issue tracking, sprint management |
| Confluence | Documentation, ADRs, runbooks |
| GitHub | Source code, PRs, CI/CD |
| Zoom | Video calls, all-hands |
| PagerDuty | On-call alerting |
| Datadog | Monitoring & observability |

## Incident Management
1. P0 incident triggered → PagerDuty alerts on-call engineer
2. Incident channel created in Slack (`#incident-YYYY-MM-DD`)
3. Root cause investigation
4. Fix deployed, incident resolved
5. Blameless post-mortem written within 48 hours and shared with all-hands
