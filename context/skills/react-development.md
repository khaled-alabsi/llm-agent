# React Development Skills

## Core Competencies

### Component Development
- Functional components with hooks
- Props and state management
- Component composition
- Controlled vs uncontrolled components
- Higher-order components (HOCs)
- Render props pattern

### React Hooks Mastery

#### Essential Hooks
```javascript
// useState - State management
const [count, setCount] = useState(0);

// useEffect - Side effects
useEffect(() => {
  // Effect logic
  return () => {
    // Cleanup
  };
}, [dependencies]);

// useContext - Context consumption
const theme = useContext(ThemeContext);

// useRef - DOM access and persistent values
const inputRef = useRef(null);

// useMemo - Memoized values
const expensiveValue = useMemo(() => computeExpensive(a, b), [a, b]);

// useCallback - Memoized functions
const handleClick = useCallback(() => {
  doSomething(a);
}, [a]);

// useReducer - Complex state logic
const [state, dispatch] = useReducer(reducer, initialState);
```

#### Custom Hooks
```javascript
// Example: useLocalStorage
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

// Example: useFetch
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url);
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

## Modern Patterns

### Context API
```javascript
// Create context
const ThemeContext = createContext({
  theme: 'light',
  toggleTheme: () => {},
});

// Provider component
export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Consumer hook
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};
```

### Compound Components
```javascript
const Accordion = ({ children }) => {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <div className="accordion">
      {React.Children.map(children, (child, index) =>
        React.cloneElement(child, {
          isOpen: index === openIndex,
          onToggle: () => setOpenIndex(index === openIndex ? null : index),
        })
      )}
    </div>
  );
};

const AccordionItem = ({ title, children, isOpen, onToggle }) => (
  <div className="accordion-item">
    <button onClick={onToggle}>{title}</button>
    {isOpen && <div className="content">{children}</div>}
  </div>
);

Accordion.Item = AccordionItem;
```

### Error Boundaries
```javascript
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }

    return this.props.children;
  }
}
```

## Form Handling

### Controlled Forms
```javascript
const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });

  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user types
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await submitForm(formData);
      // Success handling
    } catch (error) {
      // Error handling
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
        aria-invalid={!!errors.name}
      />
      {errors.name && <span className="error">{errors.name}</span>}
      {/* More fields */}
    </form>
  );
};
```

## Animation and Transitions

### CSS Transitions
```javascript
const FadeIn = ({ children, duration = 300 }) => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    setShow(true);
  }, []);

  return (
    <div
      className={`transition-opacity duration-${duration} ${
        show ? 'opacity-100' : 'opacity-0'
      }`}
    >
      {children}
    </div>
  );
};
```

### Framer Motion (if using)
```javascript
import { motion } from 'framer-motion';

const AnimatedCard = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
  >
    Card content
  </motion.div>
);
```

## Performance Optimization

### Code Splitting
```javascript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Virtual Lists (for long lists)
```javascript
import { FixedSizeList } from 'react-window';

const VirtualList = ({ items }) => (
  <FixedSizeList
    height={600}
    itemCount={items.length}
    itemSize={50}
    width="100%"
  >
    {({ index, style }) => (
      <div style={style}>
        {items[index].name}
      </div>
    )}
  </FixedSizeList>
);
```

## Common Patterns

### Loading States
```javascript
const DataDisplay = () => {
  const { data, loading, error } = useFetch('/api/data');

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!data) return null;

  return <DataGrid data={data} />;
};
```

### Debouncing Input
```javascript
const SearchInput = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (query) {
        searchAPI(query).then(setResults);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
};
```
