<!--
Sync Impact Report:
Version: Initial → 1.0.0
Modified principles: N/A (initial constitution)
Added sections: All 10 core sections (Code Quality, Content Standards, Testing, Deployment, Security, Architecture, Collaboration, NFRs, Documentation, Quality Gates)
Removed sections: None
Templates requiring updates:
  ✅ .specify/templates/plan-template.md - Constitution Check section will reference these principles
  ✅ .specify/templates/spec-template.md - Requirements sections align with content standards
  ✅ .specify/templates/tasks-template.md - Task categorization reflects quality gates
Follow-up TODOs: None
-->

# AI/Spec-Driven Book Creation Constitution

## Core Principles

### I. Documentation-First Development

**Rule**: All content MUST begin with a specification, architectural plan, and task breakdown before any implementation.

**Requirements**:
- MUST use Spec-Driven Development workflow: spec → plan → tasks → implement
- MUST create Prompt History Records (PHRs) for all significant changes
- MUST document Architectural Decision Records (ADRs) for significant decisions
- Content changes MUST follow the red-green-refactor cycle where applicable

**Rationale**: AI-assisted book creation requires explicit intent capture and iterative refinement. Specifications ensure content goals are clear before authoring begins, preventing scope drift and maintaining consistency across chapters.

### II. Markdown Quality Standards

**Rule**: All documentation MUST follow strict markdown formatting, structure, and consistency standards.

**Requirements**:
- MUST use CommonMark-compliant markdown syntax
- MUST maintain consistent heading hierarchy (no skipped levels)
- MUST use semantic headings (H1 for title, H2 for major sections, etc.)
- MUST use fenced code blocks with language identifiers
- MUST wrap lines at 100 characters for readability (except URLs/tables)
- MUST use reference-style links for repeated URLs
- SHOULD use definition lists for glossaries
- MUST NOT use HTML except where markdown is insufficient

**Rationale**: Docusaurus and GitHub Pages render markdown; inconsistent formatting breaks builds and degrades user experience.

### III. Content Organization & Modularity

**Rule**: Content MUST be organized in a clear, modular file structure with consistent naming conventions.

**Requirements**:
- MUST use kebab-case for all file and directory names (e.g., `getting-started.md`)
- MUST organize by topic/chapter in logical hierarchy under `docs/`
- MUST use `_category_.json` files to control sidebar ordering in Docusaurus
- MUST keep individual markdown files focused and under 500 lines
- MUST use `index.md` as entry point for each major section
- MUST separate reusable content into partials under `docs/_partials/`
- MUST NOT duplicate content; use imports or cross-references instead

**Rationale**: Modular organization enables parallel authoring, easier reviews, and better maintainability. It also supports Docusaurus's file-based routing and sidebar generation.

### IV. Version Control & Git Workflow

**Rule**: All changes MUST follow a disciplined git workflow with meaningful commits and PR reviews.

**Requirements**:
- MUST use conventional commit messages: `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  - Example: `docs(chapter-2): add section on neural networks`
- MUST create feature branches from `main` using format: `###-feature-name`
- MUST submit Pull Requests for all changes to `main`
- MUST require at least one review approval before merge
- MUST squash merge commits to keep history clean
- MUST include PR descriptions with: summary, changes, testing done
- MUST NOT commit directly to `main` branch
- MUST NOT force push to shared branches without team agreement

**Rationale**: Structured git workflow enables traceability, rollback capability, and collaborative review of technical content.

### V. Accessibility (WCAG 2.1 AA Compliance)

**Rule**: All content MUST meet WCAG 2.1 Level AA accessibility standards.

**Requirements**:
- MUST provide alt text for all images (descriptive, not decorative)
- MUST use semantic HTML where markdown is insufficient
- MUST maintain sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- MUST structure headings logically without skipping levels
- MUST provide text alternatives for video/audio content
- MUST ensure interactive elements are keyboard-navigable
- MUST use ARIA labels only when semantic HTML is insufficient
- SHOULD test with screen readers (NVDA, JAWS, VoiceOver)

