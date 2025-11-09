# Skill: React JS Project Blueprint

Purpose: Build and run modern React apps consistently using Vite.

When to use
- Component-based apps with JSX/ESM and multiple files → use a bundler (Vite).
- One-page demos without imports → consider CDN UMD + `text/babel` instead.

Vite React checklist
1. Root `index.html` (not under `src/`) with:
   - `<div id="root"></div>`
   - `<script type="module" src="/src/index.jsx"></script>`
   - Link styles via `<link rel="stylesheet" href="/src/styles.css" />` or import CSS in JS.
2. `src/index.jsx` mounts the app with React 18:
   - `import React from 'react'`
   - `import ReactDOM from 'react-dom/client'`
   - `import App from './App'`
   - `ReactDOM.createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>)`
3. `src/App.jsx` exports the root component. Use `.jsx` for any file that contains JSX unless you add `@vitejs/plugin-react` or a custom esbuild loader to treat `.js` as JSX.
4. `package.json` with scripts:
   - `dev: vite`, `build: vite build`, `preview: vite preview --port 5173`
   - deps: `react`, `react-dom`; devDeps: `vite`.
5. Add basic `styles.css` and import it (index.html or index.jsx).
6. Provide README with install/run/build instructions.
7. Add `.gitignore` entries for `node_modules/` and `dist/`.
8. Respect no‑go rules (e.g., do not generate SVGs; use placeholders or TODOs).

Run & build
- Install: `npm install`
- Dev server: `npm run dev` (open the printed URL)
- Production build: `npm run build`
- Preview build: `npm run preview`

Common pitfalls to avoid
- Placing `index.html` inside `src/` for Vite projects (should be at repo root).
- Using `<script src="app.js">` in `index.html` instead of a module script to `/src/index.js`.
- Writing JSX in `.js` files without the React plugin leads to esbuild errors like "The JSX syntax extension is not currently enabled". Use `.jsx` file extensions or install `@vitejs/plugin-react`.
- Forgetting `package.json` scripts and dependencies.
- Mixing absolute filesystem paths instead of workspace‑relative paths.
- Omitting a clear README with run/build steps.

Lessons learned (from prior runs)
- Missing `package.json` prevented install/run.
- `index.html` was put under `src/` and referenced `app.js`; switched to root `index.html` with a module script to `/src/index.jsx`.
- JSX was authored in `.js` files causing esbuild JSX loader errors; renamed to `.jsx` to resolve without extra plugins.
- Added Vite scripts and dependency declarations for React 18.
