# Tasks — DevOps / Infrastructure

## Task: Learn the Company Architecture
- **ID:** devops-001
- **Level:** junior, mid, senior
- **Dependency:** None
- **Expected Output:** Explain the deployment pipeline end-to-end
- **Completion Criteria:** List every step from code push to production in order
- **Estimated Duration:** 1 hour
- **Skippable:** No

## Task: Set Up Local Environment
- **ID:** devops-002
- **Level:** junior, mid
- **Dependency:** devops-001
- **Expected Output:** kubectl and helm installed, cluster access established
- **Completion Criteria:** `kubectl get pods` command works successfully
- **Estimated Duration:** 2 hours
- **Skippable:** Yes

## Task: Review the CI/CD Pipeline
- **ID:** devops-003
- **Level:** junior, mid, senior
- **Dependency:** devops-001
- **Expected Output:** Review GitHub Actions workflows and add a new trigger
- **Completion Criteria:** Workflow change submitted via PR
- **Estimated Duration:** 2 hours
- **Skippable:** No
