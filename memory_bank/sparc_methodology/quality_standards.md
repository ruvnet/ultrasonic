# SPARC Quality Standards

Last Updated: 2025-01-06

## Code Quality Metrics

### Modularity Standards
- **File Size**: Maximum 500 lines per file
- **Function Size**: Maximum 50 lines per function
- **Class Size**: Maximum 300 lines per class
- **Cyclomatic Complexity**: Maximum 10 per function
- **Nesting Depth**: Maximum 4 levels

### Naming Conventions
- **Variables**: camelCase for locals, UPPER_SNAKE_CASE for constants
- **Functions**: camelCase, verb-noun pattern (e.g., `getUserData`)
- **Classes**: PascalCase, noun pattern (e.g., `UserManager`)
- **Files**: kebab-case for general files, PascalCase for class files
- **Test Files**: `*.test.ts` or `*.spec.ts` pattern

## Testing Standards

### Test Coverage Requirements
- **Default Target**: 100% coverage
- **Minimum Acceptable**: 80% (with documented exceptions)
- **Coverage Types**:
  - Line coverage
  - Branch coverage
  - Function coverage
  - Statement coverage

### TDD London School Approach
1. **Write Test First**: Define behavior before implementation
2. **Mock Dependencies**: Use test doubles for isolation
3. **Outside-In**: Start from user-facing behavior
4. **Refactor Safely**: Only with green tests
5. **One Assertion**: Prefer single assertion per test

### Test Organization
```
describe('ComponentName', () => {
  describe('methodName', () => {
    it('should perform expected behavior when condition', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

## Security Standards

### Input Validation
- Validate all external inputs
- Use whitelisting over blacklisting
- Sanitize data before storage
- Validate data types and ranges
- Implement rate limiting

### Secret Management
- **Never** hardcode secrets
- Use environment variables
- Implement proper key rotation
- Audit secret access
- Use secure storage solutions

### Authentication & Authorization
- Implement proper session management
- Use secure password policies
- Implement MFA where appropriate
- Follow principle of least privilege
- Audit access logs

## Performance Standards

### Response Time Targets
- API endpoints: < 200ms (p95)
- Page load: < 3 seconds
- Database queries: < 100ms
- Background jobs: Define SLA per job

### Resource Utilization
- Memory usage: Monitor and set limits
- CPU usage: Optimize hot paths
- Network calls: Minimize and batch
- Database connections: Use pooling

### Optimization Practices
- Profile before optimizing
- Cache frequently accessed data
- Implement pagination
- Use appropriate data structures
- Optimize database queries

## Documentation Standards

### Code Documentation
- **Purpose**: Document why, not what
- **Complexity**: Document complex algorithms
- **Public APIs**: Full JSDoc/TSDoc
- **Examples**: Include usage examples
- **Updates**: Keep in sync with code

### Documentation Types
1. **Inline Comments**: Explain complex logic
2. **Function Documentation**: Parameters, returns, throws
3. **Class Documentation**: Purpose and usage
4. **README Files**: Setup and usage instructions
5. **API Documentation**: Endpoint specifications

### Documentation Template
```typescript
/**
 * Brief description of what the function does.
 * 
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws {ErrorType} Description of when thrown
 * @example
 * ```typescript
 * const result = functionName(param);
 * ```
 */
```

## Code Review Standards

### Review Checklist
- [ ] Follows naming conventions
- [ ] Includes appropriate tests
- [ ] Meets coverage requirements
- [ ] No security vulnerabilities
- [ ] Performance considered
- [ ] Documentation updated
- [ ] No code duplication
- [ ] Error handling implemented

### Review Process
1. Automated checks pass
2. Self-review completed
3. Peer review conducted
4. Feedback addressed
5. Final approval given

## Continuous Integration Standards

### CI Pipeline Requirements
- Automated test execution
- Code coverage reporting
- Linting and formatting
- Security scanning
- Performance testing
- Documentation generation

### Quality Gates
- All tests must pass
- Coverage targets met
- No critical security issues
- No high-priority lint errors
- Performance benchmarks satisfied

## Monitoring Standards

### Application Monitoring
- Error rate tracking
- Performance metrics
- Resource utilization
- User behavior analytics
- Business metrics

### Alerting Thresholds
- Error rate > 1%
- Response time > SLA
- Resource usage > 80%
- Failed health checks
- Security incidents

## Commit Standards

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Test addition/modification
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `arch`: Architecture changes
- `security`: Security improvements

### Commit Frequency Guidelines
- **Phase**: After each SPARC phase
- **Feature**: After each feature completion
- **Manual**: As needed for specific workflows