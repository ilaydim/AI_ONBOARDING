# Frontend Team

The team responsible for all user-facing interfaces across TechNova products.

## Team Structure
- 8 frontend engineers (2 junior, 4 mid, 2 senior)
- 1 Engineering Manager

## Tech Stack
- **Framework**: React 18 (TypeScript)
- **State Management**: Zustand (local), React Query (server state)
- **Styling**: Tailwind CSS + shadcn/ui component library
- **Build**: Vite
- **Testing**: Vitest + React Testing Library + Playwright (E2E)

## Responsibilities
- Web application development (TechNova Suite dashboard)
- Design system maintenance
- Accessibility (WCAG 2.1 AA compliance)
- Performance optimization (Core Web Vitals)
- Cross-browser compatibility

## Application Structure
```
apps/
  web/          # Main TechNova Suite web app
  admin/        # Internal admin portal
packages/
  ui/           # Shared component library
  utils/        # Shared utilities
  types/        # Shared TypeScript types
```

## Key Standards
- TypeScript strict mode — no `any` without justification
- Components must be accessible: ARIA labels, keyboard navigation
- Unit tests required for business logic
- E2E tests for critical user flows (login, checkout, reporting)
- Lighthouse score minimum: Performance 85, Accessibility 95

## Design System
- Figma is the source of truth for design
- Components built in `packages/ui` before used in apps
- Design tokens define colors, spacing, typography
- Dark mode supported via CSS custom properties

## Team Norms
- Design review required before implementing new UI
- PR includes screenshot/video for visual changes
- `#frontend-dev` Slack channel for technical discussions
- Weekly design sync with product designers (Wednesdays)
