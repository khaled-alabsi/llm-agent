# Coding Standards and Best Practices

## General Principles

### Code Organization
- One component per file
- Group related functionality
- Use clear, descriptive names
- Keep files under 300 lines

### Naming Conventions

**JavaScript/TypeScript:**
- `camelCase` for variables and functions
- `PascalCase` for components and classes
- `UPPER_SNAKE_CASE` for constants
- Prefix booleans with `is`, `has`, `should`

**Files:**
- `kebab-case.js` for utilities
- `PascalCase.jsx` for React components
- `index.js` for barrel exports

### Comments and Documentation

```javascript
/**
 * Brief description of what the function does
 *
 * @param {string} name - Parameter description
 * @returns {Object} - Return value description
 */
function greetUser(name) {
  return { message: `Hello, ${name}!` };
}
```

## React/JavaScript Standards

### Component Structure
```jsx
// 1. Imports
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

// 2. Component
const MyComponent = ({ title, onAction }) => {
  // 3. State
  const [data, setData] = useState(null);

  // 4. Effects
  useEffect(() => {
    // Effect logic
  }, []);

  // 5. Handlers
  const handleClick = () => {
    onAction();
  };

  // 6. Render
  return (
    <div className="my-component">
      <h1>{title}</h1>
      <button onClick={handleClick}>Action</button>
    </div>
  );
};

// 7. PropTypes
MyComponent.propTypes = {
  title: PropTypes.string.isRequired,
  onAction: PropTypes.func.isRequired,
};

export default MyComponent;
```

### Hooks Best Practices
- Use hooks at the top level only
- Name custom hooks with `use` prefix
- Keep hooks focused and single-purpose
- Extract complex logic to custom hooks

### State Management
- Keep state as local as possible
- Lift state only when necessary
- Use Context for global state
- Consider useReducer for complex state

## CSS/Tailwind Standards

### Tailwind Best Practices
```jsx
// ✅ Good: Organized classes
<div className="
  flex items-center justify-between
  p-4 m-2
  bg-white dark:bg-gray-800
  rounded-lg shadow-md
  hover:shadow-lg transition-shadow
">
  Content
</div>

// ❌ Avoid: Unorganized long strings
<div className="flex items-center p-4 bg-white rounded-lg shadow-md m-2 justify-between dark:bg-gray-800 hover:shadow-lg transition-shadow">
  Content
</div>
```

### Class Organization Order
1. Layout (flex, grid, display)
2. Spacing (margin, padding)
3. Sizing (width, height)
4. Typography
5. Visual (colors, borders, shadows)
6. States (hover, focus, dark mode)
7. Animations

## Error Handling

### Always Handle Errors
```javascript
// API Calls
const fetchData = async () => {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch data:', error);
    // Handle error appropriately
    throw error;
  }
};

// Event Handlers
const handleSubmit = (e) => {
  e.preventDefault();
  try {
    // Process form
  } catch (error) {
    console.error('Form submission error:', error);
    // Show user-friendly error message
  }
};
```

## Performance

### Optimization Techniques
- Memoize expensive calculations with `useMemo`
- Memoize callback functions with `useCallback`
- Lazy load components with `React.lazy`
- Debounce user input handlers
- Use image optimization (Next.js Image component)
- Code split at route level

### Example
```javascript
import { useMemo, useCallback } from 'react';

const ExpensiveComponent = ({ items, onItemClick }) => {
  // Memoize expensive computation
  const processedItems = useMemo(() => {
    return items.map(item => ({
      ...item,
      processed: expensiveOperation(item)
    }));
  }, [items]);

  // Memoize callback
  const handleClick = useCallback((id) => {
    onItemClick(id);
  }, [onItemClick]);

  return (
    <ul>
      {processedItems.map(item => (
        <li key={item.id} onClick={() => handleClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
};
```

## Accessibility

### ARIA and Semantic HTML
```jsx
// ✅ Good: Semantic and accessible
<nav aria-label="Main navigation">
  <button
    aria-label="Open menu"
    aria-expanded={isOpen}
    onClick={toggleMenu}
  >
    Menu
  </button>
</nav>

// ✅ Good: Form accessibility
<form>
  <label htmlFor="email">Email Address</label>
  <input
    id="email"
    type="email"
    aria-required="true"
    aria-describedby="email-help"
  />
  <p id="email-help">We'll never share your email</p>
</form>
```

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Provide visible focus indicators
- Implement skip links for navigation
- Ensure logical tab order

## Testing Considerations

### Testable Code
```javascript
// ✅ Good: Testable function
export const calculateTotal = (items) => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

// ✅ Good: Testable component
export const PriceDisplay = ({ items }) => {
  const total = calculateTotal(items);
  return <div>Total: ${total}</div>;
};
```

## File Structure
```
project/
├── src/
│   ├── components/
│   │   ├── common/          # Reusable components
│   │   ├── layout/          # Layout components
│   │   └── features/        # Feature-specific components
│   ├── hooks/               # Custom hooks
│   ├── utils/               # Utility functions
│   ├── styles/              # Global styles
│   ├── constants/           # Constants and config
│   └── types/               # TypeScript types
├── public/                  # Static assets
└── tests/                   # Test files
```

## Git Commit Messages

Format: `type(scope): message`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example:
```
feat(auth): add login component
fix(navbar): correct mobile menu toggle
docs(readme): update installation steps
```