**Rationale**: Technical books serve diverse audiences, including developers with visual, motor, or cognitive disabilities. Accessibility is non-negotiable.

### VI. Code Examples: Tested & Runnable

**Rule**: All code examples MUST be syntactically valid, tested, and executable.

**Requirements**:
- MUST include language identifier in fenced code blocks
- MUST validate syntax before committing (via linter or build check)
- SHOULD include complete, runnable examples where practical
- MUST annotate code with inline comments explaining non-obvious logic
- MUST use realistic, meaningful variable names (no `foo`, `bar`)
- MUST include expected output or behavior where applicable
- SHOULD provide links to full working examples in repository
- MUST NOT include insecure or deprecated code patterns

**Rationale**: Readers copy code examples. Broken or insecure examples damage credibility and harm learning outcomes.

### VII. Media Guidelines: Images, Diagrams, Videos

**Rule**: All media MUST be optimized, properly attributed, and accessible.

**Requirements**:
- MUST use web-optimized formats:
  - Images: WebP (preferred), PNG for transparency, JPEG for photos
  - Diagrams: SVG (preferred) or optimized PNG
  - Videos: MP4 (H.264) with max 720p resolution
- MUST compress images to keep file size < 200KB where possible
- MUST store media in `static/img/` directory
- MUST use descriptive filenames: `neural-network-architecture.svg` (not `img1.svg`)
- MUST provide alt text and captions for all media
- MUST include attribution/licensing for third-party media
- SHOULD use Mermaid diagrams for simple flowcharts/diagrams
- MUST NOT embed large videos; link to YouTube/external hosting instead

**Rationale**: Large media files slow page loads and bloat the repository. Proper attribution respects copyright and builds trust.

### VIII. Cross-Referencing & Internal Linking

**Rule**: Internal links MUST use relative paths and follow consistent conventions.

**Requirements**:
- MUST use relative links for internal content: `[link](../chapter-2/section.md)`
- MUST use absolute URLs for external links
- MUST verify all links before merging (automated check in CI)
- MUST use descriptive link text (not "click here")
- SHOULD use anchor links for same-page navigation
- MUST update links when moving/renaming files
- MUST NOT use hardcoded domain names for internal links

**Rationale**: Broken links frustrate readers and damage credibility. Relative links ensure portability across environments (local, staging, production).

## Content Standards

### IX. Writing Style Guide

**Tone & Voice**:
- MUST use clear, concise, technical language
- MUST write in active voice where possible
- SHOULD use second person ("you") to address readers
- MUST define acronyms on first use
- MUST maintain consistent terminology throughout the book

**Technical Depth**:
- MUST balance theory with practical application
- MUST provide context before diving into implementation
- SHOULD include "Why this matters" sections for complex topics
- MUST cite sources for claims, statistics, and research

**Rationale**: Consistency in voice and depth ensures a professional, cohesive reading experience.

## Testing & Validation

### X. Content Review Process

**Rule**: All content MUST be reviewed for technical accuracy, grammar, and readability before merge.

**Requirements**:
- MUST pass automated grammar/spell check (e.g., Vale, LanguageTool)
- MUST be reviewed by at least one technical subject-matter expert
- SHOULD be reviewed by a technical writer or editor for clarity
- MUST address all reviewer comments or provide justification for rejection
- MUST include self-review checklist in PR template

**Rationale**: Technical errors undermine trust; poor writing hinders comprehension. Peer review catches both.

### XI. Build Validation

**Rule**: All changes MUST build successfully in Docusaurus with no errors before merge.

**Requirements**:
- MUST run `npm run build` locally before creating PR
- MUST pass automated build check in GitHub Actions CI
- MUST resolve all markdown parsing errors
- MUST NOT introduce broken internal links (checked by CI)
- MUST NOT exceed bundle size budget (defined in config)

