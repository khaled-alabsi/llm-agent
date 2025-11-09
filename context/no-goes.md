# Agent Safety Rules and No-Goes

## Absolute Prohibitions

### Generation
- never generate svg or png, .. , just use placeholder text or add todos if needed

### Security
- **NO hardcoded credentials** - Never include API keys, passwords, or secrets in code
- **NO SQL injection vulnerabilities** - Always use parameterized queries
- **NO XSS vulnerabilities** - Always sanitize user input
- **NO insecure dependencies** - Avoid packages with known vulnerabilities
- **NO exposed sensitive data** - Never log or expose PII, tokens, or credentials

### Code Quality
- **NO code without error handling** - All operations must have try-catch or error handling
- **NO magic numbers** - Use named constants
- **NO duplicate code** - Follow DRY principle
- **NO commented-out code** - Remove unused code instead of commenting
- **NO console.log in production** - Use proper logging mechanisms

### File Operations
- **NO overwriting without backup** - Always check if file exists before overwriting
- **NO deleting without confirmation** - Require explicit confirmation for deletions
- **NO operations outside project directory** - Stay within ./output or designated paths
- **NO binary file modifications** - Only work with text files
- **NO large file creations** - Limit file size to configured max (10MB default)

### System Commands
- **NO rm -rf without safeguards** - Never delete recursively without confirmation
- **NO sudo/elevated permissions** - Don't require or use admin rights
- **NO network requests to unknown hosts** - Only use approved APIs
- **NO infinite loops** - Always have exit conditions
- **NO resource-intensive operations** - Be mindful of CPU/memory usage

### Best Practices Violations
- **NO skipping documentation** - Every function/component must have docs
- **NO ignoring accessibility** - Always include ARIA labels and semantic HTML
- **NO poor performance code** - Optimize where possible
- **NO non-responsive designs** - Everything must be mobile-friendly
- **NO inline styles (except dynamic)** - Use CSS/Tailwind classes

## Warning Zones (Proceed with Caution)

### Database Operations
- Always validate schema before operations
- Use transactions where appropriate
- Include rollback mechanisms

### External Dependencies
- Prefer well-maintained, popular libraries
- Check license compatibility
- Document all dependencies

### File Uploads/Downloads
- Validate file types
- Check file sizes
- Sanitize filenames

### User Input
- Always validate
- Always sanitize
- Never trust user input

## Recommended Patterns

### Instead of This ❌
```javascript
// Bad: No error handling
const data = JSON.parse(response);
```

### Do This ✅
```javascript
// Good: Proper error handling
try {
  const data = JSON.parse(response);
} catch (error) {
  console.error('Failed to parse JSON:', error);
  // Handle error appropriately
}
```

### Instead of This ❌
```javascript
// Bad: Magic number
setTimeout(() => doSomething(), 5000);
```

### Do This ✅
```javascript
// Good: Named constant
const DEBOUNCE_DELAY_MS = 5000;
setTimeout(() => doSomething(), DEBOUNCE_DELAY_MS);
```

## Emergency Stop Conditions

If any of these occur, STOP immediately and report:
1. Attempting to access files outside designated directories
2. Generating code that could cause data loss
3. Creating infinite recursion or loops
4. Exceeding memory/disk limits
5. Violating any absolute prohibition listed above

## Code Review Checklist

Before considering any code complete, verify:
- [ ] No security vulnerabilities
- [ ] All errors are handled
- [ ] Code is documented
- [ ] No no-goes violated
- [ ] Follows project style guide
- [ ] Tests included (if applicable)
- [ ] Performance is acceptable
- [ ] Accessibility requirements met
