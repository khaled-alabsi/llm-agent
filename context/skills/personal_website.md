# Skill: Personal Website Blueprint

Purpose: Provide a clear blueprint for generating a modern personal website with minimal tooling.

Core requirements
- Mobile-first, responsive layout.
- Clean, accessible design (sensible color contrast, semantic HTML).
- Easy to host statically (no server-side code required).
- Minimal dependencies; prefer CDN when using libraries.

Recommended structure
- Header with name, role, and simple navigation.
- Hero section with a short bio and portrait placeholder.
- Projects/Work section with cards (title, short description, tech tags, link buttons).
- About section with skills and background.
- Contact section with email link and social links.
- Footer with copyright and quick links.

Components
- Navbar/Header (sticky on top), Footer.
- Card component for projects.
- Tag/Pill component for quick tech labels.
- Responsive grid utilities for the Projects section.

Look & feel
- Modern, friendly typography and spacing.
- Light/dark color palette that works without JS (prefers-color-scheme is enough).
- Simple animation on hover/focus for interactivity.

Implementation guidance
- Use a single `index.html`, `styles.css`, and `app.js` (optional) for dynamic behavior like theme toggle.
- Keep images as placeholders or `TODO` notes if assets are not provided.
- Navigation should scroll to sections; use anchor links and `scroll-behavior: smooth` in CSS.
- Include a README with how to run a static server (Python or Node) and how to customize content.

Deliverables checklist
- index.html with semantic sections: header, main (hero, projects, about, contact), footer.
- styles.css with responsive grid and typography.
- app.js (optional) for small enhancements (e.g., theme toggle).
- README.md with instructions and content placeholders to edit.