**Rationale**: Broken builds block deployment. Catching build errors pre-merge maintains continuous deployability.

### XII. Link Validation

**Rule**: All internal and external links MUST be valid and reachable.

**Requirements**:
- MUST run link checker in CI (e.g., `markdown-link-check`)
- MUST fix or remove broken links before merge
- SHOULD check external links monthly for link rot
- MUST use Wayback Machine archives for historical references at risk of disappearing

**Rationale**: Broken links damage user experience and credibility.

### XIII. Preview/Staging Requirements

**Rule**: All changes MUST be previewed in a staging environment before production deployment.

**Requirements**:
- MUST deploy PR previews automatically via GitHub Actions (e.g., Netlify Deploy Previews)
- MUST review preview deployment before approving PR
- MUST verify responsive layout on mobile, tablet, desktop
- SHOULD test with multiple browsers (Chrome, Firefox, Safari, Edge)

**Rationale**: Visual review catches layout issues, broken styles, and responsive design problems that automated tests miss.

## Deployment & Operations

### XIV. GitHub Actions CI/CD Pipeline

**Rule**: All deployments MUST be automated via GitHub Actions with quality gates.

**Requirements**:
- MUST define CI workflow in `.github/workflows/deploy.yml`
- MUST run on every push to `main` and on PRs
- MUST include these steps:
  1. Install dependencies (`npm ci`)
  2. Run linters (markdown, code)
  3. Run build (`npm run build`)
  4. Run link checker
  5. Run Lighthouse CI (performance, accessibility)
  6. Deploy to GitHub Pages (on `main` only)
- MUST fail deployment if any quality gate fails
- MUST notify team on deployment failure (Slack, email, or GitHub)

**Rationale**: Automation ensures consistency, catches regressions, and enables rapid iteration.

### XV. Deployment Triggers

**Rule**: Deployments MUST occur automatically on merge to `main` and MUST be idempotent.

**Requirements**:
- MUST auto-deploy on merge to `main` (no manual intervention)
- MUST deploy only if CI passes all quality gates
- SHOULD support manual deployment via workflow dispatch
- MUST NOT deploy on PR branches (use preview deployments instead)

**Rationale**: Auto-deployment reduces toil and ensures published content matches the `main` branch.

### XVI. Rollback Procedures

**Rule**: Deployments MUST be reversible via git revert or re-deployment.

**Requirements**:
- MUST support rollback via git revert + force redeploy
- MUST document rollback procedure in `docs/operations/rollback.md`
- MUST maintain previous deployment artifacts for quick restore
- SHOULD monitor production for errors post-deployment

**Rationale**: Bugs happen. Fast rollback minimizes reader impact.

### XVII. Custom Domain & SSL/TLS

**Rule**: Production deployments MUST use HTTPS with a custom domain (if applicable).

**Requirements**:
- MUST configure custom domain in GitHub Pages settings
- MUST enforce HTTPS (HTTP redirects to HTTPS)
- MUST use valid SSL/TLS certificate (GitHub provides free certs)
- MUST configure DNS correctly (CNAME or A records)

**Rationale**: HTTPS is a web standard. Custom domains improve branding and SEO.

## Security & Privacy

### XVIII. No Secrets in Repository

**Rule**: API keys, tokens, and credentials MUST NEVER be committed to the repository.

**Requirements**:
- MUST use environment variables for secrets
- MUST use GitHub Secrets for CI/CD credentials
- MUST add sensitive patterns to `.gitignore`
- MUST scan commits for leaked secrets (e.g., `git-secrets`, `trufflehog`)
- MUST rotate credentials immediately if accidentally committed

**Rationale**: Public repositories expose secrets to the world. Credential leaks enable unauthorized access.

### XIX. Content Licensing

**Rule**: All original content MUST be licensed explicitly; third-party content MUST comply with attribution requirements.

