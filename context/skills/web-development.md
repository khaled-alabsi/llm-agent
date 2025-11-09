# Web Development Skills

## HTML5 & Semantic Markup

### Semantic Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Page description">
  <title>Page Title</title>
</head>
<body>
  <header>
    <nav aria-label="Main navigation">
      <!-- Navigation -->
    </nav>
  </header>

  <main>
    <article>
      <h1>Main Heading</h1>
      <section>
        <!-- Content -->
      </section>
    </article>
  </main>

  <aside>
    <!-- Sidebar content -->
  </aside>

  <footer>
    <!-- Footer content -->
  </footer>
</body>
</html>
```

### Accessibility Features
- Use semantic HTML elements
- Provide alt text for images
- Use ARIA labels where needed
- Ensure keyboard navigation
- Maintain proper heading hierarchy
- Include skip links for navigation

## Modern CSS

### Flexbox Layouts
```css
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.flex-column {
  display: flex;
  flex-direction: column;
}

.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### Grid Layouts
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.dashboard-grid {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 250px 1fr 1fr;
}
```

### Responsive Design
```css
/* Mobile first approach */
.container {
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### CSS Variables
```css
:root {
  --primary-color: #3b82f6;
  --secondary-color: #8b5cf6;
  --text-color: #1f2937;
  --bg-color: #ffffff;
  --spacing-unit: 0.25rem;
}

.dark-mode {
  --text-color: #f9fafb;
  --bg-color: #1f2937;
}

.button {
  background-color: var(--primary-color);
  color: var(--bg-color);
  padding: calc(var(--spacing-unit) * 3);
}
```

## Tailwind CSS Expertise

### Utility-First Approach
```jsx
// Layout
<div className="container mx-auto px-4 py-8">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {/* Grid items */}
  </div>
</div>

// Responsive Design
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>

// Dark Mode
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Dark mode support
</div>

// Hover States
<button className="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 transition-colors">
  Click me
</button>
```

### Custom Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6',
      },
      spacing: {
        '128': '32rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};
```

## JavaScript/ES6+

### Modern Syntax
```javascript
// Destructuring
const { name, age } = user;
const [first, ...rest] = array;

// Spread operator
const newObj = { ...oldObj, updated: true };
const newArr = [...arr1, ...arr2];

// Template literals
const message = `Hello, ${name}!`;

// Arrow functions
const multiply = (a, b) => a * b;

// Async/await
const fetchData = async () => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
};

// Optional chaining
const value = obj?.nested?.property;

// Nullish coalescing
const name = user.name ?? 'Guest';
```

### Array Methods
```javascript
// map - Transform array
const doubled = numbers.map(n => n * 2);

// filter - Filter array
const adults = users.filter(user => user.age >= 18);

// reduce - Reduce to single value
const sum = numbers.reduce((acc, n) => acc + n, 0);

// find - Find first match
const user = users.find(u => u.id === 5);

// some - Test if any match
const hasAdmin = users.some(u => u.role === 'admin');

// every - Test if all match
const allActive = users.every(u => u.active);
```

## API Integration

### Fetch API
```javascript
// GET request
const getData = async () => {
  try {
    const response = await fetch('https://api.example.com/data', {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
};

// POST request
const postData = async (data) => {
  const response = await fetch('https://api.example.com/data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return await response.json();
};
```

## Browser APIs

### Local Storage
```javascript
// Save data
localStorage.setItem('user', JSON.stringify(userData));

// Retrieve data
const user = JSON.parse(localStorage.getItem('user'));

// Remove data
localStorage.removeItem('user');

// Clear all
localStorage.clear();
```

### Intersection Observer (Lazy Loading)
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.src = entry.target.dataset.src;
      observer.unobserve(entry.target);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => {
  observer.observe(img);
});
```

## Progressive Web Apps (PWA)

### Service Worker Basics
```javascript
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(registration => console.log('SW registered'))
    .catch(error => console.error('SW registration failed', error));
}

// sw.js - Basic caching
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('v1').then((cache) => {
      return cache.addAll([
        '/',
        '/styles.css',
        '/script.js',
      ]);
    })
  );
});
```

### Manifest File
```json
{
  "name": "My PWA",
  "short_name": "PWA",
  "description": "A progressive web app",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## Build Tools & Optimization

### Webpack Basics
```javascript
// webpack.config.js
module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
};
```

### Performance Optimization
- Minimize and compress assets
- Use lazy loading for images
- Implement code splitting
- Enable gzip compression
- Use CDN for static assets
- Optimize images (WebP, AVIF)
- Implement caching strategies
- Remove unused CSS/JS
