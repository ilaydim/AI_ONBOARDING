# Frontend — Technologies, Links & Standards

## Internal Resources
- **Confluence**: Frontend space — component decisions, performance reports
- **Figma**: `TechNova Design System` file (ask manager for access)
- **Linear**: `FRONTEND` project for all tickets
- **GitHub**: `technova/frontend-monorepo`
- **Chromatic**: Visual regression testing for UI components

## Tech Documentation

### React & TypeScript
- React 18 with concurrent features
- Strict TypeScript — enable `strictNullChecks`, `noImplicitAny`
- Functional components only, no class components
- Custom hooks for shared logic (prefix with `use`)

### Zustand (State Management)
- One store per feature domain
- No global "god store"
- Selectors to avoid unnecessary re-renders

### React Query (Server State)
- All API calls via React Query hooks
- Stale time: 5 minutes for most data
- Optimistic updates for mutations

### Tailwind CSS
- Utility-first, avoid custom CSS unless necessary
- Extend theme in `tailwind.config.ts`, don't override defaults
- `cn()` utility for conditional class merging

### Testing
```bash
# Unit tests
npx vitest

# E2E tests
npx playwright test

# Visual regression
npx chromatic --project-token=<token>
```

## Code Standards
- ESLint + Prettier enforced in CI
- Import order: external → internal → relative
- No `console.log` in production code
- Barrel exports (`index.ts`) for package public API

## Performance Checklist
- [ ] Images use `next/image` or lazy loading
- [ ] Large lists virtualized (react-virtual)
- [ ] Bundle analyzed with `vite-bundle-visualizer`
- [ ] No layout shift (CLS) from dynamic content

## Key Contacts
- **Senior FE Engineer**: Architecture decisions, design system ownership
- **Product Designer**: Figma files, UX decisions
- **#frontend-dev** Slack: daily technical chat
- **#design-frontend** Slack: design collaboration