**Requirements**:
- MUST include `LICENSE` file at repository root (e.g., MIT, CC-BY-4.0)
- MUST state license in README and site footer
- MUST attribute third-party content per license terms
- MUST NOT use copyrighted material without permission
- SHOULD prefer permissively licensed content (MIT, Apache 2.0, CC-BY)

**Rationale**: Clear licensing protects authors and users. Proper attribution respects creators' rights.

### XX. User Privacy & Analytics

**Rule**: If analytics are used, MUST comply with privacy laws (GDPR, CCPA) and disclose tracking.

**Requirements**:
- SHOULD use privacy-respecting analytics (e.g., Plausible, Fathom) over Google Analytics
- MUST disclose tracking in privacy policy
- MUST provide opt-out mechanism if using invasive tracking
- MUST NOT collect personally identifiable information without consent
- MUST anonymize IP addresses where possible

**Rationale**: Readers value privacy. Compliance with GDPR/CCPA is legally required in many jurisdictions.

### XXI. Dependency Security

**Rule**: All npm dependencies MUST be kept up-to-date and scanned for vulnerabilities.

**Requirements**:
- MUST enable Dependabot for automated dependency updates
- MUST review and merge security updates within 7 days
- MUST run `npm audit` locally before committing
- MUST resolve high/critical vulnerabilities before merge
- SHOULD pin dependency versions in `package-lock.json`

**Rationale**: Vulnerable dependencies expose sites to exploits. Regular updates minimize attack surface.

## Architecture Decisions

### XXII. Docusaurus Configuration Standards

**Rule**: Docusaurus configuration MUST be explicit, version-controlled, and documented.

**Requirements**:
- MUST define all configuration in `docusaurus.config.js`
- MUST use Docusaurus v3.x (or latest stable)
- MUST configure sidebar auto-generation or explicit `sidebars.js`
- MUST configure search (Algolia DocSearch or local search plugin)
- MUST enable syntax highlighting for all supported languages
- MUST configure navbar, footer, and metadata
- MUST document custom configuration in `docs/operations/configuration.md`

**Rationale**: Explicit configuration prevents surprises and ensures reproducibility across environments.

### XXIII. Plugin Usage Guidelines

**Rule**: Only approved Docusaurus plugins MAY be used; new plugins MUST be justified in an ADR.

**Approved Plugins**:
- `@docusaurus/preset-classic` (core preset)
- `@docusaurus/plugin-content-docs` (documentation)
- `@docusaurus/plugin-content-blog` (if blog is needed)
- `@docusaurus/plugin-sitemap` (SEO)
- Mermaid diagram plugin (for embedded diagrams)
- Algolia DocSearch or local search plugin

**Requirements**:
- MUST justify new plugins in ADR (overhead, maintenance, security)
- MUST NOT use unmaintained or insecure plugins
- SHOULD prefer official plugins over third-party

**Rationale**: Each plugin adds complexity and maintenance burden. Limiting plugins keeps builds fast and secure.

### XXIV. Theme Customization Boundaries

**Rule**: Theme customizations MUST be minimal and documented; prefer configuration over code.

**Requirements**:
- MUST use Docusaurus's built-in theming system
- SHOULD use CSS custom properties (variables) for branding
- MAY override components via swizzling (document in ADR)
- MUST NOT modify node_modules directly
- MUST keep custom CSS under 10KB where possible

**Rationale**: Excessive customization makes upgrades difficult. Docusaurus's theming system provides sufficient flexibility.

### XXV. Performance Budgets

**Rule**: All pages MUST meet performance budgets; regressions MUST be justified.

**Performance Targets**:
- Page load time (3G): < 2 seconds (Time to Interactive)
- First Contentful Paint: < 1 second
- Lighthouse Performance score: > 90
- Total bundle size: < 500KB (JS + CSS)

**Requirements**:
- MUST run Lighthouse CI on every PR
- MUST block merge if performance regresses by > 10%
- MUST document justified regressions in PR description
- SHOULD lazy-load images and code examples

**Rationale**: Fast sites improve user experience and SEO. Performance budgets prevent bloat.

