# Tasks — Backend Development

## Task: Learn the Company Architecture
- **ID:** backend-001
- **Level:** junior, mid, senior
- **Dependency:** None
- **Expected Output:** Summarize the architecture in your own words and explain the 3 main components
- **Completion Criteria:** Correctly identify at least 3 components and explain the relationships between them
- **Estimated Duration:** 1 hour
- **Skippable:** No

## Task: Set Up Local Environment
- **ID:** backend-002
- **Level:** junior, mid
- **Dependency:** backend-001
- **Expected Output:** Application running on your local machine
- **Completion Criteria:** `uvicorn` is running and the `/health` endpoint returns 200
- **Estimated Duration:** 2 hours
- **Skippable:** Yes

## Task: Start the First Service
- **ID:** backend-003
- **Level:** junior, mid
- **Dependency:** backend-002
- **Expected Output:** Auth service running in local environment
- **Completion Criteria:** Login endpoint responds correctly to a test request
- **Estimated Duration:** 1.5 hours
- **Skippable:** Yes

## Task: Review the CI/CD Pipeline
- **ID:** backend-004
- **Level:** junior, mid, senior
- **Dependency:** backend-001
- **Expected Output:** Explain the pipeline steps and triggers
- **Completion Criteria:** Read the GitHub Actions workflow file and list 5 steps in order
- **Estimated Duration:** 1 hour
- **Skippable:** No

## Task: Learn Code Review Standards
- **ID:** backend-005
- **Level:** junior, mid, senior
- **Dependency:** backend-001
- **Expected Output:** Summarize PR standards and reviewer expectations
- **Completion Criteria:** Correctly state 4 PR rules
- **Estimated Duration:** 0.5 hours
- **Skippable:** No

## Task: Open Your First PR
- **ID:** backend-006
- **Level:** junior, mid, senior
- **Dependency:** backend-005
- **Expected Output:** Open a PR with a small improvement or typo fix
- **Completion Criteria:** PR is opened and receives at least 1 comment
- **Estimated Duration:** 2 hours
- **Skippable:** No

## Task: Review Architecture Decision Records (ADR)
- **ID:** backend-007
- **Level:** mid, senior
- **Dependency:** backend-001
- **Expected Output:** Summarize the last 3 ADRs and explain the rationale behind each decision
- **Completion Criteria:** 3 ADRs summarized and the "why this decision?" question answered
- **Estimated Duration:** 2 hours
- **Skippable:** Yes

## Task: Evaluate the Technical Debt Report
- **ID:** backend-008
- **Level:** senior
- **Dependency:** backend-007
- **Expected Output:** List current technical debt areas in order of priority
- **Completion Criteria:** At least 3 technical debt areas identified with reduction proposals
- **Estimated Duration:** 3 hours
- **Skippable:** Yes
