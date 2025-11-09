# Personal Website Example Structure

## Project Overview
A modern, responsive personal portfolio website showcasing skills, projects, and contact information.

## Technology Stack
- React 18
- Tailwind CSS
- Vite (build tool)
- React Icons
- Framer Motion (animations)

## Page Sections

### 1. Hero Section
```jsx
<section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
  <div className="text-center text-white">
    <h1 className="text-5xl md:text-7xl font-bold mb-4">John Doe</h1>
    <p className="text-xl md:text-2xl mb-8">Full-Stack Developer</p>
    <button className="bg-white text-blue-600 px-8 py-3 rounded-full">
      View My Work
    </button>
  </div>
</section>
```

### 2. About Section
- Personal introduction
- Background story
- Current focus
- Photo (optional)

### 3. Skills Section
- Technical skills grid
- Skill level indicators
- Categories (Frontend, Backend, Tools)

### 4. Portfolio/Projects Section
- Project cards with images
- Project descriptions
- Technologies used
- Live demo + GitHub links

### 5. Contact Section
- Contact form (name, email, message)
- Social media links
- Email address
- Download resume button

## Design Principles
- Clean, modern design
- Smooth scrolling between sections
- Responsive for all devices
- Dark mode support
- Accessibility compliant
- Fast loading times

## Color Scheme Example
```javascript
const colors = {
  primary: '#3b82f6',      // Blue
  secondary: '#8b5cf6',    // Purple
  accent: '#10b981',       // Green
  dark: '#1f2937',         // Dark gray
  light: '#f9fafb',        // Light gray
};
```

## Component Structure
```
src/
├── components/
│   ├── Hero.jsx
│   ├── About.jsx
│   ├── Skills.jsx
│   ├── Portfolio.jsx
│   ├── Contact.jsx
│   ├── Navbar.jsx
│   └── Footer.jsx
├── App.jsx
└── main.jsx
```

## Example Project Card
```jsx
const ProjectCard = ({ title, description, image, tech, links }) => (
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
    <img src={image} alt={title} className="w-full h-48 object-cover" />
    <div className="p-6">
      <h3 className="text-2xl font-bold mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300 mb-4">{description}</p>
      <div className="flex flex-wrap gap-2 mb-4">
        {tech.map(t => (
          <span key={t} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
            {t}
          </span>
        ))}
      </div>
      <div className="flex gap-4">
        <a href={links.demo} className="text-blue-600 hover:underline">
          Live Demo
        </a>
        <a href={links.github} className="text-gray-600 hover:underline">
          GitHub
        </a>
      </div>
    </div>
  </div>
);
```