## Collaboration Workflow

### XXVI. Spec-Driven Approach

**Rule**: All features MUST follow the spec → plan → tasks → implement workflow.

**Requirements**:
- MUST create feature spec in `specs/<feature>/spec.md` before planning
- MUST create implementation plan in `specs/<feature>/plan.md` before tasking
- MUST generate tasks in `specs/<feature>/tasks.md` before implementing
- MUST link tasks to spec and plan for traceability
- MUST validate deliverables against spec acceptance criteria

**Rationale**: Spec-driven development ensures clarity, reduces rework, and enables AI-assisted workflows.

### XXVII. Prompt History Records (PHR)

**Rule**: All significant AI-assisted interactions MUST be recorded as PHRs.

**Requirements**:
- MUST create PHR after AI-assisted content creation, planning, or debugging
- MUST store PHRs under `history/prompts/<stage>/` (e.g., `history/prompts/constitution/`)
- MUST include: prompt, response, stage, feature context, date
- MUST NOT skip PHR creation for convenience

**Rationale**: PHRs provide traceability, enable learning from past interactions, and support auditing.

### XXVIII. Architectural Decision Records (ADR)

**Rule**: Architecturally significant decisions MUST be documented as ADRs when they meet the significance test.

**Significance Test** (ALL must be true):
- **Impact**: Does this have long-term consequences?
- **Alternatives**: Were multiple viable options considered?
- **Scope**: Is this cross-cutting or influential to system design?

**Requirements**:
- MUST suggest ADR when significance test passes
- MUST wait for user consent before creating ADR
- MUST store ADRs under `history/adr/`
- MUST use format: `NNNN-decision-title.md`
- MUST include: context, decision, consequences, alternatives, status

**Rationale**: ADRs capture the "why" behind decisions, preventing future confusion and enabling informed evolution.

### XXIX. Review & Approval Process

**Rule**: All PRs MUST be reviewed and approved before merge.

**Requirements**:
- MUST require at least 1 approval from a team member
- MUST address all review comments or provide justification
- MUST re-request review after addressing comments
- SHOULD use GitHub's "Request Changes" for blocking issues
- MUST NOT self-merge without second approval (unless solo project)

**Rationale**: Peer review catches errors, improves quality, and shares knowledge.

## Non-Functional Requirements

### XXX. Performance

**Rule**: All pages MUST load in under 2 seconds on 3G networks.

**Metrics**:
- Time to Interactive (TTI): < 2s on 3G
- First Contentful Paint (FCP): < 1s
- Largest Contentful Paint (LCP): < 2.5s

**Requirements**:
- MUST optimize images (WebP, lazy loading)
- MUST code-split JavaScript bundles
- MUST enable HTTP/2 and compression (gzip/brotli)
- MUST minimize render-blocking resources

**Rationale**: Many readers access content on mobile or slow connections. Fast sites improve engagement.

### XXXI. SEO

**Rule**: All pages MUST be optimized for search engines.

**Requirements**:
- MUST include `<title>`, `<meta description>`, and Open Graph tags
- MUST generate `sitemap.xml` automatically (Docusaurus plugin)
- MUST configure `robots.txt` to allow indexing
- MUST use semantic HTML and heading hierarchy
- SHOULD use structured data (JSON-LD) for rich snippets

**Rationale**: SEO increases discoverability and drives organic traffic.

### XXXII. Browser Support

**Rule**: All pages MUST work in modern evergreen browsers.

**Supported Browsers**:
- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)

**Requirements**:
- MUST test in all supported browsers before merge
- MUST NOT rely on vendor-specific features without fallbacks
- MAY use progressive enhancement for advanced features

**Rationale**: Modern browsers auto-update; supporting legacy browsers is unnecessary burden.

## Documentation Standards

### XXXIII. README Requirements

**Rule**: Each major section or book MUST include a README with onboarding information.

