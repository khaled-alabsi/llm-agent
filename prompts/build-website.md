# Build Personal Website - Agent Task

## Objective
Create a modern, responsive personal portfolio website using React and Tailwind CSS.

## Requirements

### Technical Stack
- React 18+
- Tailwind CSS for styling
- Vite as build tool
- Modern ES6+ JavaScript
- Responsive design (mobile-first)

### Features to Implement

#### 1. Navigation
- Sticky navigation bar
- Smooth scroll to sections
- Mobile hamburger menu
- Active section highlighting

#### 2. Hero Section
- Full-screen hero with gradient background
- Name and title/tagline
- Call-to-action button
- Subtle animations on load

#### 3. About Section
- Personal introduction (2-3 paragraphs)
- Professional background
- Current work/interests
- Optional: profile image with hover effect

#### 4. Skills Section
- Grid layout of technical skills
- Categorized skills (Frontend, Backend, Tools, etc.)
- Visual indicators (icons or badges)
- Hover effects

#### 5. Portfolio/Projects Section
- Grid of project cards (minimum 3-6 projects)
- Each project card includes:
  - Project image/screenshot
  - Title and description
  - Technologies used (tags)
  - Links to live demo and GitHub
- Hover animations

#### 6. Contact Section
- Functional contact form with:
  - Name field
  - Email field (with validation)
  - Message textarea
  - Submit button
- Form validation
- Social media links (GitHub, LinkedIn, Twitter, etc.)
- Email address display

#### 7. Footer
- Copyright information
- Social links
- Back to top button

### Design Requirements
- **Modern and Clean**: Minimalist design with focus on content
- **Responsive**: Perfect on mobile, tablet, and desktop
- **Accessible**: ARIA labels, semantic HTML, keyboard navigation
- **Dark Mode**: Toggle between light and dark themes
- **Animations**: Subtle, smooth transitions (scroll animations, hover effects)
- **Performance**: Fast loading, optimized images, lazy loading

### Code Quality
- Clean, well-documented code
- Reusable components
- Proper file organization
- No hardcoded data (use constants/config files)
- Error handling
- PropTypes or TypeScript for type checking

## Deliverables

### File Structure
```
output/personal-website/
├── public/
│   ├── index.html
│   └── assets/
│       └── images/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Hero.jsx
│   │   ├── About.jsx
│   │   ├── Skills.jsx
│   │   ├── Portfolio.jsx
│   │   ├── Contact.jsx
│   │   └── Footer.jsx
│   ├── data/
│   │   └── constants.js
│   ├── styles/
│   │   └── index.css
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```

### Documentation
- README.md with:
  - Project description
  - Setup instructions
  - Available scripts
  - Technologies used
  - Features list
  - Customization guide

### Package.json Scripts
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## Customization Points
The website should be easily customizable by changing values in `src/data/constants.js`:
- Personal information (name, title, bio)
- Skills list
- Projects data
- Social media links
- Contact information
- Color scheme

## Example Constants File
```javascript
export const personalInfo = {
  name: "John Doe",
  title: "Full-Stack Developer",
  bio: "Passionate developer with expertise in...",
  email: "john@example.com",
  location: "San Francisco, CA",
};

export const skills = {
  frontend: ["React", "JavaScript", "Tailwind CSS", "HTML5", "CSS3"],
  backend: ["Node.js", "Python", "PostgreSQL", "MongoDB"],
  tools: ["Git", "Docker", "VS Code", "Figma"],
};

export const projects = [
  {
    id: 1,
    title: "Project Name",
    description: "Brief description of the project",
    image: "/assets/project1.jpg",
    technologies: ["React", "Tailwind", "Firebase"],
    links: {
      demo: "https://demo.com",
      github: "https://github.com/user/project",
    },
  },
  // More projects...
];

export const socialLinks = {
  github: "https://github.com/username",
  linkedin: "https://linkedin.com/in/username",
  twitter: "https://twitter.com/username",
};
```

## Success Criteria
- [ ] All sections implemented and functional
- [ ] Fully responsive (tested on mobile, tablet, desktop)
- [ ] Dark mode working correctly
- [ ] Contact form validates input
- [ ] Smooth scroll navigation works
- [ ] No console errors
- [ ] Code follows best practices
- [ ] README is complete and clear
- [ ] Project builds successfully
- [ ] All links are functional
- [ ] Images load properly
- [ ] Accessibility score > 90 (Lighthouse)
- [ ] Performance score > 90 (Lighthouse)

## Notes
- Use placeholder images if real images not provided
- Use Lorem Ipsum for example project descriptions
- Provide example data in constants file
- Include comments explaining key parts of code
- Follow the coding standards defined in context/guidelines/
- Adhere to all rules in context/no-goes.md