**Requirements**:
- MUST include in repository root and each major docs folder
- MUST contain: project overview, setup instructions, contribution guidelines
- MUST link to relevant documentation (spec, plan, architecture)
- MUST be kept up-to-date with each release

**Rationale**: READMEs are the first thing readers and contributors see. Clear onboarding reduces friction.

### XXXIV. Changelog Maintenance

**Rule**: All notable changes MUST be documented in `CHANGELOG.md` following Keep a Changelog format.

**Requirements**:
- MUST use Keep a Changelog format (https://keepachangelog.com/)
- MUST categorize changes: Added, Changed, Deprecated, Removed, Fixed, Security
- MUST update on every merge to `main`
- MUST include version numbers and release dates

**Rationale**: Changelogs help readers and contributors track evolution and find breaking changes.

### XXXV. API/Component Documentation

**Rule**: All reusable components and APIs MUST be documented inline and in dedicated docs.

**Requirements**:
- MUST use JSDoc or equivalent for code documentation
- MUST document parameters, return values, and examples
- MUST generate API docs automatically (e.g., TypeDoc, JSDoc)
- SHOULD include usage examples

**Rationale**: Undocumented code is unusable. Inline docs support IDE autocomplete.

### XXXVI. Troubleshooting Guides

**Rule**: Common errors and setup issues MUST be documented in troubleshooting guides.

**Requirements**:
- MUST maintain `docs/troubleshooting.md` with common issues
- SHOULD include FAQs for reader questions
- MUST update when new issues are discovered
- SHOULD link to GitHub Issues for known bugs

**Rationale**: Self-service troubleshooting reduces support burden and reader frustration.

## Quality Gates

### XXXVII. Link Validation

**Rule**: All internal and external links MUST be valid before merge.

**Requirements**:
- MUST run `markdown-link-check` in CI
- MUST fix broken links before merge
- SHOULD check external links monthly

**Rationale**: Broken links frustrate readers and damage credibility.

### XXXVIII. Code Example Syntax Validation

**Rule**: All code examples MUST be syntactically valid.

**Requirements**:
- MUST validate code blocks with language-specific linters
- MUST ensure code compiles/runs where applicable
- SHOULD include expected output

**Rationale**: Broken code examples undermine trust and waste reader time.

### XXXIX. Build Success Gate

**Rule**: Docusaurus build MUST succeed before merge.

**Requirements**:
- MUST run `npm run build` in CI
- MUST fail PR if build fails
- MUST resolve markdown parsing errors

**Rationale**: Broken builds block deployment and waste team time.

### XL. Lighthouse Quality Gates

**Rule**: All pages MUST meet Lighthouse thresholds before merge.

**Thresholds**:
- Performance: > 90
- Accessibility: > 95
- Best Practices: > 90
- SEO: > 90

**Requirements**:
- MUST run Lighthouse CI on every PR
- MUST block merge if scores regress by > 5 points
- MUST document justified regressions

**Rationale**: Lighthouse scores correlate with user experience, accessibility, and SEO performance.

## Governance

### Amendment Procedure

This constitution MAY be amended via the following process:

1. Proposal: Create a PR modifying `.specify/memory/constitution.md`
2. Justification: Include rationale in PR description
3. Review: Require approval from project maintainers
4. Version Bump: Increment version per semantic versioning rules:
   - MAJOR: Backward-incompatible changes (principle removal/redefinition)
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording, typo fixes
5. Synchronization: Update dependent templates (plan, spec, tasks)
6. Merge: Merge PR and communicate changes to team

### Compliance Review

- All PRs MUST verify compliance with this constitution
- Maintainers MUST enforce these principles in code reviews
- Complexity MUST be justified when principles are bent
- This constitution supersedes informal practices

### Runtime Guidance

For AI-assisted development workflows, refer to `CLAUDE.md` for runtime development guidance specific to Claude Code.

**Version**: 1.0.0 | **Ratified**: 2025-11-30 | **Last Amended**: 2025-11-30
